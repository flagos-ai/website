# Install FlagGems

FlagGems can be installed either as a pure python package, or a package with C-extensions for better runtime performance.

For a fresh installation of FlagGems, follow the steps below.

## Install as Python package

1. Install build dependencies.

   ```{code-block} bash
   # InsInstall and upgrade Python build tools and C++ extension compilation dependencies
   pip install -U scikit-build-core>=0.11 pybind11 ninja cmake
   ```

2. Install FlagTree (optional) and backend dependencies

   ```{code-block} bash
   #    Clone the FlagGems project from the remote Git repository to local
   git clone https://github.com/FlagOpen/FlagGems
   #    Switch the current working directory to the cloned FlagGems project directory
   cd FlagGems/
   # If you want to use the native Triton instead of FlagTree, please skip this step.
   # Install backend specific dependencies through the .txt file. For nvidia, use requirements_nvidia.txt.
   pip install -r flag_tree_requirements/requirements_backendxxx.txt

   ```

3. Install as a pure Python package.
   To install FlagGems as a pure Python package, use the commands below.

   ```{note}
   Following PEP 517, pip uses an isolated environment to build packages. If you do not want build isolation, pass the `--no-build-isolation` flag.
   ```

   You can install the current Python package to the site-package directory or in editable mode:

   - Install to the site-package directory (standard installation)

      ```{code-block} bash
      # Install the current Python package to the site-packages directory
      pip install .
      ```

   - Install in editable mode

      ```{code-block} bash
      #  Install the package in editable mode
      pip install -e .
      ```

You can optionally install FlagGems with its C extension.

## Install with C extension

To install with the C extension, you can use the following examples:

- Example 1: Editable installation with external TritonJIT

   ```{code-block} bash
   # Install/upgrade essential build tools and dependencies for C++ extensions
   pip install -U scikit-build-core ninja cmake pybind11
   
   # Install the package in editable mode with specific CMake options
   CMAKE_ARGS="-DFLAGGEMS_BUILD_C_EXTENSIONS=ON -DFLAGGEMS_USE_EXTERNAL_TRITON_JIT=ON -DTritonJIT_ROOT=<install path of triton-jit>" \
   pip install --no-build-isolation -v -e .
   ```

- Example 2: Editable installation with TritonJIT as a sub-project via FetchContent

   ```{code-block} bash
   # Perform an editable installation of the current package with specific CMake option
   CMAKE_ARGS="-DFLAGGEMS_BUILD_C_EXTENSIONS=ON" \
   pip install --no-build-isolation -v -e .
   ```

To enable C extension building in FlagGems, the CMake option `-DFLAGGEMS_BUILD_C_EXTENSIONS=ON` must be passed to CMake during the configuration stage. In the preceding examples, the environment variable `CMAKE_ARGS` is used to pass the arguments to CMake. You can also use the environment variable `SKBUILD_CMAKE_ARGS` to pass the arguments.

```{note}
Separating CMake options for preceding environment variables are different as follows:
- For the environment variable `CMAKE_ARGS`, separate options through spaces. This relates to the difference between `scikit-build-core` and its predecessor, `scikit-build`.
  
- For the environment `SKBUILD_CMAKE_ARGS`, separate options through semicolons (`;`).
```

## Options and environment variables specific to C extension installation

This section describes the options and environment variables used when installing FlagGems with C extensions.

- Options

  The following table lists the options you may use for installing with C extension:

   | Option                                | Description                                                  | Default                                      |
   |--------------------------------------|--------------------------------------------------------------|----------------------------------------------|
   | `FLAGGEMS_BUILD_C_EXTENSIONS`        | Whether to build C extension                                 | `ON` when it is the op-level project         |
   | `FLAGGEMS_USE_EXTERNAL_TRITON_JIT`   | Whether to use external Triton JIT library                   | `OFF`                                        |
   | `-DTritonJIT_ROOT=<install path>`    | Specify the installation path of Triton JIT library          | —                                            |
   | `FLAGGEMS_USE_EXTERNAL_PYBIND11`     | Whether to use external pybind11 library                     | `ON`                                         |
   | `FLAGGEMS_BUILD_CTESTS`              | Whether to build C++ unit tests                              | Same as `FLAGGEMS_BUILD_C_EXTENSIONS`        |
   | `FLAGGEMS_INSTALL`                   | Whether to install FlagGems's CMake package                  | `ON` when it is the op-level project         |

   The C extension of FlagGems depends on **TritonJIT**, a C++ library that implements a Triton JIT runtime and enables calling Triton JIT functions from C++.

   ```{note}
   If you build FlagGems with an external TritonJIT by setting `-DFLAGGEMS_USE_EXTERNAL_TRITON_JIT=ON`, you must first build and install TritonJIT separately, then pass `-DTritonJIT_ROOT=<install path>` to CMake.
   ```

- Environment variables

   The following environment variables are commonly used to configure `scikit-build-core`:

  - `SKBUILD_CMAKE_BUILD_TYPE`: Specifies the build type. Valid values are:
    - `Release`
    - `Debug`
    - `RelWithDebInfo`
    - `MinSizeRel`

  - `SKBUILD_BUILD_DIR`: Specifies the build directory.  
      Default: `build/<cache_tag>` (as defined in `pyproject.toml`).

## Common `pip` options for both pure Python and C extension installations

The following list includes the commonly used pip options:

- `v`：Show the log of the configuration and building process;
- `e`: Create an editable installation.
- `--no-build-isolation`：Do not create a separate virtualenv to build the project. This is commonly used with an editable installation. Note that when building without isolation, you have to install the build dependencies manually.
- `--no-deps`： Do not install package dependencies. This can be useful when you do not want the dependencies to be updated.
