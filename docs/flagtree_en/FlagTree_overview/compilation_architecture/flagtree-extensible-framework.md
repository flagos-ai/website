# FlagTree extensible framework

FlagTree extensible framework is specifically designed to support multi-backend compilation and three-level compiler hint languages, as mentioned in the Features section. 

- **Backend extensions**: FlagTree follows a plugin-based architecture, where each backend is self-contained in `third_party/[backend_name]/`. Each backend implements the BaseBackend interface, defines its compilation pipeline through `add_stages()`, and provides backend-specific optimizations and code generation. This design allows adding new backends without modifying the core Triton code.

- **Language and compiler optimization extensions**: For existing Triton code, FlagTree adopts incremental extensions for full compatibility with native Triton. These extensions include the following modification to the common architecture:
  - Adding `flagtree_hints` parameter to `load()` in `core.py` and `semantic.py`
  - Parsing `#@hint:` comments in `jit.py` and extracting hints in `code_generator.py`
  - Dispatching to TLE modules via module_map mechanism in `code_generator.py`
  - Integrating TLE and HINTS passes in backend compilation pipelines

For TLE specifically, FlagTree maximizes separation between TLE language extensions (`python/triton/experimental/tle/`) and TLE MLIR dialect (`third_party/tle/`). TLE language constructs are defined in Python and integrated through the AST processing pipeline, while TLE dialect operations are implemented in C++/MLIR and integrated through the compilation pipeline. This separation allows language features and IR transformations to evolve independently, improving maintainability and enabling different backends to adopt TLE features at different stages of the compilation pipeline.

The following code structure shows how FlagTree organizes its extensions:

```{code-block} python
flagtree/
├── python/
│   ├── triton/                # Triton core (existing)
│   │   ├── compiler/              
│   │   │   ├── code_generator.py  # [EXTENDED] TLE module dispatch, HINTS extraction
│   │   │   └── compiler.py       
│   │   ├── language/              
│   │   │   ├── core.py            # [EXTENDED] HINTS
│   │   │   └── semantic.py        # [EXTENDED] HINTS
│   │   ├── runtime/               
│   │   │   └── jit.py             # [EXTENDED] HINTS
│   │   └── experimental/          # Language extensions
│   │       └── tle/               # TLE (Triton Language Extensions)
│   │           ├── language/      # TLE language definition (extends AST Processing)
│   │           │   ├── core.py    # TLE-Lite: Core TLE language features (e.g., tle.load)
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