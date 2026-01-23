# Requirements

This section includes requirements of using FlagTree, including supported platforms and dependencies. FlagTree can be successfully installed and run only when all requirements are met.

## Supported hardware platforms

The following list includes the supported hardware platforms:

- AIPU
- Cambricon
- Enflame
- Huawei Ascend
- Hygon
- Iluvatar
- MetaX
- Mthreads
- NVIDIA
- AMD
- klx
- Tsingmicro

## System software requirements

You may need the following system softwares:

- Ubuntu
- Python 3.x

## Backends, Triton versions, and branches

Each backend is based on different versions of Triton, and therefore resides in different protected branches. All these protected branches have equal status.


|Branch|Vendor|Backend|Triton version|
|:-----|:-----|:------|:-------------|
|[main](https://github.com/flagos-ai/flagtree/tree/main)|NVIDIA, AMD, x86_64 cpu, ILUVATAR, Moore Threads, KLX, MetaX, HYGON|[nvidia](/third_party/nvidia/), [amd](/third_party/amd/), [triton-shared](https://github.com/microsoft/triton-shared), [iluvatar](/third_party/iluvatar/), [mthreads](/third_party/mthreads/), [xpu](/third_party/xpu/), [metax](/third_party/metax/), [hcu](third_party/hcu/)|3.1, 3.1, 3.1, 3.1, 3.1, 3.0, 3.1, 3.0|
|[triton_v3.2.x](https://github.com/flagos-ai/flagtree/tree/triton_v3.2.x)|NVIDIA, AMD, Huawei Ascend, Cambricon|[nvidia](https://github.com/FlagTree/flagtree/tree/triton_v3.2.x/third_party/nvidia/), [amd](https://github.com/FlagTree/flagtree/tree/triton_v3.2.x/third_party/amd/), [ascend](https://github.com/FlagTree/flagtree/blob/triton_v3.2.x/third_party/ascend), [cambricon](https://github.com/FlagTree/flagtree/tree/triton_v3.2.x/third_party/cambricon/)|3.2|
|[triton_v3.3.x](https://github.com/flagos-ai/flagtree/tree/triton_v3.3.x)|NVIDIA, AMD, x86_64 cpu, ARM China, Tsingmicro, Enflame|[nvidia](https://github.com/FlagTree/flagtree/tree/triton_v3.3.x/third_party/nvidia/), [amd](https://github.com/FlagTree/flagtree/tree/triton_v3.3.x/third_party/amd/), [triton-shared](https://github.com/microsoft/triton-shared), [aipu](https://github.com/FlagTree/flagtree/tree/triton_v3.3.x/third_party/aipu/), [tsingmicro](https://github.com/FlagTree/flagtree/tree/triton_v3.3.x/third_party/tsingmicro/), [enflame](https://github.com/FlagTree/flagtree/tree/triton_v3.3.x/third_party/enflame/)|3.3|
|[triton_v3.4.x](https://github.com/flagos-ai/flagtree/tree/triton_v3.4.x)|NVIDIA, AMD|[nvidia](https://github.com/FlagTree/flagtree/tree/triton_v3.4.x/third_party/nvidia/), [amd](https://github.com/FlagTree/flagtree/tree/triton_v3.4.x/third_party/amd/)|3.4|
|[triton_v3.5.x](https://github.com/flagos-ai/flagtree/tree/triton_v3.5.x)|NVIDIA, AMD|[nvidia](https://github.com/FlagTree/flagtree/tree/triton_v3.5.x/third_party/nvidia/), [amd](https://github.com/FlagTree/flagtree/tree/triton_v3.5.x/third_party/amd/)|3.5|

## Dependencies

- **System dependencies**  
  FlagTree is primarily tested on Ubuntu. We recommend using a Linux virtual machine or Docker container for installation.
  The following table lists the dependencies for Ubuntu.

    | Dependency     | Description |
    |----------------|-------------|
    | `zlib1g`       | The compression library runtime files. This is a widely used software library for data compression, commonly used by other packages (such as `libxml2`) to handle compressed data streams. |
    | `zlib1g-dev`   | The compression library development files. Contains the header files and static libraries required to compile and link programs that use the zlib compression library. |
    | `libxml2`      | The GNOME XML library runtime. Provides software libraries for parsing, manipulating, and generating XML data, and is used by many applications and dependencies. |
    | `libxml2-dev`  | The GNOME XML library development files. Includes header files and symbolic links necessary for developing software that uses `libxml2` (for example, compiling XML-parsing programs). |

- **Python dependencies**  
  The following table lists the Python dependencies. These dependencies are included in the `requirements.txt` file and will be automatically installed when using the `pip install` command.

    | Dependency   | Description |
    |--------------|-------------|
    | `ninja`      | A small build system with a focus on speed. It is often used as a backend for CMake to compile C/C++ code much faster than traditional Make. |
    | `cmake`      | A cross-platform tool for building, testing, and packaging software. It is used to control the software compilation process via configuration files. |
    | `wheel`      | A Python library that provides the `bdist_wheel` command for setuptools. It allows Python packages to be distributed in a built-package format (`.whl`), which is faster to install than source distributions. |
    | `GitPython`  | A Python library used to interact with Git repositories. It allows Python code to perform Git operations (like `log`, `commit`, `diff`) programmatically. |
    | `pytest`     | A mature full-featured Python testing framework. It is used for writing and running simple unit tests as well as complex functional tests. |
    | `scipy`      | A fundamental library for scientific computing and technical computing in Python. It builds on NumPy and provides modules for optimization, integration, interpolation, eigenvalue problems, algebra, and other tasks. |
    | `filelock`   | A platform-independent file-based lock for Python. It is used to synchronize access to a shared resource (like a file) between multiple Python processes or threads. |
    | `nanobind`   | A lightweight C++ library that exposes C++ types and functions to Python. It is used to create Python bindings for C++ code with minimal overhead (similar to pybind11, but faster). |

  - **Backend specific dependencies**  
    For more information, see [Install FlagTree for different backends](/getting_started/install.md#install-flagtree-for-different-backends).
  
## Features on different branches

- Hints are available on specific branches. For more information, see [Use Hints](/user_guide/use-hints.md).
- TLE-Lite, TLE-Struct, and TLE-Raw are available on trition_3.5.x. for GPU vendors and Huawei Ascend.
