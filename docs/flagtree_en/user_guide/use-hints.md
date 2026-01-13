# Use Hints

`flagtree_hints` allows users to provide optimization hints to the compiler through trailing comments in the Triton Kernel code.

You can simply add hints by placing a trailing comment with the format `# @hint: <hint_name>` on the same line as operations like `tl.load`.

Example 1

```{code-block} python
# Hints are embedded as trailing comments using the '@hint:' prefix.
mat_a_block = tl.load(mat_a + mat_a_offset, mask=mat_a_mask, other=0.0)  # @hint: dot_pad_only_k
x = tl.load(x_ptr + offsets, mask=mask) 
for s in range(0, 2):  # @hint: bind_sub_block
    # ... code ...
```

Example 2

```{code-block} python
import triton
import triton.language as tl

@triton.jit
def kernel(x_ptr, y_ptr, N):
    pid = tl.program_id(0)
    x = tl.load(x_ptr + pid)  #@hint: shared_memory
    y = x + 1
    tl.store(y_ptr + pid, y)
```


## Supported hints

The following tables list the optimization hints applicable to Triton operations for compilation on different backends.

NVIDIA

| Hint Name | Triton Operation | Description | Branch |
| :--- | :--- | :--- | :--- |
| shared_memory | tl.load | Converts a global memory load operation to an asynchronous copy to shared memory, then loads from shared memory. The load must be at least 4 bytes and convertible to an async load. | triton_v3.5.x |

Huawei Ascend

| Hint Name | Triton Operation | Description | Branch |
| :--- | :--- | :--- | :--- |
| dot_pad_only_k | tl.load | Optimizes matrix multiplication performance by padding only the K dimension for dot operations. Equivalent to `tl.compile_hint(tensor, "dot_pad_only_k")` in triton-ascend. | triton_v3.2.x_ascend_hints |
| bind_sub_block | for loop | Optimizes parallel execution by binding loop iterations to sub-blocks. Equivalent to `tl.parallel(..., bind_sub_block=True)` in triton-ascend. | triton_v3.2.x_ascend_hints |
| multibuffer | tl.load | Enables multi-buffering optimization to overlap data transfer and computation (fixed to 2 buffer copies). Equivalent to `tl.multibuffer(tensor, 2)` or `tl.compile_hint(tensor, "multi_buffer", 2)` in triton-ascend. | triton_v3.2.x_ascend_hints |

AIPU

| Hint Name | Triton Operation | Description | Branch |
| :--- | :--- | :--- | :--- |
| dma | tl.load | Enables asynchronous DMA transfers for improved performance. Lowers `memref.copy` operations to `memref.dma_start` and `memref.dma_wait` operations. Requires stride-1 memory access patterns. | triton_v3.3.x |
| shared_memory | tl.load | Loads data into shared memory for faster access. Allocates shared memory (memory space 8) with a size 4x (for AIPUcore parallel) the original tensor shape and copies data from global memory. | triton_v3.3.x |

For Hints usage information, see [Use Hints](/user_guide/use-hints.md).
