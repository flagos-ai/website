# Features

FlagTree includes the following main features:

- **Multi-backend support**
  FlagTree supports a wide range of hardware platforms and has been extensively tested across different hardware configurations. For more information, see [Supported hardware platforms](/getting_started/requirements.md#supported-hardware-platforms).
- **Three levels of compiler hint languages**
  FlagTree provides three levels of compiler hint languages tailored for different users:
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

## TLE-Lite, TLE-Struct, and TLE-Raw

TLE-Lite, TLE-Struct, and TLE-Raw are the compiler hint languages, located in the middle layer of the AI ecosystem. The upper layer connects AI frameworks through graph compilers and operator libraries, while the lower layer connects to various hardware runtimes.

The following diagram demonstrates the location of TLE-Lite, TLE-Struct, and TLE-Raw in the AI ecosystem.

![alt text](../assets/images/three-level-tle.png)

These three compiler hint languages provide different levels of performance optimizations for different users:

- TLE-Lite allows users to modify existing Triton kernels with minimal changes, while being compatible with various hardware backends. It can be used by algorithm engineers in quick optimization scenarios.
- TLE-Struct allows users to explicitly defines structural mapping between computation and data for different clusters with different hardware architectures, such as GPGPU and DSA. It can be used by developers who have a certain understanding of characteristics and optimization of targeted hardware.
- TLE-Raw allows users to directly modify vendors' native programming languages. It can be used by developers who have a good understanding of targeted hardware. These developers are mainly the performance optimization experts.

TLE-Lite and TLE-Struct will eventually lower to LLVM (Low Level Virtual Machine) IR (Intermediate Representation) through FLIR (that is, FlagTree IR), while TLE-Raw will lower to LLVM IR through the corresponding compilation pipeline of the language, such as the vendor's private compiler. Finally, they will be linked together to jointly generate a complete kernel for the runtime to load and execute.

### TLE-Raw

The following diagram illustrates the TLE-Raw's compatibility with existing DSLs (TileLang and cuTile) as well as essential libraries and tools (PyCUDA and MLIR Pybind), and also the location in the AI ecosystem.

![alt text](../assets/images/tle-raw.png)

For TLE usage information, see [Use TLE-Lite](/user_guide/use-tle-lite.md), [Use TLE-Struct](/user_guide/use-tle-struct.md), and [Use TLE-Raw](/user_guide/use-tle-raw.md).

## Hints

Hints provides a non-invasive performance hints injection mechanism that enables hardware-aware optimizations while maintaining full compatibility with native Triton code. The mechanism is simple: programmers add inline comments (`#@hint: <hint_name>`) to the corresponding Triton operations (for example, `tl.load`) to provide hardware-aware optimization hints. These hints are encoded as MLIR (Multi-Level Intermediate Representation) attributes during compilation, enabling the mid-end and backend to apply hardware-aware optimizations and multi-platform dynamic adaptation based on an elastic verification strategy.

This mechanism provides the following characteristics:

- Native compatibility: Hints are optional—kernels remain valid Triton and run correctly with the original Triton compiler.

- Low learning overhead: Hints are added via lightweight comments (`flagtree_hints`) without changing core Triton syntax.

- Enhanced compiler extensibility: New optimizations can be introduced by evolving hint schemas and MLIR attributes, avoiding language-level operation/syntax extensions.

- Enhanced performance capability: Hardware-aware hints unlock additional compiler optimizations to better utilize hardware features.

For Hints usage information, see [Use Hints](/user_guide/use-hints.md).
