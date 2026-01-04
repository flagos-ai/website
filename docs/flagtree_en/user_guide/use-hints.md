# User Guide

`flagtree_hints` allows users to provide optimization hints to the compiler through trailing comments in the Triton Kernel code.

You can simply add hints by placing a trailing comment with the format # @hint: <hint_name> on the same line as operations like `tl.load`.

```{code-block} python
# Hints are embedded as trailing comments using the '@hint:' prefix.
mat_a_block = tl.load(mat_a + mat_a_offset, mask=mat_a_mask, other=0.0)  # @hint: dot_pad_only_k
x = tl.load(x_ptr + offsets, mask=mask)  # @hint: mask_opt
for s in range(0, 2):  # @hint: bind_sub_block
    # ... code ...
```

These hints help the compiler generate more efficient code for these operations.