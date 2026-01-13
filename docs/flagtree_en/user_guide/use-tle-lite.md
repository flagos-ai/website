# Use TLE-Lite

This section introduces how to use TLE-Lite. TLE-Lite is available on trition_3.5.x branch.

## Memory management

You can use the following operations to manage the memory.

### tle.load

The following example demonstrates how to load a tensor asynchronously from GMEM.

```{code-block} python
x = tle.load(..., is_async=True)
```
