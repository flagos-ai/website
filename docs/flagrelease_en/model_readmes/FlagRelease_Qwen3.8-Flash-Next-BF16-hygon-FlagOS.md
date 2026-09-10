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
- Released **FlagOS-Hygon** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.	


# Evaluation Results
## Benchmark Result
| Metrics      | Qwen3.8-Flash-Next-Nvidia-Origin | Qwen3.8-Flash-Next-Hygon-FlagOS |
|--------------|----------------------------------|---------------------------------|
| GPQA_Diamond | 92.9                             | 89.9                     |
| MuSR         | 78.57                            | 77.51                             |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 20.10.5, build 55c4c88 |
| Operating System | Ubuntu 22.04.4 LTS (Jammy Jellyfish) |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-hygon001-gems5.4.0-tree0.6.1-cxnone-plugin0.2.0-vllm0.24.0-cp310-pt210-dtk2604-x64-6.3.30-v1.4.1a:202608280655
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Qwen3.8-Flash-Next-BF16-hygon-FlagOS --local_dir /data/Qwen3.8-Flash-Next
```

### Start the Container
```bash
docker run -d --name flagos \
  --network host --ipc host \
  --device /dev/kfd --device /dev/mkfd --device /dev/dri \
  --mount type=bind,src=/dev/infiniband,dst=/dev/infiniband \
  --mount type=bind,src=/sys/class/infiniband,dst=/sys/class/infiniband,readonly \
  --mount type=bind,src=/sys/class/infiniband_verbs,dst=/sys/class/infiniband_verbs,readonly \
  --mount type=bind,src=/sys/class/net,dst=/sys/class/net,readonly \
  --mount type=bind,src=/usr/etc/libibverbs.d,dst=/usr/etc/libibverbs.d,readonly \
  --mount type=bind,src=/lib/x86_64-linux-gnu/libibverbs.so.1.14.44.0,dst=/lib/x86_64-linux-gnu/libibverbs.so.1.14.47.0,readonly \
  --mount type=bind,src=/lib/x86_64-linux-gnu/libshca-rdmav34.so,dst=/lib/x86_64-linux-gnu/libshca-rdmav34.so,readonly \
  --mount type=bind,src=/lib/x86_64-linux-gnu/libnl-3.so.200,dst=/lib/x86_64-linux-gnu/libnl-3.so.200,readonly \
  --mount type=bind,src=/lib/x86_64-linux-gnu/libnl-route-3.so.200,dst=/lib/x86_64-linux-gnu/libnl-route-3.so.200,readonly \
  -v /opt/hyhal:/opt/hyhal \
  -v /data:/data:rslave \
  -v /public-flash:/public-flash \
  --group-add video \
  --cap-add SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --security-opt label=disable \
  -e HSA_FORCE_FINE_GRAIN_PCIE=1 \
  -e NCCL_IB_DISABLE=0 \
  harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-hygon001-gems5.4.0-tree0.6.1-cxnone-plugin0.2.0-vllm0.24.0-cp310-pt210-dtk2604-x64-6.3.30-v1.4.1a:202608280655 \
  bash -lc 'sleep infinity'
docker exec -it flagos /bin/bash
```
### Start the Server
```bash
set +o nounset
source /opt/dtk-26.04-DCC2602-0317/env.sh
set -o nounset
export HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
export HSA_FORCE_FINE_GRAIN_PCIE=1
export TRITON_HIP_CLANG_PATH=/opt/dtk-26.04-DCC2602-0317/aillvm/bin/clang-18
export LD_LIBRARY_PATH="/opt/ucx-shca/lib:/opt/rccl-shca-net/lib:${LD_LIBRARY_PATH:-}"
export UCX_MODULE_DIR=/opt/ucx-shca/lib/ucx
export MASTER_ADDR=10.232.2.19
export GLOO_SOCKET_IFNAME=ib0
export NCCL_SOCKET_IFNAME=ib0
export NCCL_NET_PLUGIN=shca
export NCCL_IB_DISABLE=0
export NCCL_IB_HCA=shca_0,shca_1,shca_2,shca_3
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_DATASETS_OFFLINE=1
# vLLM 0.24+ RPC timeout for execute_model calls (seconds).
# W8A8 quantized models need extra time on first inference for kernel compilation.
export VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS=1800
vllm serve "$MODEL_PATH" \
    --served-model-name "$SERVED_MODEL_NAME" \
    --trust-remote-code \
    --distributed-executor-backend mp \
    --nnodes 1 \
    --node-rank "$NODE_RANK" \
    --master-addr "$MASTER_ADDR" \
    --master-port "$MASTER_PORT" \
    --distributed-timeout-seconds 1800 \
    --tensor-parallel-size "$TP" \
    --pipeline-parallel-size "$PP" \
    --data-parallel-size "$DP" \
    --load-format "$LOAD_FORMAT" \
    --mm-encoder-tp-mode data \
    --disable-custom-all-reduce \
    --moe-backend triton \
    --max-model-len "${MAX_MODEL_LEN:-32768}" \
    --reasoning-parser qwen3 \
    --max-num-seqs 16 \
    --gpu-memory-utilization 0.95 \
    --language-model-only \
    --no-enable-log-requests
```

## Service Invocation
### Invocation Script
```bash
curl http://localhost:$MASTER_PORT/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "$SERVED_MODEL_NAME",
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
- Enter your question (e.g., “Explain the basics of quantum computing”)
- Click the send button to get a response
# Technical Overview
**FlagOS** is a fully open-source system software stack designed to unify the "model–system–chip" layers and foster an open, collaborative ecosystem. It enables a “develop once, run anywhere” workflow across diverse AI accelerators, unlocking hardware performance, eliminating fragmentation among vendor-specific software stacks, and substantially lowering the cost of porting and maintaining AI workloads. With core technologies such as the **FlagScale**, together with vllm-plugin-fl, distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the **FlagOS** stack to automatically produce and release various combinations of \<chip + open-source model\>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.
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

