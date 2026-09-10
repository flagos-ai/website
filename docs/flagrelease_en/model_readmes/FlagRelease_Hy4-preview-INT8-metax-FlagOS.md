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
- Released **FlagOS-Metax** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | Hy4-preview-Nvidia-Origin | Hy4-preview-Metax-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 90.91      | Evaluating   |
| Musr_team    | 82.8       |  Evaluating  |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 29.3.1 |
| Operating System | 22.04 LTS |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/hy4-preview-metax001-gems5.4.0-treenone-cxnone-plugin3.0.0-vllm0.24.0-cp312-pt28-maca37-x64-3.8.1:202608301009

```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Hy4-preview-INT8-metax-FlagOS --local_dir /data/Hy4-preview
```

### Start the Container
```bash
IMAGE="harbor.baai.ac.cn/flagrelease-public/hy4-preview-metax001-gems5.4.0-treenone-cxnone-plugin3.0.0-vllm0.24.0-cp312-pt28-maca37-x64-3.8.1:202608301009"
docker run -d \
  --name flagos\
  --network host \
  --shm-size 64g \
  --device /dev/dri:/dev/dri:rwm \
  --device /dev/mxcd:/dev/mxcd:rwm \
  -v /data:/data \
  ${IMAGE} \
  sleep infinity
docker exec -it flagos/bin/bash
```
### Start the Server
```bash
# Hy4 多机 Ray 公共环境变量
# 所有节点（head + worker）执行 source ray_env.sh 后再启动 ray

# ============ 网络配置 ============
# 查看网卡: ip addr / ifconfig
# 用了 --network=host，容器里网卡和宿主机一致
export GLOO_SOCKET_IFNAME=inbond1
export MCCL_SOCKET_IFNAME=inbond1

# ============ Ray 集群配置 ============
# HEAD_IP 需要按实际填写（主机的 inbond1 IP）
export HEAD_IP="<inbond1 IP>"
export HEAD_PORT=6379
export RAY_ADDRESS="${HEAD_IP}:${HEAD_PORT}"

# ============ vLLM / MetaX 运行时 ============
export GEMS_VENDOR=metax
export VLLM_PLUGINS=fl
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS=6000
export VLLM_ENGINE_ITERATION_TIMEOUT_S=7200
export VLLM_ENGINE_READY_TIMEOUT_S=3600

export VLLM_FL_FLAGOS_BLACKLIST="mm,mm_out,bmm,bmm_out,full,broadcast_to,nonzero,nonzero_numpy,linear,diff,masked_fill,masked_fill_,sort,stable_sort,topk,layer_norm"

export VLLM_HY4_SPARSE_TORCH_REF=0

# ============ Ray Runtime Env ============
# 这个变量让 ray 在所有 worker 进程中自动注入环境变量
# 只在 head 节点 vllm serve 之前 export 即可（worker 通过 ray 传播）
export RAY_RUNTIME_ENV='{
  "env_vars": {
    "VLLM_EXECUTE_MODEL_TIMEOUT_SECONDS": "6000",
    "VLLM_ENGINE_ITERATION_TIMEOUT_S": "7200",
    "GLOO_SOCKET_IFNAME": "inbond1",
    "MCCL_SOCKET_IFNAME": "inbond1",
    "GEMS_VENDOR": "metax",
    "VLLM_PLUGINS": "fl",
    "VLLM_HY4_SPARSE_TORCH_REF": "0",
    "VLLM_FL_FLAGOS_BLACKLIST": "mm,mm_out,bmm,bmm_out,full,broadcast_to,nonzero,nonzero_numpy,linear,diff,masked_fill,masked_fill_,sort,stable_sort,topk,layer_norm"
  }
}'

# ============ 模型配置 ============
export MODEL_PATH="/data/Hy4-preview"
export MODEL_NAME="hy4"
export PORT=8000
export TP_SIZE=8
export PP_SIZE=4
export MAX_MODEL_LEN=8192

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/ray_env.sh"

# 确认 ray 集群存活
echo "[SERVE] 检查 ray 集群状态..."
ray status || { echo "[SERVE] ERROR: ray 集群不可用，请先执行 ray_start_head.sh + ray_start_worker.sh"; exit 1; }
echo ""

# 启动 vllm serve
LOG_DIR="/data/hy4_running/logs"
LOG_FILE="${LOG_DIR}/hy4-ray-serve-$(date +%Y%m%d-%H%M%S).log"
mkdir -p ${LOG_DIR}

echo "[SERVE] 启动 vllm serve..." | tee -a ${LOG_FILE}
echo "[SERVE] 日志: ${LOG_FILE}" | tee -a ${LOG_FILE}
echo "[SERVE] 启动时间: $(date)" | tee -a ${LOG_FILE}
echo "[SERVE] TP=${TP_SIZE} PP=${PP_SIZE} max_model_len=${MAX_MODEL_LEN}" | tee -a ${LOG_FILE}
echo "[SERVE] 模型: ${MODEL_PATH}" | tee -a ${LOG_FILE}
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
  --max-num-seqs 4 \
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
  "model": "hy4",
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
The model weights are derived from Tencent-Hunyuan/Hy4-preview and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt
