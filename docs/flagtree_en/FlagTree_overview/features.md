# Features

FlagTree includes the following main features:

- **Multi-backend support**
  FlagTree supports a wide range of hardware platforms and has been extensively tested across different hardware configurations. For more information, see [Supported hardware platforms](/getting_started/requirements.md#supported-hardware-platforms).
- **Tree levels of complier hint languages**
  FlagTree provides three levels of complier hint languages tailored for different users:
  - TLE-Lite:
    - Design philosophy: Write once, run everywhere.
    - Core concept: By introducing high-level semantic hints rather than mandatory constraints, guide the compiler to perform heuristic optimization. It emphasizes backward compatibility, allowing developers to achieve cross-platform performance improvements with minimal code intrusiveness without disrupting the original Triton programming paradigm.
  - TLE-Struct:
    - Design philosophy: Architectural perception, fine tuning.
    - Core concept: Based on the hardware topological features, the backend is divided into clusters such as GPGPU and DSA, exposing a universal hierarchical parallel and storage structure. It allows developers to explicitly define the structured mapping relationship between computing and data (such as Warp Group control, pipeline orchestration), decoupling algorithmic logic from the physical implementation of specific hardware at the abstract level.
  - TLE-Raw:
    - Design philosophy: Native transmission, ultimate control.
    - Core concept: Break the abstract boundaries of DSL and support inline native code from vendors. It enables the direct generation of target instructions through the vendor's private compilation pipeline, bypassing the intermediate conversion overhead of general-purpose compilers and granting expert-level users absolute control over instruction scheduling, register allocation, and underlying synchronization primitives.
- **Hints**:
  The topmost-level compiler hint language, tailored for beginners, providing lightweight performance optimizations without altering program semantics or underlying hardware behavior. Hints is fully backward-compatible with native Triton code.
