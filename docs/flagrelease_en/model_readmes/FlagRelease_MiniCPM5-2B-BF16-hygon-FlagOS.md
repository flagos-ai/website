---
frameworks:
- ""
language:
- zh
- en
license: apache-2.0
tasks: []
---

# Introduction
Following its debut at the World Artificial Intelligence Conference (WAIC 2026) on July 19, ModelBest, in partnership with OpenBMB, officially open‑sourced the next‑generation edge model “Little Cannon” MiniCPM5‑2B on September 7. With 2B parameters, the model attained a score of 17 on the authoritative Artificial Analysis (AA‑Index) leaderboard, securing first place worldwide among models under 4B parameters, and recorded an average score of 54.26 across multiple authoritative benchmark evaluations, markedly outperforming same‑size counterparts including Qwen3.5‑2B (41.66), Qwen3‑1.7B (40.89), and Gemma‑4‑E2B‑it (37.62). Natively supporting hybrid thinking for seamless switching between fast responses and deep reasoning, it offers a 512K ultra‑long context window and comes with built‑in core agent capabilities covering tool calling, deep search and code generation, and can serve directly as an edge agent foundation for smartphones, PCs, smart cockpits and other devices. ModelBest additionally released UltraX, its tiered data governance technology, together with full‑process agent training technology.

### Integrated Deployment
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS-Hygon** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | MiniCPM5-2B-Nvidia-Origin | MiniCPM5-2B-Hygon-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| math_500           |           93.46                  |         92.4        |
| mmlu_pro_other |            51.52                |                51.40                 |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 20.10.7, build f0df350 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease-minicpm5-hygon-tree_none-gems_4.2.1rc0-vllm_0.13.0_das.opt1.dtk2604.20260306.g0c698cda-plugin_0.1.0-cx_none-python_3.10.12-torch_2.9.0_das.opt1.dtk2604.20260206.g275d08c:202605211622

```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/MiniCPM5-2B-BF16-hygon-FlagOS --local_dir /data/MiniCPM5-2B
```

### Start the Container
```bash
docker run \
    --name flagos \
    --network=host \
    --ipc=host \
    --device=/dev/kfd \
    --device=/dev/mkfd \
    --device=/dev/dri \
    -v /opt/hyhal:/opt/hyhal \
    -v /data:/data \
    --group-add video \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    -itd \
    harbor.baai.ac.cn/flagrelease-public/flagrelease-minicpm5-hygon-tree_none-gems_4.2.1rc0-vllm_0.13.0_das.opt1.dtk2604.20260306.g0c698cda-plugin_0.1.0-cx_none-python_3.10.12-torch_2.9.0_das.opt1.dtk2604.20260206.g275d08c:202605211622
docker exec -it flagos /bin/bash
```
### Start the Server
```bash
vllm serve /data/MiniCPM5-2B \
    --trust-remote-code \
    --enforce-eager \
    --port 9010 \
    --host 0.0.0.0 \
    --served-model-name minicpm526 \
    --gpu-memory-utilization 0.85
```

## Service Invocation
### Invocation Script
```bash
curl http://localhost:9010/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
      "model": "minicpm526",
      "messages": [{"role": "user", "content": "你好"}]
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
The model weights are derived from OpenBMB/MiniCPM5-2B and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt

