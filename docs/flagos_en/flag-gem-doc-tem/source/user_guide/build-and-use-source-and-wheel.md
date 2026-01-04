# # Build and install distribution packages

This section introduces how to build source and wheel packages and install FlagGems through these packages.

## Build source and wheel packages

You can package your Python project into a standard format so that others (or production environments) can install and use it conveniently, reliably, and reproducibly.

To build the source and wheel packages with build front end, use the following command:

```{code-block} python
# Install or upgrade the 'build' package, a PEP 517-compliant tool for building Python packages
pip install -U build

# Install dependency
pip install setuptools>=64.0

# Build distribution packages (e.g., sdist and wheel) from the current project directory
python -m build --no-isolation .
```

These commands will first create a source distribution (`sdist`) and then build a binary distribution (`wheel`) from the source distribution.

If you want to disable the default behavior (`source_dir` → `sdist` → `wheel`), you can:

- Pass `--sdist` to build a source distribution from the source (`source_dir` → `sdist`);
- Pass `--wheel` to build a binary distribution from the source (`source_dir` → `wheel`);
- Pass both `--sdist` and `--wheel` to build both the source and binary distributions from the source (`source_dir` → `sdist`, and `source_dir` → `wheel`).

The `.tar.gz` and `.whl` packages are built in the `./dist/` directory.

## Install FlagGems from source or wheel package

If other people have built source or wheel packages in the `./dist/` directory, you can install FlagGems from the source or wheel package.

```{note}
You are recommended to install from source since Python 3.14 hasn't supported a PyTorch version yet.
```

```{note}
# Install flag_gems using the source file without repeatedly installing dependencies
pip install -v . --no-build-isolation

# Or install flag_gems using the wheel package for Windows system
pip install ./dist/flag_gems-4.1-cp314-cp314-win_amd64.whl
```
