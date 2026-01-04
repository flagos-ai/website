# FlagGems overview

FlagGems is a high-performance general operator library implemented in [OpenAI Triton](https://github.com/openai/triton). It aims to provide a suite of kernel functions to accelerate LLM training and inference. Flag Gems is a core component of FlagOS.

By registering with the ATen backend of PyTorch, FlagGems facilitates a seamless transition, allowing users to switch to the Triton function library without the need to modify their model code. Users can still utilize the ATen backend as usual while experiencing significant performance enhancement. The Triton language offers benefits in readability, user-friendliness and performance comparable to CUDA. This convenience allows developers to engage in the development of FlagGems with minimal learning investment.


```{toctree}

features.md
workflow.md

```