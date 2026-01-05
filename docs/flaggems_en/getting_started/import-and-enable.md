# Import and enable FlagGems

FlagGems supports two common usage patterns: patching PyTorch ATen ops (recommended) and calling FlagGems ops explicitly.

- Enable FlagGems and patch ATen ops
   After `flag_gems.enable()`, supported `torch.* / torch.nn.functional.*` calls will be dispatched to FlagGems implementations automatically.
  - Global enablement
    To apply FlagGems optimizations across your entire script or interactive session:

     ```{code-block} python
      import torch
      import flag_gems

      flag_gems.enable()

      x = torch.randn(4096, 4096, device=flag_gems.device, dtype=torch.float16)
      y = torch.mm(x, x)
     ```

    Once enabled, all supported operators in your code will automatically be replaced with the optimized FlagGems implementations, no further changes needed.

  - Scoped enablement
    To apply FlagGems optimizations across your entire script or interactive session:

     ```{code-block} python
      import torch
      import flag_gems

      with flag_gems.use_gems():
         x = torch.randn(4096, 4096, device=flag_gems.device, dtype=torch.float16)
         y = torch.mm(x, x)
     ```

    Enabling within a specific scope is helpful for the following cases:

    - Benchmark performance differences
    - Compare correctness between implementations
    - Apply acceleration selectively in complex workflows

The `flag_gems.enable(...)` function supports several optional parameters. For more information, see [Use optional parameters for FlagGems enablement function](/user_guide/how-to-use-flaggems.md#use-optional-parameters-for-flaggems-enablement-function).

- Explicitly call FlagGems ops
   You can also bypass PyTorch dispatch and call operators from `flag_gems.ops` directly without using `enable()`:

   ```{code-block} python
   import torch
   from flag_gems import ops
   import flag_gems

   a = torch.randn(1024, 1024, device=flag_gems.device, dtype=torch.float16)
   b = torch.randn(1024, 1024, device=flag_gems.device, dtype=torch.float16)
   c = ops.mm(a, b)
   ```
