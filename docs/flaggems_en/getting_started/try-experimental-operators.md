# Try out FlagGems experimental operators

The `experimental_ops` module provides a space for new operators that are not yet ready for production release. Operators in this module are accessible via `flag_gems.experimental_ops.*` and follow the same development patterns as core operators. The experimental_ops directory in FlagGems is: `src/flag_gems/experimental_ops`.

```{code-block} python
import flag_gems

# Global enablement

flag_gems.enable()
result = flag_gems.experimental.layer_norm(*args)

# Or scoped enablement

with flag_gems.use_gems():
    result = flag_gems.experimental.layer_norm(*args)
```