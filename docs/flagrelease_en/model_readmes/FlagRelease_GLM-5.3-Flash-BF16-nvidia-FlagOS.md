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
- Released **FlagOS-Nvidia** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | GLM-5.3-Flash-Nvidia-Origin | GLM-5.3-Flash-Nvidia-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 89.29                             | 90.36    |
| Musr | 74.6                             | 73.5     |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 24.0.0 |
| Operating System | 22.04.4 LTS |

## Operation Steps

### Download FlagOS Image
```bash
set -euo pipefail

IMAGE=harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-bf16-nvidia003-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20:202608271300
docker pull "${IMAGE}"
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/GLM-5.3-Flash-BF16-nvidia-FlagOS --local_dir /data/GLM-5.3-Flash
```

### Start the Container
```bash
set -euo pipefail

: "${NODE_RANK:?set NODE_RANK to 0 on the API node or 1 on the headless node}"
[[ "${NODE_RANK}" =~ ^[01]$ ]] || { echo "NODE_RANK must be 0 or 1" >&2; exit 2; }

IMAGE=${IMAGE:-harbor.baai.ac.cn/flagos-inner-models-release/glm5.3-flash-bf16-nvidia003-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20@sha256:aa04dfbcf07793d441a1f55713c83f676cdf5e3d77ca39d6ce9bdbf1c9ee8084}
CONTAINER=${CONTAINER:-glm53-flash-flagos-n${NODE_RANK}}
MODEL_ROOT=${MODEL_ROOT:-/data}

driver_libcuda=$(readlink -f "$(ldconfig -p | awk "/libcuda\\.so\\.1 \\(libc6,x86-64\\)/ {print \\$NF; exit}")")
driver_libnvml=$(readlink -f "$(ldconfig -p | awk "/libnvidia-ml\\.so\\.1 \\(libc6,x86-64\\)/ {print \\$NF; exit}")")
driver_libptxjit=$(readlink -f "$(ldconfig -p | awk "/libnvidia-ptxjitcompiler\\.so\\.1 \\(libc6,x86-64\\)/ {print \\$NF; exit}")")
test -f "${driver_libcuda}"
test -f "${driver_libnvml}"
test -f "${driver_libptxjit}"

device_args=()
for dev in /dev/infiniband/* /dev/nvidia[0-9]* /dev/nvidiactl \
    /dev/nvidia-uvm /dev/nvidia-uvm-tools /dev/nvidia-nvlink \
    /dev/nvidia-nvswitch* /dev/nvidia-caps/*; do
    [[ -e "${dev}" ]] && device_args+=(--device "${dev}:${dev}")
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
  "${device_args[@]}" \
  -v "${driver_libcuda}:/driver/libcuda.so.1:ro" \
  -v "${driver_libcuda}:/driver/libcuda.so:ro" \
  -v "${driver_libnvml}:/driver/libnvidia-ml.so.1:ro" \
  -v "${driver_libnvml}:/driver/libnvidia-ml.so:ro" \
  -v "${driver_libptxjit}:/driver/libnvidia-ptxjitcompiler.so.1:ro" \
  -v "${driver_libptxjit}:/driver/libnvidia-ptxjitcompiler.so:ro" \
  -v /data:/models:ro" \
  -e NODE_RANK="${NODE_RANK}" \
  -e CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
  "${IMAGE}" -lc "exec sleep infinity"
```
### Start the Server
```bash
set -euo pipefail

: "${NODE_RANK:?set NODE_RANK to 0 on the API node or 1 on the headless node}"
: "${MASTER_ADDR:?set MASTER_ADDR to a resolvable address of NODE_RANK=0}"
[[ "${NODE_RANK}" =~ ^[01]$ ]] || { echo "NODE_RANK must be 0 or 1" >&2; exit 2; }

CONTAINER=${CONTAINER:-glm53-flash-flagos-n${NODE_RANK}}
MASTER_PORT=${MASTER_PORT:-29873}
PORT=${PORT:-8000}
GLOO_SOCKET_IFNAME=${GLOO_SOCKET_IFNAME:-bond0}
NCCL_SOCKET_IFNAME=${NCCL_SOCKET_IFNAME:-bond0}
NCCL_IB_HCA=${NCCL_IB_HCA:-=mlx5_100:1,mlx5_101:1,mlx5_102:1,mlx5_103:1,mlx5_104:1,mlx5_105:1,mlx5_106:1,mlx5_107:1}

role_args=(--headless)
if [[ "${NODE_RANK}" == 0 ]]; then
  role_args=(--host 0.0.0.0 --port "${PORT}")
fi

docker exec -d \
  -e NODE_RANK="${NODE_RANK}" \
  -e MASTER_ADDR="${MASTER_ADDR}" \
  -e MASTER_PORT="${MASTER_PORT}" \
  -e PORT="${PORT}" \
  -e GLOO_SOCKET_IFNAME="${GLOO_SOCKET_IFNAME}" \
  -e NCCL_SOCKET_IFNAME="${NCCL_SOCKET_IFNAME}" \
  -e NCCL_IB_HCA="${NCCL_IB_HCA}" \
  -e NCCL_IB_DISABLE=0 \
  -e NCCL_CROSS_NIC=0 \
  -e NCCL_NVLS_ENABLE=0 \
  -e LD_LIBRARY_PATH=/driver:/usr/local/cuda/lib64 \
  -e CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
  -e HF_HUB_OFFLINE=1 \
  -e TRANSFORMERS_OFFLINE=1 \
  -e TOKENIZERS_PARALLELISM=false \
  -e VLLM_PLUGINS=fl \
  -e USE_FLAGGEMS=1 \
  -e VLLM_FL_PREFER=flagos \
  -e VLLM_FL_PREFER_ENABLED=true \
  -e VLLM_FL_OOT_ENABLED=1 \
  -e VLLM_FL_STRICT=0 \
  -e VLLM_FL_GLM5_PROVIDER=auto \
  -e VLLM_FL_FLAGOS_WHITELIST=grouped_topk,moe_sum \
  -e VLLM_USE_BREAKABLE_CUDAGRAPH=1 \
  "${CONTAINER}" /usr/local/bin/vllm serve /models/GLM-5.3-Flash \
    --tokenizer /models/GLM-5.3-Flash \
    --served-model-name GLM-5.3-Flash \
    --tensor-parallel-size 16 \
    --pipeline-parallel-size 1 \
    --distributed-executor-backend mp \
    --nnodes 2 \
    --node-rank "${NODE_RANK}" \
    --master-addr "${MASTER_ADDR}" \
    --master-port "${MASTER_PORT}" \
    --distributed-timeout-seconds 1800 \
    --cpu-distributed-timeout-seconds 1800 \
    --load-format auto \
    --dtype bfloat16 \
    --disable-custom-all-reduce \
    --max-model-len 102400 \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 128 \
    --gpu-memory-utilization 0.80 \
    --seed 1234 \
    --compilation-config "{\"cudagraph_mode\":\"PIECEWISE\",\"pass_config\":{\"fuse_allreduce_rms\":false}}" \
    --enable-expert-parallel \
    --mm-encoder-tp-mode data \
    --limit-mm-per-prompt "{\"image\":16,\"video\":0}" \
    --reasoning-parser glm47 \
    --enable-auto-tool-choice \
    --tool-call-parser glm47 \
    "${role_args[@]}"

if [[ "${NODE_RANK}" == 0 ]]; then
  for _ in $(seq 1 360); do
    if curl --noproxy "*" -fsS "http://127.0.0.1:${PORT}/health" >/dev/null; then
      echo "health=200 port=${PORT}"
      exit 0
    fi
    sleep 10
  done
  docker logs --tail 200 "${CONTAINER}" >&2 || true
  exit 1
fi

echo "headless node started; start NODE_RANK=0 and wait for its health check"

```

## Service Invocation
### Invocation Script
```bash
set -euo pipefail

PORT=${PORT:-8000}
curl --noproxy "*" -fsS "http://127.0.0.1:${PORT}/health"
printf "\n"
curl --noproxy "*" -fsS "http://127.0.0.1:${PORT}/v1/models"
printf "\n"
curl --noproxy "*" -fsS "http://127.0.0.1:${PORT}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  --data-binary @- <<JSON
{
  "model": "GLM-5.3-Flash",
  "messages": [
    {"role": "user", "content": "请计算 17+25，只回答结果。"}
  ],
  "temperature": 0,
  "max_tokens": 1024,
  "chat_template_kwargs": {"enable_thinking": true}
}
JSON
printf "\n"
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
