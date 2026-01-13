# Use TLE-Raw

This section introduces how to use TLE-Raw. TLE-Raw is available on trition_3.5.x branch.

## MLIR

The following is an example of MLIR (Multi-Level Intermediate Representation).

```{code-block} python
from typing import Annotated
from mlir import ir
from mlir.dialects import arith, nvvm, tensor
import triton.language as tl
from triton.experimental.flagtree.edsl import dialect
import triton.experimental.flagtree.language as fl

# 1. Dialect declaration
@tle.raw.language(name="mlir")
# 2. Hardware constraint
@tle.hardware_constraint(threads_dim=1, sync_scope="block")
# 3. Function implementation
def vector_add_tile(
    x: Annotated[ir.RankedTensorType, "tensor<1024xf32>"],
    y: Annotated[ir.RankedTensorType, "tensor<1024xf32>"],
    output: Annotated[ir.RankedTensorType, "tensor<1024xf32>"]
):
    # Write low-level operations directly using the MLIR Python bindings
    tidx = nvvm.ThreadIdXOp(ir.IntegerType.get_signless(32)).res
    bidx = nvvm.BlockIdXOp(ir.IntegerType.get_signless(32)).res
    bdimx = nvvm.BlockDimXOp(ir.IntegerType.get_signless(32)).res
    idx = arith.addi(arith.muli(bidx, bdimx), tidx)
    idx = arith.index_cast(ir.IndexType.get(), idx)
    xval = tensor.extract(x, [idx])
    yval = tensor.extract(y, [idx])
    result = arith.addf(xval, yval)
    tensor.insert(result, output, [idx])

@tle.jit
def add_kernel(
    x_ptr, y_ptr, output_ptr,
    n_elements,
    BLOCK_SIZE: tl.constexpr,
):
    #  Tile language main code
    pid = tl.program_id(axis=0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n_elements
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    output = tl.zeros_like(x)
    
    # 4. Function call
    tle.call(
        vector_add_tile,
        args=[x, y, output],
        hardware={
            "threads": (BLOCK_SIZE,),  # Must satisfies threads_dim=1
        },
        layout={
            x: {"space": "shared", "order": [0]},      # Shared memory, one-dimensional layout (for optimizing connection)
            y: {"space": "shared", "order": [0]},
            output: {"space": "shared", "order": [0]}
        }
    )
    tl.store(output_ptr + offsets, output, mask=mask)
```

TLE-raw consists of the following four parts:

- Dialect declaration (decorator)
  - Decorator: `@tle.raw.language(name="mlir")`
  - Explanation: This decorator marks the function `vector_add_tile` as a block of code written directly in the MLIR dialect. It tells the compiler, specifically through the FlagTree EDSL (Embedded Domain Specific Language), that the body of this function should be interpreted and lowered using MLIR operations (such as `nvvm`, `arith`, and `tensor`), rather than standard Python or Triton operations.
- Hardware constraint (decorator)
  - Decorator: `@tle.hardware_constraint(threads_dim=1, sync_scope="block")`
  - Explanation: This decorator imposes constraints on the hardware execution model for the `vector_add_tile` function. It specifies that the function operates in a 1-dimensional thread space (`threads_dim=1`) and that synchronization primitives should be scoped at the block level (`sync_scope="block"`).
- Function implementation
  - Function: `vector_add_tile(...)`
  - Explanation: This is the actual implementation of the computation kernel written using low-level MLIR Python bindings. It defines the specific operations (thread indexing, memory loading, floating-point addition, and memory storing) that will be executed by the hardware. The function signature uses Annotated types to explicitly define the input and output as `tensor<1024xf32>` (1024-element float32 tensors), ensuring the compiler knows the exact data layout and types to expect.
- Function call
  - Invocation: `tle.call(vector_add_tile, args=[x, y, output], hardware={...}, layout={...})`
  - Explanation: This line invokes the declared MLIR function (`vector_add_tile`) from within the high-level Triton kernel (`add_kernel`). It passes the input tensors `x`, `y`, and the output buffer. Crucially, it provides hardware mapping hints (defining the number of threads) and memory layout specifications (defining the tensors as residing in "shared" memory with a specific order). This allows the compiler to bridge the gap between the high-level `tl.load`/`tl.store` operations and the low-level MLIR IR generation.
