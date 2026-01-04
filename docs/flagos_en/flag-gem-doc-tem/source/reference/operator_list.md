## Operator List

The following table lists the latest supported operators.

| No. | Operator Name                     | Description                                                                 | Operation Type                   |
|-----|-----------------------------------|-----------------------------------------------------------------------------|----------------------------------|
| 1   | abs                               | Element-wise absolute value.                                                | Pointwise and Reduction Operations |
| 2   | abs_                              | In-place absolute value.                                                    | Pointwise and Reduction Operations |
| 3   | add                               | Element-wise addition (supports scalar or tensor).                          | Pointwise and Reduction Operations |
| 4   | add_                              | In-place addition.                                                          | Pointwise and Reduction Operations |
| 5   | addcdiv                           | Computes `input + value * (tensor1 / tensor2)`.                             | Pointwise and Reduction Operations |
| 6   | addcmul                           | Computes `input + value * (tensor1 * tensor2)`.                             | Pointwise and Reduction Operations |
| 7   | addmm                             | Computes `beta * input + alpha * mat1 @ mat2` (matrix multiplication with bias). | BLAS Operations                |
| 8   | addmv                             | Computes `beta * input + alpha * mat @ vec` (matrix-vector product).        | BLAS Operations                |
| 9   | addr                              | Computes `beta * input + alpha * vec1 ⊗ vec2` (outer product with scaling). | BLAS Operations                |
| 10  | all                               | Tests if all elements evaluate to True (optionally along a dimension).      | Pointwise and Reduction Operations |
| 11  | allclose                          | Checks if two tensors are element-wise equal within a tolerance.            | Pointwise and Reduction Operations |
| 12  | amax                              | Maximum value along given dimensions, ignoring NaNs.                        | Pointwise and Reduction Operations |
| 13  | angle                             | Returns the phase angle (in radians) of complex numbers.                    | Pointwise and Reduction Operations |
| 14  | any                               | Tests if any element evaluates to True (optionally along a dimension).      | Pointwise and Reduction Operations |
| 15  | apply_rotary_pos_emb              | Applies rotary positional embeddings (used in Transformers).                | Attention Operations           |
| 16  | arange                            | Creates a 1D tensor with evenly spaced values within a given interval.      | Pointwise and Reduction Operations |
| 17  | argmax                            | Returns indices of maximum values along a dimension.                        | Pointwise and Reduction Operations |
| 18  | argmin                            | Returns indices of minimum values along a dimension.                        | Pointwise and Reduction Operations |
| 19  | atan                              | Element-wise arctangent (inverse tangent).                                  | Pointwise and Reduction Operations |
| 20  | atan_                             | In-place arctangent.                                                        | Pointwise and Reduction Operations |
| 21  | avg_pool2d                        | 2D average pooling.                                                         | Pointwise and Reduction Operations |
| 22  | batch_norm                        | Batch normalization.                                                        | Normalization Operations       |
| 23  | bitwise_and                       | Element-wise bitwise AND.                                                   | Pointwise and Reduction Operations |
| 24  | bitwise_and_                      | In-place bitwise AND.                                                       | Pointwise and Reduction Operations |
| 25  | bitwise_left_shift                | Element-wise left bit shift (`x << y`).                                     | Pointwise and Reduction Operations |
| 26  | bitwise_not                       | Element-wise bitwise NOT.                                                   | Pointwise and Reduction Operations |
| 27  | bitwise_not_                      | In-place bitwise NOT.                                                       | Pointwise and Reduction Operations |
| 28  | bitwise_or                        | Element-wise bitwise OR.                                                    | Pointwise and Reduction Operations |
| 29  | bitwise_or_                       | In-place bitwise OR.                                                        | Pointwise and Reduction Operations |
| 30  | bitwise_right_shift               | Element-wise right bit shift (`x >> y`).                                    | Pointwise and Reduction Operations |
| 31  | bmm                               | Batch matrix-matrix product.                                                | BLAS Operations                |
| 32  | cat                               | Concatenates tensors along a specified dimension.                           | Pointwise and Reduction Operations |
| 33  | celu                              | Continuously Differentiable Exponential Linear Unit activation.             | Pointwise and Reduction Operations |
| 34  | celu_                             | In-place CELU.                                                              | Pointwise and Reduction Operations |
| 35  | clamp                             | Clamps all elements in input into the range `[min, max]`.                   | Pointwise and Reduction Operations |
| 36  | clamp_                            | In-place clamp.                                                             | Pointwise and Reduction Operations |
| 37  | clamp_min                         | Clamps all elements to be ≥ `min`.                                          | Pointwise and Reduction Operations |
| 38  | clamp_min_                        | In-place clamp_min.                                                         | Pointwise and Reduction Operations |
| 39  | concat_and_cache_mla              | Custom operator for concatenation and caching in MLA (Multi-head Latent Attention). | Attention Operations       |
| 40  | contiguous                        | Returns a contiguous tensor in memory (no numerical change).                | Pointwise and Reduction Operations |
| 41  | conv1d                            | 1D convolution.                                                             | Pointwise and Reduction Operations |
| 42  | conv2d                            | 2D convolution.                                                             | Pointwise and Reduction Operations |
| 43  | conv3d                            | 3D convolution.                                                             | Pointwise and Reduction Operations |
| 44  | cos                               | Element-wise cosine.                                                        | Pointwise and Reduction Operations |
| 45  | cos_                              | In-place cosine.                                                            | Pointwise and Reduction Operations |
| 46  | count_nonzero                     | Counts non-zero elements (optionally along dimensions).                     | Pointwise and Reduction Operations |
| 47  | cross_entropy_loss                | Cross-entropy loss function.                                                | Pointwise and Reduction Operations |
| 48  | cummax                            | Cumulative maximum along a dimension (returns values and indices).          | Pointwise and Reduction Operations |
| 49  | cummin                            | Cumulative minimum along a dimension (returns values and indices).          | Pointwise and Reduction Operations |
| 50  | cumsum                            | Cumulative sum along a dimension.                                           | Pointwise and Reduction Operations |
| 51  | diag                              | Extracts diagonal or constructs diagonal matrices.                          | Pointwise and Reduction Operations |
| 52  | diag_embed                        | Embeds input as the diagonal of a zero matrix.                              | Pointwise and Reduction Operations |
| 53  | diagonal                          | Returns specified diagonals of a tensor.                                    | Pointwise and Reduction Operations |
| 54  | div                               | Element-wise division.                                                      | Pointwise and Reduction Operations |
| 55  | div_                              | In-place division.                                                          | Pointwise and Reduction Operations |
| 56  | dot                               | Dot product of two 1D tensors.                                              | BLAS Operations                |
| 57  | dropout                           | Randomly zeros elements during training for regularization.                 | Pointwise and Reduction Operations |
| 58  | elu                               | Exponential Linear Unit activation.                                         | Pointwise and Reduction Operations |
| 59  | elu_                              | In-place ELU.                                                               | Pointwise and Reduction Operations |
| 60  | embedding                         | Looks up embeddings from a weight matrix (e.g., word embeddings).           | Pointwise and Reduction Operations |
| 61  | eq                                | Element-wise equality comparison (returns boolean tensor).                  | Pointwise and Reduction Operations |
| 62  | erf                               | Gaussian error function.                                                    | Pointwise and Reduction Operations |
| 63  | erf_                              | In-place error function.                                                    | Pointwise and Reduction Operations |
| 64  | exp                               | Element-wise natural exponential (`e^x`).                                   | Pointwise and Reduction Operations |
| 65  | exp2                              | Element-wise power of two (`2^x`).                                          | Pointwise and Reduction Operations |
| 66  | exp2_                             | In-place exp2.                                                              | Pointwise and Reduction Operations |
| 67  | exp_                              | In-place natural exponential.                                               | Pointwise and Reduction Operations |
| 68  | exponential_                      | Fills tensor in-place with samples from an exponential distribution.        | Pointwise and Reduction Operations |
| 69  | eye                               | Creates an identity matrix.                                                 | Pointwise and Reduction Operations |
| 70  | fill                              | Fills tensor with a specified value.                                        | Pointwise and Reduction Operations |
| 71  | fill_                             | In-place fill.                                                              | Pointwise and Reduction Operations |
| 72  | flash_attention_forward           | Forward pass of FlashAttention (efficient attention mechanism).             | Attention Operations           |
| 73  | flash_attn_varlen_func            | FlashAttention supporting variable-length sequences.                        | Attention Operations           |
| 74  | flash_mla                         | Flash Multi-head Latent Attention (custom efficient attention).             | Attention Operations           |
| 75  | flip                              | Reverses the order of elements along given dimensions.                      | Pointwise and Reduction Operations |
| 76  | floor_divide                      | Element-wise floor division (`//`).                                         | Pointwise and Reduction Operations |
| 77  | floor_divide_                     | In-place floor division.                                                    | Pointwise and Reduction Operations |
| 78  | full                              | Creates a tensor filled with a specified value.                             | Pointwise and Reduction Operations |
| 79  | full_like                         | Creates a tensor with same shape as input, filled with a specified value.   | Pointwise and Reduction Operations |
| 80  | fused_add_rms_norm                | Fused operation: addition followed by RMS normalization (for LLM inference).| Fused Operations               |
| 81  | gather                            | Gathers values along a dimension using index tensor.                        | Pointwise and Reduction Operations |
| 82  | ge                                | Element-wise greater-than-or-equal-to comparison.                           | Pointwise and Reduction Operations |
| 83  | gelu                              | Gaussian Error Linear Unit activation.                                      | Pointwise and Reduction Operations |
| 84  | gelu_                             | In-place GELU.                                                              | Pointwise and Reduction Operations |
| 85  | gelu_and_mul                      | Fused operation: `GELU(x) * x` (used in SwiGLU).                            | Fused Operations               |
| 86  | get_scheduler_metadata            | Retrieves metadata for inference scheduler (internal use).                  | Pointwise and Reduction Operations |
| 87  | glu                               | Gated Linear Unit activation.                                               | Pointwise and Reduction Operations |
| 88  | group_norm                        | Group normalization.                                                        | Normalization Operations       |
| 89  | gt                                | Element-wise greater-than comparison.                                       | Pointwise and Reduction Operations |
| 90  | hstack                            | Horizontal stacking (column-wise concatenation).                            | Pointwise and Reduction Operations |
| 91  | index_add                         | Adds values to specified indices along a dimension.                         | Pointwise and Reduction Operations |
| 92  | index_add_                        | In-place index_add.                                                         | Pointwise and Reduction Operations |
| 93  | index_put                         | Writes values into specified indices.                                       | Pointwise and Reduction Operations |
| 94  | index_put_                        | In-place index_put.                                                         | Pointwise and Reduction Operations |
| 95  | index_select                      | Selects elements along a dimension using indices.                           | Pointwise and Reduction Operations |
| 96  | instance_norm                     | Instance normalization.                                                     | Normalization Operations       |
| 97  | isclose                           | Element-wise check if two tensors are close within tolerance.               | Pointwise and Reduction Operations |
| 98  | isfinite                          | Checks if elements are finite (not inf/NaN).                                | Pointwise and Reduction Operations |
| 99  | isin                              | Tests if each element is in a given set.                                    | Pointwise and Reduction Operations |
| 100 | isinf                             | Checks if elements are infinite.                                            | Pointwise and Reduction Operations |
| 101 | isnan                             | Checks if elements are NaN.                                                 | Pointwise and Reduction Operations |
| 102 | kron                              | Kronecker product.                                                          | BLAS Operations                |
| 103 | layer_norm                        | Layer normalization.                                                        | Normalization Operations       |
| 104 | le                                | Element-wise less-than-or-equal-to comparison.                              | Pointwise and Reduction Operations |
| 105 | lerp                              | Linear interpolation: `start + weight * (end - start)`.                     | Pointwise and Reduction Operations |
| 106 | lerp_                             | In-place linear interpolation.                                              | Pointwise and Reduction Operations |
| 107 | linspace                          | Returns evenly spaced values over a specified interval.                     | Pointwise and Reduction Operations |
| 108 | log                               | Element-wise natural logarithm.                                             | Pointwise and Reduction Operations |
| 109 | log_sigmoid                       | Log-Sigmoid activation.                                                     | Pointwise and Reduction Operations |
| 110 | log_softmax                       | Numerically stable `log(softmax(x))`.                                       | Pointwise and Reduction Operations |
| 111 | logical_and                       | Element-wise logical AND.                                                   | Pointwise and Reduction Operations |
| 112 | logical_not                       | Element-wise logical NOT.                                                   | Pointwise and Reduction Operations |
| 113 | logical_or                        | Element-wise logical OR.                                                    | Pointwise and Reduction Operations |
| 114 | logical_xor                       | Element-wise logical XOR.                                                   | Pointwise and Reduction Operations |
| 115 | logspace                          | Returns numbers spaced evenly on a log scale (base 10).                     | Pointwise and Reduction Operations |
| 116 | lt                                | Element-wise less-than comparison.                                          | Pointwise and Reduction Operations |
| 117 | masked_fill                       | Fills elements where mask is True with a specified value.                   | Pointwise and Reduction Operations |
| 118 | masked_fill_                      | In-place masked_fill.                                                       | Pointwise and Reduction Operations |
| 119 | masked_select                     | Selects elements where mask is True (returns 1D tensor).                    | Pointwise and Reduction Operations |
| 120 | max                               | Maximum value (optionally along a dimension).                               | Pointwise and Reduction Operations |
| 121 | max_pool2d                        | 2D max pooling.                                                             | Pointwise and Reduction Operations |
| 122 | maximum                           | Element-wise maximum of two tensors.                                        | Pointwise and Reduction Operations |
| 123 | mean                              | Mean along specified dimensions.                                            | Pointwise and Reduction Operations |
| 124 | min                               | Minimum value (optionally along a dimension).                               | Pointwise and Reduction Operations |
| 125 | minimum                           | Element-wise minimum of two tensors.                                        | Pointwise and Reduction Operations |
| 126 | mm                                | Matrix multiplication (2D only).                                            | BLAS Operations                |
| 127 | moe_align_block_size              | Helper operator for aligning block sizes in Mixture-of-Experts (MoE).       | Pointwise and Reduction Operations |
| 128 | mse_loss                          | Mean Squared Error loss.                                                    | Pointwise and Reduction Operations |
| 129 | mul                               | Element-wise multiplication.                                                | Pointwise and Reduction Operations |
| 130 | mul_                              | In-place multiplication.                                                    | Pointwise and Reduction Operations |
| 131 | multinomial                       | Samples from a multinomial distribution.                                    | Pointwise and Reduction Operations |
| 132 | mv                                | Matrix-vector product.                                                      | BLAS Operations                |
| 133 | nan_to_num                        | Replaces NaN, positive/negative infinity with finite numbers.               | Pointwise and Reduction Operations |
| 134 | ne                                | Element-wise not-equal comparison.                                          | Pointwise and Reduction Operations |
| 135 | neg                               | Element-wise negation (`-x`).                                               | Pointwise and Reduction Operations |
| 136 | neg_                              | In-place negation.                                                          | Pointwise and Reduction Operations |
| 137 | nll_loss                          | Negative log-likelihood loss (common in classification).                    | Pointwise and Reduction Operations |
| 138 | nonzero                           | Returns indices of non-zero elements.                                       | Pointwise and Reduction Operations |
| 139 | normal                            | Fills tensor with samples from a normal distribution.                       | Pointwise and Reduction Operations |
| 140 | ones                              | Creates a tensor filled with ones.                                          | Pointwise and Reduction Operations |
| 141 | ones_like                         | Creates a tensor of ones with the same shape as input.                      | Pointwise and Reduction Operations |
| 142 | outer                             | Outer product of two vectors.                                               | BLAS Operations                |
| 143 | pad                               | Pads a tensor (e.g., constant, reflect modes).                              | Pointwise and Reduction Operations |
| 144 | polar                             | Constructs complex numbers from magnitude and angle.                        | Pointwise and Reduction Operations |
| 145 | pow                               | Element-wise power (`x^y`).                                                 | Pointwise and Reduction Operations |
| 146 | pow_                              | In-place power.                                                             | Pointwise and Reduction Operations |
| 147 | prod                              | Product of elements along a dimension.                                      | Pointwise and Reduction Operations |
| 148 | quantile                          | Computes quantiles (percentiles).                                           | Pointwise and Reduction Operations |
| 149 | rand                              | Samples from uniform distribution on [0, 1).                                | Pointwise and Reduction Operations |
| 150 | rand_like                         | Creates a tensor with same shape as input, filled with uniform random values.| Pointwise and Reduction Operations |
| 151 | randn                             | Samples from standard normal distribution.                                  | Pointwise and Reduction Operations |
| 152 | randn_like                        | Creates a tensor with same shape as input, filled with standard normal random values.| Pointwise and Reduction Operations |
| 153 | randperm                          | Returns a random permutation of integers.                                   | Pointwise and Reduction Operations |
| 154 | reciprocal                        | Element-wise reciprocal (`1/x`).                                            | Pointwise and Reduction Operations |
| 155 | reciprocal_                       | In-place reciprocal.                                                        | Pointwise and Reduction Operations |
| 156 | relu                              | Rectified Linear Unit: `max(0, x)`.                                         | Pointwise and Reduction Operations |
| 157 | relu_                             | In-place ReLU.                                                              | Pointwise and Reduction Operations |
| 158 | remainder                         | Element-wise remainder (similar to `%`, sign follows divisor).              | Pointwise and Reduction Operations |
| 159 | remainder_                        | In-place remainder.                                                         | Pointwise and Reduction Operations |
| 160 | repeat                            | Repeats tensor along each dimension.                                        | Pointwise and Reduction Operations |
| 161 | repeat_interleave                 | Repeats each element a specified number of times.                           | Pointwise and Reduction Operations |
| 162 | reshape_and_cache                 | Reshapes and caches key/value tensors (for autoregressive decoding).        | Attention Operations           |
| 163 | reshape_and_cache_flash           | FlashAttention-optimized KV cache update.                                   | Attention Operations           |
| 164 | resolve_conj                      | Returns a physical copy resolving conjugate views.                          | Pointwise and Reduction Operations |
| 165 | resolve_neg                       | Returns a physical copy resolving negative views.                           | Pointwise and Reduction Operations |
| 166 | rms_norm                          | Root Mean Square Layer Normalization.                                       | Normalization Operations       |
| 167 | rsqrt                             | Element-wise reciprocal square root (`1/√x`).                               | Pointwise and Reduction Operations |
| 168 | rsqrt_                            | In-place reciprocal square root.                                            | Pointwise and Reduction Operations |
| 169 | rwkv_mm_sparsity                  | Sparse matrix multiplication optimized for RWKV models.                     | BLAS Operations                |
| 170 | rwkv_ka_fusion                    | Fused kernel for RWKV time-mixing module.                                   | Fused Operations               |
| 171 | scaled_dot_product_attention      | Scaled dot-product attention (PyTorch 2.0+ core operator).                  | Attention Operations           |
| 172 | scatter                           | Writes values into specified indices along a dimension.                     | Pointwise and Reduction Operations |
| 173 | scatter_                          | In-place scatter.                                                           | Pointwise and Reduction Operations |
| 174 | select_scatter                    | Writes source tensor into a slice of target tensor.                         | Pointwise and Reduction Operations |
| 175 | sigmoid                           | Sigmoid activation: `1 / (1 + exp(-x))`.                                    | Pointwise and Reduction Operations |
| 176 | sigmoid_                          | In-place sigmoid.                                                           | Pointwise and Reduction Operations |
| 177 | silu                              | SiLU (Swish) activation: `x * sigmoid(x)`.                                  | Pointwise and Reduction Operations |
| 178 | silu_                             | In-place SiLU.                                                              | Pointwise and Reduction Operations |
| 179 | silu_and_mul                      | Fused operation: `SiLU(x) * y` (used in GLU variants).                      | Fused Operations               |
| 180 | sin                               | Element-wise sine.                                                          | Pointwise and Reduction Operations |
| 181 | sin_                              | In-place sine.                                                              | Pointwise and Reduction Operations |
| 182 | skip_layer_norm                   | Fused residual connection + layer normalization.                            | Fused Operations               |
| 183 | slice_scatter                     | Writes source tensor into a slice region of target tensor.                  | Pointwise and Reduction Operations |
| 184 | softmax                           | Softmax function (exponentiate and normalize).                              | Pointwise and Reduction Operations |
| 185 | softplus                          | Softplus activation: `log(1 + exp(x))`.                                     | Pointwise and Reduction Operations |
| 186 | sort                              | Sorts elements along a dimension (returns values and indices).               | Pointwise and Reduction Operations |
| 187 | sqrt                              | Element-wise square root.                                                   | Pointwise and Reduction Operations |
| 188 | sqrt_                             | In-place square root.                                                       | Pointwise and Reduction Operations |
| 189 | stack                             | Stacks tensors along a new dimension.                                       | Pointwise and Reduction Operations |
| 190 | std                               | Standard deviation along specified dimensions.                              | Pointwise and Reduction Operations |
| 191 | sub                               | Element-wise subtraction.                                                   | Pointwise and Reduction Operations |
| 192 | sub_                              | In-place subtraction.                                                       | Pointwise and Reduction Operations |
| 193 | sum                               | Sum of elements along specified dimensions.                                 | Pointwise and Reduction Operations |
| 194 | tan                               | Element-wise tangent.                                                       | Pointwise and Reduction Operations |
| 195 | tan_                              | In-place tangent.                                                           | Pointwise and Reduction Operations |
| 196 | tanh                              | Hyperbolic tangent activation.                                              | Pointwise and Reduction Operations |
| 197 | tanh_                             | In-place hyperbolic tangent.                                                | Pointwise and Reduction Operations |
| 198 | threshold                         | Thresholds elements: if < threshold, replace with value; else keep.         | Pointwise and Reduction Operations |
| 199 | tile                              | Repeats tensor like NumPy’s tile.                                           | Pointwise and Reduction Operations |
| 200 | to_copy                           | Copies tensor and converts dtype/device.                                    | Pointwise and Reduction Operations |
| 201 | topk                              | Returns top-k largest elements and their indices along a dimension.         | Pointwise and Reduction Operations |
| 202 | trace                             | Sum of diagonal elements of a 2D matrix.                                    | Pointwise and Reduction Operations |
| 203 | topk_softmax                      | Fused top-k selection followed by softmax (for sparse attention).           | Fused Operations               |
| 204 | triu                              | Returns upper triangular part of matrix (others zeroed).                    | Pointwise and Reduction Operations |
| 205 | uniform_                          | Fills tensor in-place with samples from a uniform distribution.             | Pointwise and Reduction Operations |
| 206 | unique                            | Returns unique elements (with optional inverse/count).                      | Pointwise and Reduction Operations |
| 207 | upsample_bicubic2d_aa             | Anti-aliased bicubic 2D upsampling.                                         | Pointwise and Reduction Operations |
| 208 | upsample_nearest2d                | Nearest-neighbor 2D upsampling.                                             | Pointwise and Reduction Operations |
| 209 | var_mean                          | Computes variance and mean simultaneously.                                  | Pointwise and Reduction Operations |
| 210 | vdot                              | Conjugating dot product (for complex tensors).                              | BLAS Operations                |
| 211 | vector_norm                       | Computes vector norms (L1, L2, Frobenius, etc.).                            | Pointwise and Reduction Operations |
| 212 | vstack                            | Vertical stacking (row-wise concatenation).                                 | Pointwise and Reduction Operations |
| 213 | weight_norm                       | Weight normalization (splits weight into direction and magnitude).          | Normalization Operations       |
| 214 | where                             | Conditional selection: `where(condition, x, y)`.                            | Pointwise and Reduction Operations |
| 215 | zeros                             | Creates a tensor filled with zeros.                                         | Pointwise and Reduction Operations |
| 216 | zeros_like                        | Creates a zero-filled tensor with same shape as input.                      | Pointwise and Reduction Operations |
