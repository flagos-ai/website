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
- Released **FlagOS-Nvidia** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | Hy4-preview-Nvidia-Origin | Hy4-preview-Nvidia-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 90.91      | 89.9 |
| Musr_team    | 82.8       |  82.8 |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 24.0.0 |
| Operating System | 22.04.4 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/hy4-preview-fp8-nvidia004-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20:202608300817
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Hy4-preview-FP8-nvidia-FlagOS --local_dir /data/Hy4-preview
```

### Start the Container
```bash
set -euo pipefail

: "${NODE_RANK:?set NODE_RANK to 0 on the API node or 1 on the headless node}"
[[ "${NODE_RANK}" =~ ^[01]$ ]] || { echo "NODE_RANK must be 0 or 1" >&2; exit 2; }
IMAGE_REF="${IMAGE_REF:-harbor.baai.ac.cn/flagos-inner-models-release/hy4-preview-fp8-testing-nvidia003-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20@sha256:4bf8be17128e2b5cdb2ed085bc1e2c621580b08e51d3378e60f901b4fb908927}"
MODEL_SOURCE="${MODEL_SOURCE:-/data/Hy4-preview-FP8-Testing}"
CONTAINER="${CONTAINER:-hy4-flagos-n${NODE_RANK}}"
test -d "${MODEL_SOURCE}"

driver_libcuda=$(readlink -f "$(ldconfig -p | awk "/libcuda.so.1 (libc6,x86-64)/ {print \$NF; exit}")")
driver_libnvml=$(readlink -f "$(ldconfig -p | awk "/libnvidia-ml.so.1 (libc6,x86-64)/ {print \$NF; exit}")")
driver_libptxjit=$(readlink -f "$(ldconfig -p | awk "/libnvidia-ptxjitcompiler.so.1 (libc6,x86-64)/ {print \$NF; exit}")")
test -f "${driver_libcuda}"
test -f "${driver_libnvml}"
test -f "${driver_libptxjit}"

device_args=()
for device in /dev/infiniband/* /dev/nvidia[0-9]* /dev/nvidiactl /dev/nvidia-uvm /dev/nvidia-uvm-tools /dev/nvidia-nvlink /dev/nvidia-nvswitch* /dev/nvidia-caps/*; do
  [[ -e "${device}" ]] && device_args+=(--device "${device}":${device})
done

docker run -d \
  --name "${CONTAINER}" \
  --network host \
  --ipc host \
  --pid host \
  --pids-limit=-1 \
  --shm-size=128g \
  --ulimit memlock=-1:-1 \
  --ulimit stack=67108864:67108864 \
  --cap-add SYS_PTRACE \
  --security-opt seccomp=unconfined \
  --runtime runc \
  --gpus all \
  ${device_args[@]} \
  -v "${driver_libcuda}":/driver/libcuda.so.1:ro \
  -v "${driver_libcuda}":/driver/libcuda.so:ro \
  -v "${driver_libnvml}":/driver/libnvidia-ml.so.1:ro \
  -v "${driver_libnvml}":/driver/libnvidia-ml.so:ro \
  -v "${driver_libptxjit}":/driver/libnvidia-ptxjitcompiler.so.1:ro \
  -v "${driver_libptxjit}":/driver/libnvidia-ptxjitcompiler.so:ro \
  -v "${MODEL_SOURCE}":/models/Hy4-preview-FP8-Testing:ro \
  -e "NODE_RANK=${NODE_RANK}" \
  -e CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
  -e VLLM_PLUGINS=fl \
  -e USE_FLAGGEMS=1 \
  -e HF_HUB_OFFLINE=1 \
  -e TRANSFORMERS_OFFLINE=1 \
  --entrypoint /usr/bin/bash \
  harbor.baai.ac.cn/flagrelease-public/hy4-preview-fp8-nvidia004-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20:202608300817 -lc "exec sleep infinity"
```
### Start the Server
```bash
set -euo pipefail

: "${NODE_RANK:?set NODE_RANK to 0 on the API node or 1 on the headless node}"
: "${MASTER_ADDR:?set MASTER_ADDR to the address reachable by both nodes}"
[[ "${NODE_RANK}" =~ ^[01]$ ]] || { echo "NODE_RANK must be 0 or 1" >&2; exit 2; }
CONTAINER="${CONTAINER:-hy4-flagos-n${NODE_RANK}}"
MASTER_PORT="${MASTER_PORT:-29978}"
PORT="${PORT:-8000}"
MODEL_PATH=/data/Hy4-preview
reasoning_plugin=$(docker exec "${CONTAINER}" /usr/bin/python3 -c "import vllm_fl.reasoning.hy_v4_reasoning_parser as m; print(m.__file__)")
net_env=()
if [[ -n "${GLOO_SOCKET_IFNAME-}" ]]; then net_env+=(-e "GLOO_SOCKET_IFNAME=${GLOO_SOCKET_IFNAME}"); fi
if [[ -n "${NCCL_SOCKET_IFNAME-}" ]]; then net_env+=(-e "NCCL_SOCKET_IFNAME=${NCCL_SOCKET_IFNAME}"); fi
role_args=(--headless)
if [[ "${NODE_RANK}" == 0 ]]; then role_args=(--host 0.0.0.0 --port "${PORT}"); fi

docker exec -d ${net_env[@]} \
  -v /data:/data \
  -e "NODE_RANK=${NODE_RANK}" \
  -e "MASTER_ADDR=${MASTER_ADDR}" \
  -e "MASTER_PORT=${MASTER_PORT}" \
  -e "PORT=${PORT}" \
  -e LD_LIBRARY_PATH=/driver:/usr/local/cuda/lib64 \
  -e CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
  -e HF_HUB_OFFLINE=1 \
  -e TRANSFORMERS_OFFLINE=1 \
  -e TOKENIZERS_PARALLELISM=false \
  -e VLLM_PLUGINS=fl \
  -e USE_FLAGGEMS=1 \
  -e VLLM_FL_PREFER=flagos \
  -e VLLM_FL_PREFER_ENABLED=true \
  -e VLLM_FL_FLAGOS_BLACKLIST_APPEND=linear \
  -e VLLM_FL_FLAGOS_MM_SHAPE_AWARE=1 \
  -e VLLM_FL_FLAGOS_MM_DECODE_MAX_M=64 \
  -e VLLM_HY4_HC_N8_PROJECTION=1 \
  -e VLLM_HY4_HC_POINTWISE_FUSION=1 \
  -e TORCHINDUCTOR_COMPILE_THREADS=1 \
  "${CONTAINER}" /usr/local/bin/vllm serve "${MODEL_PATH}" \
  --tokenizer "${MODEL_PATH}" \
  --served-model-name hy4-preview-fp8 \
  --tensor-parallel-size 16 \
  --pipeline-parallel-size 1 \
  --distributed-executor-backend mp \
  --nnodes 2 \
  --node-rank "${NODE_RANK}" \
  --master-addr "${MASTER_ADDR}" \
  --master-port "${MASTER_PORT}" \
  --distributed-timeout-seconds 1800 \
  --cpu-distributed-timeout-seconds 1800 \
  --load-format hy4_safetensors \
  --dtype bfloat16 \
  --disable-custom-all-reduce \
  --max-model-len 102400 \
  --max-num-seqs 1 \
  --max-num-batched-tokens 8192 \
  --gpu-memory-utilization 0.81 \
  --enable-chunked-prefill \
  --no-enable-prefix-caching \
  --seed 0 \
  --no-enable-log-requests \
  --compilation-config "{\"pass_config\":{\"fuse_allreduce_rms\":false}}" \
  --enable-expert-parallel \
  --enable-ep-weight-filter \
  --all2all-backend allgather_reducescatter \
  --reasoning-parser hy_v4 \
  --reasoning-parser-plugin "${reasoning_plugin}" \
  ${role_args[@]}
```

## Service Invocation
### Invocation Script
```bash
curl --fail-with-body --noproxy "*" 'http://127.0.0.1:8000/v1/chat/completions' \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "model":"hy4-preview-fp8",
    "messages":[
      {"role":"user","content":"Return only 7391"}
    ],
    "temperature":0,
    "max_tokens":32
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
