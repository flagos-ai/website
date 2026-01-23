# FlagTree extensible framework

FlagTree extensible framework is specifically designed to support multi-backend compilation and three-level compiler languages, as mentioned in the [Features](features.md) section. 

- **Backend extensions**: FlagTree follows a plugin-based architecture, where each backend is self-contained in `third_party/[backend_name]/`. Each backend implements the BaseBackend interface, defines its compilation pipeline through `add_stages()`, and provides backend-specific optimizations and code generation. This design allows adding new backends without modifying the core Triton code.

- **Language and compiler optimization extensions**: For existing Triton code, FlagTree adopts incremental extensions for full compatibility with native Triton. These extensions include the following modification to the common architecture:
  - Modifications to Existing Triton Files: FlagTree incrementally extends Triton's compilation pipeline by modifying existing files. For example, `python/triton/runtime/jit.py` is extended to parse `#@hint:` comments and route TLE syntax, attaching hints to AST nodes. TTIR dialect definition files (`.td`) are extended with new attribute definitions to encode hints as MLIR attributes on operations like `tt.load`. Backend compiler files (for example, `backend/compiler.py`) are extended to register new optimization passes that process hints and TLE operations, integrating with the existing pass management infrastructure.

  - New Files Added: FlagTree introduces a complete TLE module as new files in `third_party/tle/`, including dialect definitions (operations like `tle.dsl_region`), transformation pass implementations (memory space assignment, async load lowering, and so on.), LLVM conversion passes, and Python language bindings. This modular design keeps TLE independent from core Triton while integrating through the extended TTIR attributes and backend pass registration mechanism, enabling features like shared memory management and pipeline optimizations without modifying the common architecture.

For TLE specifically, FlagTree maximizes separation between TLE language extensions (`python/triton/experimental/tle/`) and TLE MLIR dialect (`third_party/tle/`). TLE language constructs are defined in Python and integrated through the AST processing pipeline, while TLE dialect operations are implemented in C++/MLIR and integrated through the compilation pipeline. This separation allows language features and IR transformations to evolve independently, improving maintainability and enabling different backends to adopt TLE features at different stages of the compilation pipeline.

The following code structure shows how FlagTree organizes its extensions:

```{code-block} python
flagtree/
├── python/
│   ├── triton/                # Triton core (existing)
│   │   ├── compiler/              
│   │   │   ├── code_generator.py  # [EXTENDED] TLE module dispatch, Hints extraction
│   │   │   └── compiler.py       
│   │   ├── language/              
│   │   │   ├── core.py            # [EXTENDED] Hints
│   │   │   └── semantic.py        # [EXTENDED] Hints
│   │   ├── runtime/               
│   │   │   └── jit.py             # [EXTENDED] Hints
│   │   └── experimental/          # Language extensions
│   │       └── tle/               # TLE (Triton Language Extensions)
│   │           ├── language/      # TLE language definition (extends AST Processing)
│   │           │   ├── core.py    # TLE-Lite: Core TLE language features (for example, tle.load)
│   │           │   ├── [gpu/npu]/ # TLE-Struct: GPU-specific and NPU-specific constructs
│   │           │   │   ├── core.py    
│   │           │   │   ├── semantic.py 
│   │           │   │   └── types.py   
│   │           │   └── raw/       # TLE-Raw: Raw MLIR programming interface
│   │           │       ├── core.py    
│   │           │       └── semantic.py
│   │           └── raw/           # TLE-Raw implementation (extends AST Processing)
│   │               ├── mlir/      # MLIR code generation for TLE-Raw
│   │               │   ├── codegen.py  
│   │               │   └── runtime.py 
│   │               └── runtime.py # Runtime support for TLE-Raw
│   ├── tutorials/             # Tutorials and examples (not in code path)
│   │   └── tle/                # TLE examples
│   │       ├── 01-sparse-mla.py
│   │       └── raw/            # TLE-Raw examples
│   └── test/                   # Test code (not in code path)
│       └── tle/                # TLE tests
│           ├── integration/    # Integration tests
│           ├── unit/           # Unit tests
│           └── run_tests.py
│
└── third_party/              
    ├── [backend_name]/       # Backend-specific extensions
    │   ├── backend/           
    │   │   └── compiler.py    # [EXTENDED] TLE and HINTS pass dispatch
    │   ├── include/           # TTIR dialect definitions (may extend tt.load with attributes)
    │   └── lib/                            
    ├── tle/                  # TLE MLIR extensions
    │   └── dialect/           # TLE dialect implementation
    │       ├── include/IR/    
    │       ├── lib/IR/       
    │       ├── lib/Conversion/  
    │       └── lib/Transforms/
    └── flir/                 # FLIR: FlagTree-maintained common Linalg, including HINTS pass

```

```{note}
The code structure above shows only the key files and directories relevant to FlagTree's extensions. Many other files and subdirectories in the codebase are omitted for clarity.
```