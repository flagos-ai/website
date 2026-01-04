# Features

FlagGems includes the following main features:

- **Multi-Backend Hardware Support**：FlagGems supports a wide range of hardware platforms and has been extensively tested across different hardware configurations. See Supported hardware platforms.

- **Automatic Codegen**：FlagGems provides an automatic code generation mechanism that enables developers to easily generate both pointwise and fused operators.
The auto-generation system supports a variety of needs, including standard element-wise computations, non-tensor parameters, and specifying output types.
For more details, please refer to pointwise_dynamic(pointwise_dynamic.md). See Generate operators. 

- **LibEntry**：FlagGems introduces `LibEntry`, which independently manages the kernel cache and bypasses the runtime of `Autotuner`, `Heuristics`, and `JitFunction`. To use it, simply decorate the Triton kernel with LibEntry.
  `LibEntry` also supports direct wrapping of `Autotuner`, `Heuristics`, and `JitFunction`, preserving full tuning functionality. However, it avoids nested runtime type invocations, eliminating redundant parameter processing. This means no need for binding or type wrapping, resulting in a simplified cache key format and reduced unnecessary key computation. For more information, see Apply LibEntry decorator to Triton Kernel.

- **C++ Runtime**：FlagGems can be installed either as a pure Python package or as a package with C++ extensions. The C++ runtime is designed to address the overhead of the Python runtime and improve end-to-end performance. For more information, see Install with C extension, C++ tests, Add a C++ wrapper.
