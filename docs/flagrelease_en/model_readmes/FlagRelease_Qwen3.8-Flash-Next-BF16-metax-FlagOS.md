---
language:
- zh
- en
license: apache-2.0
---

# Introduction
On August 26, Alibaba open-sourced its multimodal MoE model Qwen3.8-Flash-Next. The FlagOS community completed Day-0 synchronized adaptation across multiple chips, having accomplished multi-chip adaptation, precision alignment, and deployment validation based on the FlagOS unified open-source technology stack on 8 AI chips —  including T-Head (Pingtouge), NVIDIA, Moore Threads, Ascend, MetaX, Kunlunxin, Hygon, and Iluvatar CoreX. The first batch uniformly provides a BF16-precision version. The multi-chip versions have been open-sourced on the ModelScope and Hugging Face platforms, where developers can directly obtain out-of-the-box solutions for their respective chips.


### Integrated Deployment
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS-Metax** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | Qwen3.8-Flash-Next-Nvidia-Origin | Qwen3.8-Flash-Next-Metax-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 92.9       | 91.16            |
| MuSR| 78.57      | 76.58        |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 29.3.1 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-metax001-gems5.4.0-treenone-cxnone-plugin3.0.0-vllm0.24.0-cp312-pt28-maca37-x64-3.8.1:202608261009
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Qwen3.8-Flash-Next-BF16-metax-FlagOS --local_dir /data/Qwen3.8-Flash-Next
```

### Start the Container
```bash
IMAGE="harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-metax001-gems5.4.0-treenone-cxnone-plugin3.0.0-vllm0.24.0-cp312-pt28-maca37-x64-3.8.1:202608261009"
docker run -d \
  --name flagos \
  --network host \
  --shm-size 64g \
  --device /dev/dri:/dev/dri:rwm \
  --device /dev/mxcd:/dev/mxcd:rwm \
  -v /data:/data \
  ${IMAGE} \
  sleep infinity

docker exec -it flagos /bin/bash
```
### Start the Server
```bash
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export GEMS_VENDOR=metax
export VLLM_PLUGINS=fl
export VLLM_FL_FLAGOS_BLACKLIST="mm,mm_out,sort,stable_sort,masked_fill,masked_fill_,log_softmax,log_softmax_out,log_softmax_backward,log_softmax_backward_out,pad,constant_pad_nd,copy_,topk"
export VLLM_ENGINE_ITERATION_TIMEOUT_S=7200
export VLLM_ENGINE_READY_TIMEOUT_S=1800
export VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS=7200
export VLLM_RINGBUFFER_WARNING_INTERVAL=300

vllm serve /data/Qwen3.8-Flash-Next/ \
    --dtype bfloat16 \
    --tensor-parallel-size 8 \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.9 \
    --port 8000 \
    --enforce-eager \
    --trust-remote-code \
    --served-model-name qwen38_flash
```

## Service Invocation
### Invocation Script
```bash
curl http://localhost:8030/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "model": "qwen38_flash",
  "messages": [{"role": "user", "content": "中国的首都是哪里？"}],
  "temperature": 0.7,
  "max_tokens": 1024
}'
```


### AnythingLLM Integration Guide

#### 1. Download & Install

- Visit the official site: https://anythingllm.com/
- Choose the appropriate version for your OS (Windows/macOS/Linux)
- Follow the installation wizard to complete the setup

#### 2. Configuration

- Launch AnythingLLM
- Open settings (bottom left, fourth tab)
- Configure core LLM parameters
- Click "Save Settings" to apply changes

#### 3. Model Interaction

- After model loading is complete:
- Click **"New Conversation"**
- Enter your question (e.g., "Explain the basics of quantum computing")
- Click the send button to get a response
# Technical Overview
**FlagOS** is a fully open-source system software stack designed to unify the "model–system–chip" layers and foster an open, collaborative ecosystem. It enables a "develop once, run anywhere" workflow across diverse AI accelerators, unlocking hardware performance, eliminating fragmentation among vendor-specific software stacks, and substantially lowering the cost of porting and maintaining AI workloads. With core technologies such as the **FlagScale**, together with vllm-plugin-fl, distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the **FlagOS** stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.
## FlagGems
FlagGems is a high-performance, generic operator libraryimplemented in [Triton](https://github.com/openai/triton) language. It is built on a collection of backend-neutralkernels that aims to accelerate LLM (Large-Language Models) training and inference across diverse hardware platforms.
## FlagTree
FlagTree is an open source, unified compiler for multipleAI chips project dedicated to developing a diverse ecosystem of AI chip compilers and related tooling platforms, thereby fostering and strengthening the upstream and downstream Triton ecosystem. Currently in its initial phase, the project aims to maintain compatibility with existing adaptation solutions while unifying the codebase to rapidly implement single-repository multi-backend support. Forupstream model users, it provides unified compilation capabilities across multiple backends; for downstream chip manufacturers, it offers examples of Triton ecosystem integration.
## FlagScale and vllm-plugin-fl
Flagscale is a comprehensive toolkit designed to supportthe entire lifecycle of large models. It builds on the strengths of several prominent open-source projects, including [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) and [vLLM](https://github.com/vllm-project/vllm), to provide a robust, end-to-end solution for managing and scaling large models.
vllm-plugin-fl is a vLLM plugin built on the FlagOS unified multi-chip backend, to help flagscale support multi-chip on vllm framework.
## **FlagCX**
FlagCX is a scalable and adaptive cross-chip communication library. It serves as a platform where developers, researchers, and AI engineers can collaborate on various projects, contribute to the development of cutting-edge AI solutions, and share their work with the global community.

## **FlagEval Evaluation Framework**
 FlagEval is a comprehensive evaluation system and open platform for large models launched in 2023. It aims to establish scientific, fair, and open benchmarks, methodologies, and tools to help researchers assess model and training algorithm performance. It features:
 - **Multi-dimensional Evaluation**: Supports 800+ modelevaluations across NLP, CV, Audio, and Multimodal fields,covering 20+ downstream tasks including language understanding and image-text generation.
 - **Industry-Grade Use Cases**: Has completed horizonta1 evaluations of mainstream large models, providing authoritative benchmarks for chip-model performance validation.

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support
# License
The model weights are derived from Qwen/Qwen3.8-Flash-Next and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt

