# Import and enable FlagGems

You can enable FlagGems globally or enable it within a specific scope.

- Global enablement
  To apply FlagGems optimizations across your entire script or interactive session:

   ```{code-block} python
   import flag_gems

   # Enable flag_gems globally

   flag_gems.enable()
   ```

  Once enabled, all supported operators in your code will automatically be replaced with the optimized FlagGems implementations—no further changes needed.

- Scoped enablement
  To apply FlagGems optimizations across your entire script or interactive session:

   ```{code-block} python
   import flag_gems

   # Enable flag_gems within a specific scope

   with flag_gems.use_gems():
      # Code inside this block will use FlagGems-accelerated operators
      pass
   ```

  Enabling within a specific scope is helpful for the following cases:

  - Benchmark performance differences
  - Compare correctness between implementations
  - Apply acceleration selectively in complex workflows

   Scoped enablement example:

   ```{code-block} python
   import torch
   import flag_gems

   M, N, K = 1024, 1024, 1024
   A = torch.randn((M, K), dtype=torch.float16, device=flag_gems.device)
   B = torch.randn((K, N), dtype=torch.float16, device=flag_gems.device)
   with flag_gems.use_gems():
      C = torch.mm(A, B)
   ```

The `flag_gems.enable(...)` function supports several optional parameters. For more information, see Advanced usage of FlagGems enablement function.
