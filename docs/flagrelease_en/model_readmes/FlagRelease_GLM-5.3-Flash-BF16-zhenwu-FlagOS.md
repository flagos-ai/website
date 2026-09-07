---
license: apache-2.0
language:
- zh
- en
---

# Introduction
GLM‑5.3‑Flash is the first natively multimodal model in the GLM‑5 series. It has 320B total parameters with 18B activated per token. It outperforms GLM‑5.2 and scores 57 points on the globally‑recognized Artificial Analysis Composite Intelligence Index (AA Composite Intelligence Index), ranking among the world’s frontier models and matching the score of Claude Opus 4.8. In Z.ai’s internal Code‑Bench experiential evaluation, its coding performance is on par with Claude Opus 4.8.

The FlagOS community has completed day‑0 adaptation, precision alignment and deployment validation for AI chips from nine vendors: T‑Head (平头哥), NVIDIA(英伟达), Moore Threads（摩尔）, Ascend（华为）, Hygon（海光）, MetaX（沐曦）, Tsingmicro (清微智能), Kunlunxin（昆仑芯） and Sunrise(曦望). Model images have been published to ModelScope and HuggingFace, enabling developers to get out‑of‑the‑box solutions for respective chips directly.

### Integrated Deployment
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS-Zhenwu** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | GLM-5.3-Flash-Nvidia-Origin | GLM-5.3-Flash-Zhenwu-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 89.29                             | 89.8    |
| Musr | 74.6                             | 72.66     |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 29.7.2 |
| Operating System | 24.04.2 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-pp001-gems5.4-tree0.6.1-cxnone-plugin0.3.0-vllm0.24.0-cp312-ptnone-hggcnone-x64-2.1.1-rbd225:202608271447

```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/GLM-5.3-Flash-BF16-zhenwu-FlagOS --local_dir /data/GLM-5.3-Flash
```

### Start the Container
```bash
docker run --privileged -dit \
  --network=host \
  --device=/dev/infiniband \
  --ipc=host \
  --device=/dev/alixpu_ctl \
  --device=/dev/alixpu \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --init \
  -v /data:/data\
  -w /data/ \
  --name flagos \
  harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-pp001-gems5.4-tree0.6.1-cxnone-plugin0.3.0-vllm0.24.0-cp312-ptnone-hggcnone-x64-2.1.1-rbd225:202608271447
docker exec -it flagos /bin/bash

```
### Start the Server
```bash
NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME=eth0 NCCL_DEBUG=WARN \
  VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS=3600 \
  VLLM_WORKER_MULTIPROC_METHOD=spawn \
  VLLM_USE_BREAKABLE_CUDAGRAPH=1 \
  VLLM_FL_USE_FLAGGEMS_ATTN=1 \
  VLLM_FL_GLM5_PROVIDER=flaggems \
  vllm serve /data/GLM-5.3-Flash \
  --served-model-name glm-5.3-flash \
  --trust-remote-code \
  --tensor-parallel-size 16 \
  --distributed-executor-backend mp \
  --host 0.0.0.0 \
  --port 8021 \
  --max-model-len 65536 \
  --max-num-seqs 32 \
  --gpu-memory-utilization 0.90 \
  --reasoning-parser glm45 \
  --compilation-config \
  '{"cudagraph_mode":"FULL_AND_PIECEWISE","cudagraph_capture_sizes":[1,2,4,8,16,32]}'

```

## Service Invocation
### Invocation Script
```bash
curl http://127.0.0.1:8021/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
      "messages": [{"role": "user", "content": "Hi"}],
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
The model weights are derived from ZhipuAI/GLM-5.3-Flash-BF16 and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
