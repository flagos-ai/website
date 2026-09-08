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
- Released **FlagOS-Ascend** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Evaluation Results
## Benchmark Result
| Metrics      | Qwen3.8-Flash-Next-Nvidia-Origin | Qwen3.8-Flash-Next-Ascend-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 92.9                              | 92.8                                   |
| MuSR| 78.57                             | Evaluating                                     |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 20.10.8 |
| Operating System | openEuler 22.03 (LTS-SP4) |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-ascend001-gems5.3.0-tree0.6.0-cx0.13.0-pluginnone-vllmnone-sglang0.5.11-sglangfl0.1.0-cp311-ptnpu28-cann85-a64-25.5.0:202609021230

```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Qwen3.8-Flash-Next-BF16-ascend-FlagOS --local_dir /data/Qwen3.8-Flash-Next
```

### Start the Container
```bash
docker run -dit \
    --name flagos \
    --privileged \
    --init \
    --network=host --ipc=host --shm-size=512g \
    --device=/dev/davinci0 --device=/dev/davinci1 --device=/dev/davinci2 --device=/dev/davinci3 \
    --device=/dev/davinci4 --device=/dev/davinci5 --device=/dev/davinci6 --device=/dev/davinci7 \
    --device=/dev/davinci8 --device=/dev/davinci9 --device=/dev/davinci10 --device=/dev/davinci11 \
    --device=/dev/davinci12 --device=/dev/davinci13 --device=/dev/davinci14 --device=/dev/davinci15 \
    --device=/dev/davinci_manager \
    --device=/dev/hisi_hdc \
    --volume /usr/local/sbin:/usr/local/sbin \
    --volume /usr/local/Ascend/driver:/usr/local/Ascend/driver \
    --volume /usr/local/Ascend/firmware:/usr/local/Ascend/firmware \
    --volume /etc/ascend_install.info:/etc/ascend_install.info \
    --volume /var/queue_schedule:/var/queue_schedule \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/timezone:/etc/timezone:ro \
    -v /data:/data \
    -v /public-flash/models:/models \
    --entrypoint=bash \
    harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-ascend001-gems5.3.0-tree0.6.0-cx0.13.0-pluginnone-vllmnone-sglang0.5.11-sglangfl0.1.0-cp311-ptnpu28-cann85-a64-25.5.0:202609021230 \
    -c "tail -f /dev/null"
docker exec -it flagos /bin/bash
```
### Start the Server
```bash
set -euo pipefail

# 校验并安装优化后的模型代码
cd /opt/qwen38-best/current
sha256sum -c payload.sha256

install -m 0644 payload/qwen4.py \
  /sgl-workspace/sglang/python/sglang/srt/models/qwen4.py

install -m 0644 payload/qwen4_ops.py \
  /sgl-workspace/sglang/python/sglang/srt/models/qwen4_ops.py

install -m 0644 payload/scheduler.py \
  /sgl-workspace/sglang/python/sglang/srt/managers/scheduler.py

# 设备与线程配置
export ASCEND_RT_VISIBLE_DEVICES=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
export OMP_NUM_THREADS=8
export STREAMS_PER_DEVICE=32
export SGLANG_SET_CPU_AFFINITY=1

# 多流与通信配置
export SGLANG_ENABLE_OVERLAP_PLAN_STREAM=1
export SGLANG_NPU_USE_MULTI_STREAM=1
export HCCL_BUFFSIZE=1000
export HCCL_OP_EXPANSION_MODE=AIV
export HCCL_SOCKET_IFNAME=business
export GLOO_SOCKET_IFNAME=business
export FLAGCX_PATH=/sgl-workspace/FlagCX

# 内存与离线配置
export HF_HUB_OFFLINE=1
export PYTORCH_NPU_ALLOC_CONF=expandable_segments:True
export PYTHONPATH="/sgl-workspace/sglang/python:${PYTHONPATH:-}"

# FlagGems 与算子配置
export USE_FLAGGEMS=1
export SGLANG_FL_WATCHDOG_DIAG=1
export SGLANG_FL_PER_OP=mrotary_embedding=reference
export SGLANG_FL_FLAGOS_BLACKLIST='conv1d,conv2d,index,index_put,index_put_,_index_put_impl_,full_like,mul,mul_,sub,sub_,remainder,remainder_,floor_divide,floor_divide_,add,add_,ge,ge_scalar,lt,lt_scalar,bitwise_and_scalar,bitwise_and_scalar_tensor,bitwise_and_tensor,bitwise_and_scalar_,bitwise_and_tensor_,bitwise_not,bitwise_not_,fill_scalar,fill_scalar_out,fill_tensor,fill_tensor_out,fill_scalar_,fill_tensor_,sum,sum_out,sum_dim,sum_dim_out,mean,mean_out,mean_dim,mean_dim_out,max,max_dim,gather,gather_backward,argmax,bincount,where_self,where_self_out,where_scalar_self,where_scalar_other,silu,silu_,silu_backward,bmm,bmm_out'

# Qwen3.8-Flash-Next W8A16 配置
export SGLANG_QWEN4_MOE_W8A16=1
export SGLANG_QWEN4_FORCE_NPU_GMM=1
export SGLANG_QWEN4_STATE_CAPACITY=40000
export SGLANG_QWEN4_ENABLE_NEXTN=0
export SGLANG_QWEN4_MTP_MODE=NEXTN

# 清除可能影响当前最优配置的变量
unset https_proxy http_proxy HTTPS_PROXY HTTP_PROXY
unset ASCEND_LAUNCH_BLOCKING
unset SGLANG_QWEN4_GRAPH_CANARY
unset SGLANG_QWEN4_GRAPH_FIXED_REQ_KEYS
unset SGLANG_QWEN4_GRAPH_INPLACE_STATE
unset SGLANG_QWEN4_GRAPH_MAX_BS
unset SGLANG_QWEN4_NOPLE

# 检查运行环境
python3 -c 'import tbe; print("TBE_IMPORT_OK")'

# 启动服务
exec python3 -m sglang.launch_server \
  --model-path /data/Qwen3.8-Flash-Next/ \
  --served-model-name Qwen3.8-Flash-Next \
  --host 0.0.0.0 \
  --port 30100 \
  --tp-size 4 \
  --dp-size 4 \
  --load-balance-method round_robin \
  --attention-backend ascend \
  --trust-remote-code \
  --reasoning-parser qwen3-thinking \
  --skip-server-warmup \
  --disable-cuda-graph \
  --disable-radix-cache \
  --chunked-prefill-size 8192 \
  --max-prefill-tokens 32768 \
  --prefill-max-requests 4 \
  --max-total-tokens 70000 \
  --max-running-requests 4 \
  --max-mamba-cache-size 4 \
  --watchdog-timeout 900 \
  --mem-fraction-static 0.88
```

## Service Invocation
### Invocation Script
```bash
curl -s http://localhost:30100/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3.8-Flash-Next",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "请用一句话介绍北京。"}
    ],
    "max_tokens": 50,
    "temperature": 0.7
  }' | jq .
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
The model weights are derived from Qwen/Qwen3.8-Flash-Next and are open‑sourced under the Apache License 2.0: https://www.apache.org/licenses/LICENSE-2.0.txt

