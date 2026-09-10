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
- Released **FlagOS-Nvidia** container image supporting deployment within minutes
### Consistency Validation
- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.	


# Evaluation Results
## Benchmark Result
| Metrics      | Qwen3.8-Flash-Next-Nvidia-Origin | Qwen3.8-Flash-Next-Nvidia-FlagOS |
|--------------|--------------------------------|--------------------------------------|
| GPQA_Diamond | 92.9                             | 91.3                    |
| MuSR         | 78.57                            | Evaluating                                |

# User Guide
Environment Setup

| Item             | Version              |
|------------------|----------------------|
| Docker Version   | Docker version 24.0.0, build 98fdcd7 |
| Operating System | 22.04.4 LTS (Jammy Jellyfish) |

## Operation Steps

### Download FlagOS Image
```bash
docker pull harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-nvidia003-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20:202608262106
```

### Download Open-source Model Weights
```bash
pip install modelscope
modelscope download --model FlagRelease/Qwen3.8-Flash-Next-BF16-nvidia-FlagOS --local_dir /data/Qwen3.8-Flash-Next
```

### Start the Container
```bash
set -euo pipefail
IMAGE_URI='harbor.baai.ac.cn/flagrelease-public/qwen3.8-flash-next-nvidia003-gems5.3.3-tree0.5.0-cxnone-plugin0.3.0-vllm0.24.0-cp312-pt211-cu129-x64-580.126.20:202608262106'
MODEL_DIR='/data/Qwen3.8-Flash-Next'
CONTAINER='qwen38_flash_next_flagos_release'
test -d "$MODEL_DIR"
docker run -d --name "$CONTAINER" --network host --shm-size 64g \
  --device /dev/nvidia0 --device /dev/nvidia1 --device /dev/nvidia2 --device /dev/nvidia3 \
  --device /dev/nvidia4 --device /dev/nvidia5 --device /dev/nvidia6 --device /dev/nvidia7 \
  --device /dev/nvidiactl --device /dev/nvidia-uvm --device /dev/nvidia-uvm-tools \
  --device /dev/nvidia-nvlink --device /dev/nvidia-nvswitch0 --device /dev/nvidia-nvswitch1 \
  --device /dev/nvidia-nvswitch2 --device /dev/nvidia-nvswitch3 --device /dev/nvidia-nvswitchctl \
  --device /dev/nvidia-caps/nvidia-cap0 --device /dev/nvidia-caps/nvidia-cap1 --device /dev/nvidia-caps/nvidia-cap2 \
  -v /usr/lib/x86_64-linux-gnu/libcuda.so.580.126.20:/driver/libcuda.so:ro \
  -v /usr/lib/x86_64-linux-gnu/libcuda.so.580.126.20:/driver/libcuda.so.1:ro \
  -v /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.580.126.20:/driver/libnvidia-ml.so:ro \
  -v /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.580.126.20:/driver/libnvidia-ml.so.1:ro \
  -v /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.580.126.20:/driver/libnvidia-ptxjitcompiler.so:ro \
  -v /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.580.126.20:/driver/libnvidia-ptxjitcompiler.so.1:ro \
  -v "$MODEL_DIR:/models/Qwen3.8-Flash-Next:ro" \
  -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  "$IMAGE_URI" -lc 'exec sleep infinity'
```
### Start the Server
```bash
docker exec -d qwen38_flash_next_flagos_release bash -lc 'export FLAGGEMS_ATEN_PLAN_CACHE=0 VLLM_PLUGINS=fl USE_FLAGGEMS=1 VLLM_FL_PREFER=flagos VLLM_FL_PREFER_ENABLED=true QWEN4_QSA_FUSED_COMPRESS=1 VLLM_WORKER_MULTIPROC_METHOD=spawn VLLM_ENABLE_V1_MULTIPROCESSING=1 VLLM_MOE_USE_DEEP_GEMM=0 VLLM_USE_DEEP_GEMM=0 VLLM_USE_FLASHINFER_MOE_FP8=0 CUDA_DEVICE_ORDER=PCI_BUS_ID OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1; export VLLM_FL_FLAGOS_BLACKLIST=index_put_,index_put,_index_put_impl_,nonzero,copy_,to_copy,index,index_select,conv1d,_conv_depthwise2d,conv2d,pad,constant_pad_nd,mul; export LD_LIBRARY_PATH=/driver:/usr/local/cuda/lib64:${LD_LIBRARY_PATH:-}; exec python3 -m vllm.entrypoints.cli.main serve /models/Qwen3.8-Flash-Next --served-model-name Qwen3.8-Flash-Next --host 0.0.0.0 --port 8001 --tensor-parallel-size 8 --distributed-executor-backend mp --max-model-len 102400 --max-num-seqs 64 --max-num-batched-tokens 32768 --limit-mm-per-prompt '\''{"image":16}'\'' --mm-encoder-tp-mode data --gpu-memory-utilization 0.90 --no-enable-prefix-caching --disable-custom-all-reduce --moe-backend triton --compilation-config '\''{"mode":"NONE","cudagraph_mode":"FULL","cudagraph_capture_sizes":[1,2,4,8,16],"max_cudagraph_capture_size":16,"pass_config":{"fuse_allreduce_rms":false}}'\'' >/tmp/qwen38-flagrelease-server.log 2>&1'
```

## Service Invocation
### Invocation Script
```bash
curl --fail --silent --show-error http://127.0.0.1:8001/health >/dev/null
curl --fail --silent --show-error http://127.0.0.1:8001/v1/chat/completions \
  --header 'Content-Type: application/json' \
  --data-raw '{"model":"Qwen3.8-Flash-Next","messages":[{"role":"user","content":"Reply with exactly: OK"}],"temperature":0,"max_tokens":8}'
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

