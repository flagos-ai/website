---
license: apache-2.0
language:
- zh
- en
---

# Introduction
On August 28, Tencent Hunyuan released and open‑sourced its new‑generation flagship model Hy4 preview. The Zhongzhi(众智) FlagOS Community completed cross‑chip adaptation, precision alignment and deployment validation of Hy4 preview across AI chips. Multi‑chip‑adapted model images have been simultaneously released on ModelScope and HuggingFace. Developers can directly obtain out‑of‑the‑box solutions for their respective chips.

### Integrated Deployment
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS-Mthreads** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | Hy4-preview-Nvidia-Origin | Hy4-preview-Mthreads-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 90.91                            | Evaluating                                   |
| Musr_team | 82.8                            |  Evaluating                                     |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 20.10.12 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/hy4-preview-mthreads001-gems5.0.2-treenone-cx0.13.0-pluginnone-vllmnone-cp310-pt29-musa43-x64-3.3.5-server:202608300624

```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Hy4-preview-FP8-mthreads-FlagOS --local_dir /data/Hy4-preview
```

### Start the Container
```bash
docker run -dit \
  --name Hy4_preview \
  --privileged \
  --ipc host \
  --network host \
  --shm-size 512g \
  -w /workspace \
  -v /data/:/data/ \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  --env MTHREADS_VISIBLE_DEVICES=all \
harbor.baai.ac.cn/flagos-inner-models-release/preview-mthreads001-gems5.0.2-treenone-cx0.13.0-pluginnone-vllmnone-cp310-pt29-musa43-x64-3.3.5-server:202608300624 \
  sleep infinity
```
### Start the Server
```bash
# first in rank 1：
docker exec -d \
  -e DIST_INIT_ADDR=<rank0_ip>:29699 \
  -e LOG_FILE=/workspace/hy4_adapter_musa/logs/hy4_gpqa_rank1.log \
  Hy4_preview \
  /opt/hy4_tp16_handoff/launch_hy4_pr36805_worker3208x.sh

# then in rank 0：
docker exec -d \
  -e DIST_INIT_ADDR=<rank0_ip>:29699 \
  -e LOG_FILE=/workspace/hy4_adapter_musa/logs/hy4_gpqa_rank0.log \
  Hy4_preview \
  /opt/hy4_tp16_handoff/launch_hy4_pr36805_worker3208x.sh
```

## Service Invocation
### Invocation Script
```bash
curl http://<rank0_ip>:30100/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Hy4-preview",
    "messages": [
      {"role": "user", "content": "你好，请介绍一下自己"}
    ]
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
The model weights are derived from Tencent-Hunyuan/Hy4-preview-FP8 and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
