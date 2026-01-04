# Release Notes

This section includes the FlagGems release information.

## v4.2

- **Added features**：
  - Supported 216 operators that is aligned with the Operator List.
  - Added the following operators: `tan`, `tan_`, `baddbmm`, `avg_pool2d`, `clamp_min`, `clamp_min_`, `std`, `trace`, `max_pool2d`, `bitwise_left_shift`, and `bitwise_right_shift`.
- **Changed features**:
  - Split `upsample` operator into `upsample_nearest2d` and `upsample_bicubic2d_aa`.

## v4.1

- **Added features**:
  - Released RWKV related operators and supported 204 operators.
  - Included fused kernels `rwkv_mm_sparsity` and `rwkv_ka_fusion` optimized for RWKV inference acceleration scenarios.
  - Adopted by the RWKV project in [`BlinkDL/Albatross:faster_251101`](https://github.com/BlinkDL/Albatross/tree/faster_251101).

## v4.0

- **Added features**:
  - Supported 202 operators.
  - Added the following operators: `addcdiv`, `addcmul`, `addmv`, `addr`, `atan`, `atan_`, `celu`, `celu_`, `elu_`, `exp2`, `exp2_`, `get_scheduler_metadata`, `index_add_`, `logspace`, `moe_align_block_size`, `softplus`, `sqrt_`, and `topk_softmax`.
- **Changed features**:
  - Triton JIT C++ runtime shipped precompiled kernels for the following operators:  
    `add`, `addmm`, `argmax`, `bmm`, `cat`, `contiguous`, `embedding`, `exponential_`, `fill`, `flash_attn_varlen_func`, `fused_add_rms_norm`, `max`, `mm`, `nonzero`, `reshape_and_cache_flash`, `rms_norm`, `rotary_embedding`, `softmax`, `sum`, `topk`, and `zeros`.

## v3.0

- **Added features**:
  - Supported 184 operators, including custom operators used in large model inference.
  - Supported more hardware platforms, for example, supported Ascend, AIPU and so on.
  - Supported compatibility with the vLLM framework and passed the inference verification of DeepSeek model.

## v2.1

- **Added features**:
  - Supported the following Tensor operators: `where`, `arange`, `repeat`, `masked_fill`, `tile`, `unique`, `index_select`, `masked_select`, `ones`, `ones_like`, `zeros`, `zeros_like`, `full`, `full_like`, `flip`, and `pad`.
  - Supported the following neural network operator: `embedding`.
  - Supported the following basic math operators: `allclose`, `isclose`, `isfinite`, `floor_divide`, `trunc_divide`, `maximum`, and `minimum`.
  - Supported the following distribution operators: `normal`, `uniform_`, `exponential_`, `multinomial`, `nonzero`, `topk`, `rand`, `randn`, `rand_like`, and `randn_like`.
  - Supported the following science operators: `erf`, `resolve_conj`, and `resolve_neg`.

## v2.0

- **Added features**:
  - Supported the following BLAS operators: `mv`, `outer`.
  - Supported the following pointwise operators: `bitwise_and`, `bitwise_not`, `bitwise_or`, `cos`, `clamp`, `eq`, `ge`, `gt`, `isinf`, `isnan`, `le`, `lt`, `ne`, `neg`, `or`, `sin`, `tanh`, `sigmoid`.
  - Supported the following reduction operators: `all`, `any`, `amax`, `argmax`, `max`, `min`, `prod`, `sum`, `var_mean`, `vector_norm`, `cross_entropy_loss`, `group_norm`, `log_softmax`, `rms_norm`.
  - Supported the following fused operators: `fused_add_rms_norm`, `skip_layer_norm`, `gelu_and_mul`, `silu_and_mul`, `apply_rotary_position_embedding`.

## v1.0

- **Added features**:
  - Supported the following BLAS operators: `addmm`, `bmm`, `mm`.
  - Supported the following pointwise operators: `abs`, `add`, `div`, `dropout`, `exp`, `gelu`, `mul`, `pow`, `reciprocal`, `relu`, `rsqrt`, `silu`, `sub`, `triu`.
  - Supported the following reduction operators: `cumsum`, `layernorm`, `mean`, `softmax`.
