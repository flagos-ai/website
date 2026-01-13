# Use TLE-Struct

This section introduces how to use TLE-Struct. TLE-Struct is available on trition_3.5.x branch.

## GPU memory management

You can use the following operations to manage the GPU's memory.

### tle.gpu.alloc

The following example demonstrates how to reserve a block of memory in the GPU's high-speed on-chip  SMEM (Shared Memory) with dimensions `XBLOCK * YBLOCK` and data type `float32`.

```{code-block} python
a_smem = tle.gpu.alloc([XBLOCK, YBLOCK], dtype=tl.float32,
                      layout=None, scope=tle.gpu.storage_kind.smem)
```

### tle.gpu.copy

The following example demonstrates how to load a tile of data from the low-speed GMEM (Global Memory) into the high-speed on-chip SMEM.

- Copy from source:
  - `a_ptrs`: The base pointer(s) in GMEM
  - `ystride_a * yoffs[None, :]`: An offset vector added to the base pointer.
    - `yoffs[None, :]`: Represents a range of Y-axis offsets, broadcasted to a row vector.
    - `ystride_a`: The stride between rows in the source layout. This calculates the exact addresses of the 2D block that tends to load from GMEM.
- To destination:
  - `a_smem`: The previously allocated SMEM buffer. Data will be written here for fast access by the threads in this block.

```{code-block} python
tle.gpu.copy(a_ptrs + ystride_a * yoffs[None, :], a_smem, [XBLOCK, YBLOCK])
```

### tle.gpu.local_load

The following example demonstrates how to load data from the SMEM buffer a_smem into the local registers for the current thread/warp to process.

```{code-block} python
aval = tle.gpu.local_load(a_smem)
```

