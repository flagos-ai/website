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
- Released **FlagOS-Kunlunxin** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | Hy4-preview-Nvidia-Origin | Hy4-preview-Kunlunxin-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 90.91      | Evaluating   |
| Musr_team    | 82.8       |  Evaluating  |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 20.10.12 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/hy4-preview-w8a8-linear-moe-kunlunxin001-gems5.0.0-treenone-cx0.13.0-plugin0.2.0-vllm0.20.2-cp310-pt29-xrt513-x64-5.0.21.47:202608310922
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Hy4-preview-INT8-kunlunxin-FlagOS --local_dir /data/Hy4-preview
```

### Start the Container
```bash
set -euo pipefail

# Run once on each node. Set NODE_RANK=0 on the API node and NODE_RANK=1
# on the worker node. MASTER_ADDR must be the routable address of node 0.
: "${NODE_RANK:?set NODE_RANK to 0 or 1}"
: "${MASTER_ADDR:?set MASTER_ADDR to the address of node 0}"
MASTER_PORT="${MASTER_PORT:-29564}"
CONTAINER_NAME="${CONTAINER_NAME:-hy4-w8a8-flagos-p800}"

docker run -d \
  --name "${CONTAINER_NAME}" \
  --privileged \
  --network host \
  --shm-size 128g \
  --cap-add SYS_PTRACE \
  --ulimit memlock=-1:-1 \
  --ulimit nofile=120000:120000 \
  --ulimit stack=67108864:67108864 \
  -e NODE_RANK="${NODE_RANK}" \
  -e MASTER_ADDR="${MASTER_ADDR}" \
  -e MASTER_PORT="${MASTER_PORT}" \
  -v /data:/data \
  --entrypoint /bin/bash \
  harbor.baai.ac.cn/flagrelease-public/hy4-preview-w8a8-linear-moe-kunlunxin001-gems5.0.0-treenone-cx0.13.0-plugin0.2.0-vllm0.20.2-cp310-pt29-xrt513-x64-5.0.21.47:202608310922 \
  -lc 'sleep infinity'
```
### Start the Server
```bash
# Run once on each node after both containers exist. The API is exposed by
# rank 0 at port 8000 after all 16 ranks have joined.
CONTAINER_NAME="${CONTAINER_NAME:-hy4-w8a8-flagos-p800}"

docker exec -d "${CONTAINER_NAME}" /bin/bash -lc '
set -euo pipefail
export USE_FLAGGEMS=1
export VLLM_DISABLE_PYNCCL=1
export VLLM_PLUGINS=fl
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS=1800
export PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
exec /root/miniconda/envs/python310_torch29_cuda/bin/vllm serve /data/Hy4-preview \
    --served-model-name hy4-w8a8 \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 16 \
    --enable-expert-parallel \
    --enable-ep-weight-filter \
    --all2all-backend allgather_reducescatter \
    --distributed-executor-backend mp \
    --nnodes 2 \
    --node-rank "${NODE_RANK}" \
    --master-addr "${MASTER_ADDR}" \
    --master-port "${MASTER_PORT}" \
    --distributed-timeout-seconds 1800 \
    --load-format hy4_safetensors \
    --dtype bfloat16 \
    --disable-custom-all-reduce \
    --max-model-len 8192 \
    --max-num-seqs 8 \
    --max-num-batched-tokens 1024 \
    --block-size 128 \
    --gpu-memory-utilization 0.90 \
    --enable-chunked-prefill \
    --no-enable-prefix-caching \
    --enforce-eager >>"/var/log/hy4-w8a8-vllm-rank${NODE_RANK}.log" 2>&1
'
```

## Service Invocation
### Invocation Script
```bash
set -euo pipefail

# Run on node 0 after /health returns HTTP 200.
curl --noproxy '*' -fsS http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"hy4-w8a8","messages":[{"role":"user","content":"Compute 17 * 19. Return only the integer."}],"temperature":0,"max_tokens":64}'

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
The model weights are derived from Tencent-Hunyuan/Hy4-preview and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
