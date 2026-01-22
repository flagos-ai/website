# Common architecture

This section introduces the common architecture between FlagTree and Triton. The common architecture comprises **AST Processing**, **Backend Compilation**, and **Runtime System** modules that handle the compilation process.

The following list introduces directories in FlagTree and the functions of each module:

- **AST Processing**:
  - Directory: `python/triton/compiler/` and `python/triton/language/`
  - Function: Understands your code and translates Python kernel code into TTIR（Triton IR）in MLIR（Multi-Level Intermediate Representation）format.
  This module comprises the following submodules:
  - **Language Definition**:
    - Directory: `python/triton/language/`
    - Function: Defines Triton's language constructs, including core types (`core.py`), standard operations (`standard.py`), math functions (`math.py`), and semantic rules (`semantic.py`). These provide the building blocks that kernels use.
  - **Code Generation**:
    - Directory: `python/triton/compiler/code_generator.py`
    - Function: Transforms Python AST（Abstract Syntax Tree）into TTIR （that is Triton IR） operations by recognizing Triton language constructs (defined in `python/triton/language/`) and generating the initial Intermediate Representation (IR).
  - **Compiler Coordination**:
    - Directory: `python/triton/compiler/compiler.py`
    - Function: Orchestrates the compilation process, managing AST sources, IR sources, and coordinating with backends.

- **Backend Compilation**:
  - Directory: `third_party/[backend]/backend/compiler.py`
  - Function: Each backend defines its compilation pipeline through the `add_stages()` method, which specifies how to transform TTIR into executable code. The typical flow includes: TTIR → TTGPU IR/ Linalg IR → LLVM IR → target assembly → binary. Each backend implements these stages with hardware-specific optimizations and code generation.

- **Runtime System**:
  - Directory: `python/triton/runtime/`
  - Function: Handles JIT compilation, kernel caching, and kernel launch. The runtime compiles kernels on-demand when first called, caches compiled results to avoid recompilation, and manages kernel execution on the GPU through backend drivers.
