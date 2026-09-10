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
- Released **FlagOS-Hygon** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | GLM-5.3-Flash-Nvidia-Origin | GLM-5.3-Flash-Hygon-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 89.29                             | 87.46 |
| Musr | 74.6                             | Evaluating    |


# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 27.3.1 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-hygon001-gems5.4.0-tree0.6.1-cxnone-plugin0.2.0-vllm0.26.1-cp310-pt210-dtk2604-x64-6.3.30-v1.4.1a:202608271850
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/GLM-5.3-Flash-BF16-hygon-FlagOS --local_dir /data/GLM-5.3-Flash
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
  harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-hygon001-gems5.4.0-tree0.6.1-cxnone-plugin0.2.0-vllm0.26.1-cp310-pt210-dtk2604-x64-6.3.30-v1.4.1a:202608271850 \
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
vllm serve /data/GLM-5.3-Flash --served-model-name GLM-5.3-Flash-BF16 --trust-remote-code --distributed-executor-backend mp --nnodes 2 --node-rank 0 --master-addr 10.232.2.30 --master-port 29850 --distributed-timeout-seconds 1800 --tensor-parallel-size 16 --pipeline-parallel-size 1 --data-parallel-size 1 --load-format safetensors --disable-custom-all-reduce --moe-backend triton --max-model-len 131072 --max-num-seqs 64 --gpu-memory-utilization 0.95 --no-enable-log-requests --reasoning-parser glm45 --block-size 128 --host 0.0.0.0 --port 8000
```

## Service Invocation
### Invocation Script
```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "GLM-5.3-Flash-BF16",
    "messages": [{"role": "user", "content": "Hi"}]
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
