# Requirements

This section includes requirements of using FlagTree, including supported platforms and dependencies. FlagTree can be successfully installed and run only when all requirements are met.

## Supported hardware platforms

The following list includes the supported hardware platforms:
- aipu
- cambricon
- enflame
- huawei ascend
- HYGON
- ILUVATAR
- MetaX
- Moore Threads
- nvidia
- amd
- klx
- tsingmicro

## Tools

The following list includes the supported tools:

- Ubuntu
- Python 3.x
- Triton 3.x

## Dependencies

- **System dependencies**  
  FlagTree is primarily tested on Ubuntu. If you are not on a Linux system, we recommend using an Ubuntu virtual machine or Docker container for installation.  
  The following table lists the dependencies for Ubuntu.

    | Dependency     | Description |
    |----------------|-------------|
    | `zlib1g`       | The compression library runtime files. This is a widely used software library for data compression, commonly used by other packages (such as `libxml2`) to handle compressed data streams. |
    | `zlib1g-dev`   | The compression library development files. Contains the header files and static libraries required to compile and link programs that use the zlib compression library. |
    | `libxml2`      | The GNOME XML library runtime. Provides software libraries for parsing, manipulating, and generating XML data, and is used by many applications and dependencies. |
    | `libxml2-dev`  | The GNOME XML library development files. Includes header files and symbolic links necessary for developing software that uses `libxml2` (e.g., compiling XML-parsing programs). |


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
    For more information, see [](/getting_started/install.md#install-flagtree-for-different-backends).


