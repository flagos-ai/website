# TLE-Lite, TLE-Struct, and TLE-Raw

This section introduces TLE-Lite, TLE-Struct, and TLE-Raw and how they are handled in the compilation process.

## TLE-Lite, TLE-Struct, and TLE-Raw introduction

TLE-Lite, TLE-Struct, and TLE-Raw are the compiler languages, located in the middle layer of the AI ecosystem. The upper layer connects AI frameworks through graph compilers and operator libraries, while the lower layer connects to various hardware runtimes.

The following diagram demonstrates the location of TLE-Lite, TLE-Struct, and TLE-Raw in the AI ecosystem.

![alt text](../../assets/images/three-level-tle.png)

These three compiler languages provide different levels of performance optimizations for different users:

- TLE-Lite allows users to modify existing Triton kernels with minimal changes, while being compatible with various hardware backends. It can be used by algorithm engineers in quick optimization scenarios.
- TLE-Struct allows users to explicitly defines structural mapping between computation and data for different clusters with different hardware architectures, such as GPGPU and DSA. It can be used by developers who have a certain understanding of characteristics and optimization of targeted hardware.
- TLE-Raw allows users to directly modify vendors' native programming languages. It can be used by developers who have a good understanding of targeted hardware. These developers are mainly the performance optimization experts.

Hints, TLE-Lite and TLE-Struct will eventually lower to LLVM (Low Level Virtual Machine) IR (Intermediate Representation) through FLIR (that is, FlagTree IR), while TLE-Raw will lower to LLVM IR through the corresponding compilation pipeline of the language, such as the vendor's private compiler. Finally, they will be linked together to jointly generate a complete kernel for the runtime to load and execute.

The following diagram illustrates the TLE-Raw's compatibility with existing DSLs (TileLang and cuTile) as well as essential libraries and tools (PyCUDA and MLIR Pybind), and also the location in the AI ecosystem.

![alt text](../../assets/images/tle-raw.png)

For how to use TLE, see [Use TLE-Lite](/user_guide/use-tle-lite.md), [Use TLE-Struct](/user_guide/use-tle-struct.md), and [Use TLE-Raw](/user_guide/use-tle-raw.md).

## TLE in the compilation process

- Purpose and scope
  - Extends Triton with explicit shared and tensor memory management, asynchronous data movement via Tensor Memory Accelerator (TMA), and pipeline control optimized for NVIDIA Hopper-class GPUs for now.
  - Frontend APIs live under `tle` and lower into custom MLIR dialect and processed by passes under `tle`.
- Frontend DSL layer (Python)
  - `tle.language.core` overrides key `tl` builtins to attach extra attributes (for example, "tt.load.async") and the `buffered_tensor` handles representing shared or tensor memory allocations (core.py) are returned. For example, the key `tl` builtins are `load`, `alloc`, `copy`, `local_load`, `local_store`, and loop helpers.
  - GPU-specific helpers in GPU define layouts (`swizzled_shared_layout`, `nv_mma_shared_layout`, and so on.), scopes (`smem`, `tmem`), and `buffered_tensor` semantics. These semantics wrap IR memdesc types while keeping Triton-style type checking.`
  - Users import these symbols (for example, `tle.alloc`, `tle.copy`, `tle.pipeline`) inside `@triton.jit` kernels to allocate SMEM tiles, launch async copies, or orchestrate staged loops.
- Semantic validation
  - `TLESemantic` in `semantic.py` runs alongside Triton’s semantic layer. It validates shapes, dtypes, and copy compatibility before lowering, providing early error messages and adapting constexpr inputs.
  - Semantic helpers call into custom builder hooks (exposed through the C++ bridge) to emit `LocalAllocOp`, `TMACopyOp`, and so on., ensuring Python APIs map 1:1 to TTIR constructs.
- TLE-Raw and EDSL Layer
  - TLE-Raw (raw) exposes a lightweight MLIR-based EDSL (Embedded Domain-Specific Language) for writing dialect-specific intrinsics directly. Decorators like `@dialect(name="mlir")` build LLVM IR from Python ASTs via `EdslMLIRJITFunction`, enabling backend developers to prototype kernels or helper ops outside the high-level Triton syntax.
  - The TLE-Raw runtime (`call()` helper) materializes `tle::DSLRegionOp` nodes whose bodies are later inlined by passes.
- C++ bridge and dialect
  - `triton_tle.cc` registers additional builder methods (creating encoding attributes, memdesc types, TMACopy ops, DSL regions) onto Triton’s `TritonOpBuilder`, and wires new passes plus raw IR helpers into Python through `pybind11`.
  - The MLIR dialect resides in the dialect directory, encompassing IR definitions and Analysis, Conversion, and Transforms infrastructure that mirrors upstream Triton conventions.
- Pass and lowering pipeline
  - Pass registrations are defined in `Passes.td` and exposed as Python APIs, including `add_early_assign_memory_space`, `add_lower_async_load`, `add_lower_tma_copy`, `add_tle_convert_arg_to_memdesc`, `add_tle_dsl_region_inline`.
  - Key transformations:
    - Early Assign Memory Space rewrites tensors tagged with `tt.memory_space="shared_memory"` into explicit local alloc and store sequences and removes the attribute, and exposes concrete SMEM ops (`TleEarlyAssignMemorySpace.cpp`) for subsequent passes.
    - Lower Async Load looks for loads marked with "tt.load.async" (set by `tle.load`) and converts them into Hopper-style async copy plus commit or wait chains that feed `LocalLoadOps`. It also deduplicates redundant allocations (`TleLowerAsyncLoad.cpp`).
    - Lower TMA Copy lowers high-level `TMACopyOp` (emitted by `tle.copy` with tensor descriptors) into NVIDIA TMA intrinsics, handling both GM→SMEM and SMEM→GM directions with barrier management (`TleLowerTmaCopy.cpp`).
    - Convert Arg To MemDesc materializes memdesc-compatible operands and results within DSL regions by inserting temporary local alloc and load sequences. This allows generic Triton passes to reason about these operands and results (`ConvertArgToMemDesc.cpp`).
    - DSL Region Inline splices `tle::DSLRegionOp` bodies back into surrounding CFG (Control Flow Graph) blocks, replacing yields with branches once TLE-Raw kernels are lowered (`DSLRegionInline.cpp`).
- Backend distribution
  - Backend-specific logic currently targets NVIDIA (see `nvidia` and the use of `triton::nvidia_gpu` intrinsics inside passes). Other hardware backends can be added by reusing the TLE-Raw DSL and pass hooks and implementing their own lowering passes and encodings under `third_party/<backend>/backend/compiler.py`. This extension mechanism is similar to how HINTS are dispatched.
  - Pass wrappers exported from `triton_tle.cc` let each backend opt into only the passes it supports when assembling its pipeline. For example, NVIDIA enables TMA lowering while another backend might stop after memory-space tagging.
- Testing and examples
  - Integration tests under `tle` cover end-to-end kernels for pipeline loops, GEMM, and TMA copies. These tests ensure alignment between Python APIs, semantic checks, and passes.
  - Developers can run `python/test/tle/run_tests.py` after modifying either the Python DSL or MLIR passes to catch regressions quickly.
- Extending TLE
  - New APIs should mirror the established pattern: add Python surface ops with semantic validation → expose necessary builder hooks → create and extend dialect ops → add lowering passes and register them for backends.
  - Centralize layout and scope abstractions in `types.py` to enable toggling future hardware (for example, tensor memory) without touching users' code, and document any new passes in `Passes.td`.