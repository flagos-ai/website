# Hints

This section introduces Hints and how Hints are handled in the compilation process.

## Hints introduction

Hints provides a non-invasive performance hints injection mechanism that enables hardware-aware optimizations while maintaining full compatibility with native Triton code. The mechanism is simple: programmers add inline comments (`#@hint: <hint_name>`) to the corresponding Triton operations (for example, `tl.load`) to provide hardware-aware optimization hints. These hints are encoded as MLIR (Multi-Level Intermediate Representation) attributes during compilation, enabling the mid-end and backend to apply hardware-aware optimizations and multi-platform dynamic adaptation based on an elastic verification strategy.

This mechanism provides the following characteristics:

- Native compatibility: Hints are optional—kernels remain valid Triton and run correctly with the original Triton compiler.

- Low learning overhead: Hints are added via lightweight comments (`flagtree_hints`) without changing core Triton syntax.

- Enhanced compiler extensibility: New optimizations can be introduced by evolving hint schemas and MLIR attributes, avoiding language-level operation/syntax extensions.

- Enhanced performance capability: Hardware-aware hints unlock additional compiler optimizations to better utilize hardware features.

For Hints usage information, see [Use Hints](/user_guide/use-hints.md).

## Hints in the compilation process

Hints extends TTIR operations with attributes to enable hardware-aware optimizations. The implementation involves AST processing, TTIR attribute encoding, and backend pass distribution.

- **AST Processing**: Hints are processed in two stages:
  - Parsing: 
    - Directory: `python/triton/runtime/jit.py`
    - Function: The `parse()` method uses Python's `tokenize` module to scan source code for `#@hint:` comments, extracts hint names, and maps them to line numbers. These hints are stored in a `line_flagtree_hints` dictionary and attached to the AST function definition node. 
  - Create Op：
    - Directory: `python/triton/compiler/code_generator.py`, `python/triton/language/core.py`, and `python/triton/language/semantic.py`
    - Function: During code generation, when encountering `tl.load` calls, the code generator retrieves hints from the line number mapping and passes them as the `flagtree_hints` parameter to `load()`. The semantic layer then forwards this parameter to the builder's `create_load()` method, which encodes hints as TTIR operation attributes.

- **TTIR Attribute Extension**: Hints are encoded as attributes on TTIR operations (e.g., `tt.load` operations carry hint attributes), enabling mid-end and backend passes to access and process them.

- **Backend Pass Distribution**: 
  - Directory: `third_party/[backend_name]/backend/compiler.py`
  - Function: Hints processing passes are dispatched in backend compilers (e.g., `third_party/[backend_name]/backend/compiler.py`). Each backend registers appropriate passes based on the hints it supports (e.g., `add_process_shared_memory_hint()` for NVIDIA backend). 

- **Pass Implementation Locations**: Hints processing passes are implemented in the following folders:
  - Backend-specific folders: Each backend may implement hint-specific passes in its own directory (e.g., `third_party/nvidia/`)
  - Linalg/FLIR folders: Common Linalg passes that process hints during structured-to-memref conversions
  - TLE folders: TLE-related passes that may interact with hints during transformations