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
- Released **FlagOS-Metax** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | GLM-5.3-Flash-Nvidia-Origin | GLM-5.3-Flash-Metax-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 89.29                              | Evaluating                               |
|Musr|   74.6       |   Evaluating   | 

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 29.3.1 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-metax001-gems5.4.0-treenone-cxnone-plugin3.0.0-vllm0.24.0-cp312-pt28-maca37-x64-3.8.1:202608301009

```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/GLM-5.3-Flash-BF16-metax-FlagOS --local_dir /data/GLM-5.3-Flash
```

### Start the Container
```bash
IMAGE="harbor.baai.ac.cn/flagrelease-public/glm5.3-flash-metax001-gems5.4.0-treenone-cxnone-plugin3.0.0-vllm0.24.0-cp312-pt28-maca37-x64-3.8.1:202608301009"
docker run -d \
  --name glm5.3-flash \
  --network host \
  --shm-size 64g \
  --device /dev/dri:/dev/dri:rwm \
  --device /dev/mxcd:/dev/mxcd:rwm \
  -v /public-flash/models:/models \
  ${IMAGE} \
  sleep infinity
docker exec -it glm5.3-flash /bin/bash
```
### Start the Server
```bash
# NOTICE! Environment variables must be set first, then start Ray on two Metax 8*64G machines: one as head node and the other as worker node
# GLM‑5.3‑Flash Multi‑node Ray Common Environment Variables
# Execute `source ray_env.sh` on all nodes (head + worker) before starting Ray
# ============ Network Configuration ============
# View network interface: ip addr / ifconfig; --network=host is used, container network interface aligns with host
# MetaX implements MCCL as its NCCL counterpart. Set NCCL_/MCCL_/GLOO_ variables all together
export NIC="${NIC:-inbond1}"
export GLOO_SOCKET_IFNAME=${NIC}
export MCCL_SOCKET_IFNAME=${NIC}
export NCCL_SOCKET_IFNAME=${NIC}

# ============ Ray Cluster Configuration ============
# Fill in HEAD_IP with actual value (inbond1 IP of head host, query via `ip -br addr show inbond1`)
export HEAD_IP="${HEAD_IP:-192.168.2.109}"
export HEAD_PORT="${HEAD_PORT:-6379}"
export RAY_ADDRESS="${HEAD_IP}:${HEAD_PORT}"

# Number of GPUs per machine
export NUM_GPUS="${NUM_GPUS:-8}"

# ============ vLLM / MetaX Runtime ============
export GEMS_VENDOR=metax
export VLLM_PLUGINS=fl
export VLLM_WORKER_MULTIPROC_METHOD=spawn

# Timeout settings (for multi‑node communication, initial Triton compilation and loading of large 288‑expert model)
export VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS=7200
export VLLM_ENGINE_ITERATION_TIMEOUT_S=7200
export VLLM_ENGINE_READY_TIMEOUT_S=3600
export VLLM_RPC_TIMEOUT=36000000

export VLLM_FL_FLAGOS_BLACKLIST="mm,mm_out,bmm,bmm_out,sort,stable_sort,masked_fill,masked_fill_,log_softmax,log_softmax_out,log_softmax_backward,log_softmax_backward_out,pad,constant_pad_nd,copy_,topk,layer_norm"

# ============ Ray Runtime Env ============
# Instruct Ray to inject environment variables automatically across all worker processes
# (export only required before vllm serve on head node)
export RAY_RUNTIME_ENV='{
  "env_vars": {
    "VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS": "7200",
    "VLLM_ENGINE_ITERATION_TIMEOUT_S": "7200",
    "VLLM_RPC_TIMEOUT": "36000000",
    "GLOO_SOCKET_IFNAME": "'"${NIC}"'",
    "MCCL_SOCKET_IFNAME": "'"${NIC}"'",
    "NCCL_SOCKET_IFNAME": "'"${NIC}"'",
    "GEMS_VENDOR": "metax",
    "VLLM_PLUGINS": "fl",
    "VLLM_FL_FLAGOS_BLACKLIST": "'"${VLLM_FL_FLAGOS_BLACKLIST}"'"
  }
}'


# Commands below are executed ONLY on the head node
# ============ Model Configuration ============
export MODEL_PATH="${MODEL_PATH:-/data/GLM-5.3-Flash}"
export MODEL_NAME="${MODEL_NAME:-glm53-flash}"
export PORT="${PORT:-8000}"
export TP_SIZE="${TP_SIZE:-16}"       # 2 nodes × 8 GPUs
export PP_SIZE="${PP_SIZE:-1}"        # Pipeline parallel disabled for now; adjust when out‑of‑memory occurs
export MAX_MODEL_LEN="${MAX_MODEL_LEN:-8192}"

# GLM‑5.3‑Flash Multi‑node — launch vllm serve only (do NOT rebuild Ray cluster)
# Used for restarting vllm process after failure while Ray cluster remains alive
#
# Usage (run on HEAD node):

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/ray_env.sh"

# Verify Ray cluster health
echo "[SERVE] Checking Ray cluster status..."
ray status || { echo "[SERVE] ERROR: Ray cluster unavailable. Please run ray_start_head.sh + ray_start_worker.sh first"; exit 1; }
echo ""

# Launch vllm serve
LOG_DIR="/models/glm53_flash_running/logs"
LOG_FILE="${LOG_DIR}/glm53-ray-serve-$(date +%Y%m%d-%H%M%S).log"
mkdir -p ${LOG_DIR}

echo "[SERVE] Starting vllm serve..." | tee -a ${LOG_FILE}
echo "[SERVE] Log file: ${LOG_FILE}" | tee -a ${LOG_FILE}
echo "[SERVE] Start time: $(date)" | tee -a ${LOG_FILE}
echo "[SERVE] TP=${TP_SIZE} PP=${PP_SIZE} max_model_len=${MAX_MODEL_LEN}" | tee -a ${LOG_FILE}
echo "[SERVE] Model path: ${MODEL_PATH}" | tee -a ${LOG_FILE}
echo ""

/opt/conda/bin/vllm serve ${MODEL_PATH} \
  --port ${PORT} \
  --served-model-name ${MODEL_NAME} \
  --tensor-parallel-size ${TP_SIZE} \
  --pipeline-parallel-size ${PP_SIZE} \
  --distributed-executor-backend ray \
  --dtype bfloat16 \
  --gpu-memory-utilization 0.9 \
  --no-async-scheduling \
  --enforce-eager \
  --trust-remote-code \
  --compilation-config '{"pass_config":{"fuse_allreduce_rms":false}}' \
  --max-model-len 32768 \
  2>&1 | tee -a ${LOG_FILE}

```

## Service Invocation
### Invocation Script
```bash
curl http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{
  "model": "glm53-flash",
  "messages": [{"role": "user", "content": "中国的首都是哪里？"}],
  "temperature": 0.7,
  "max_tokens": 128,
  "chat_template_kwargs": {
     "enable_thinking": false
  }
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
