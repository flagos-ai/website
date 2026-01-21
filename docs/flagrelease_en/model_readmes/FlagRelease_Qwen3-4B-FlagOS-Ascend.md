# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **Qwen3-4B-FlagOS-Ascend** model is adapted for the Ascend chip using the FlagOS software stack, enabling:

### Integrated Deployment

- Deep integration with the open-source [FlagScale framework](https://github.com/FlagOpen/FlagScale)
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS** container image supporting deployment within minutes

### Consistency Validation

- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Technical Overview

## **FlagScale Distributed Training and Inference Framework**

FlagScale is an end-to-end framework for large models across heterogeneous computing resources, maximizing computational efficiency and ensuring model validity through core technologies. Its key advantages include:

- **Unified Deployment Interface:** Standardized command-line tools support one-click service deployment across multiple hardware platforms, significantly reducing adaptation costs in heterogeneous environments.
- **Intelligent Parallel Optimization:** Automatically generates optimal distributed parallel strategies based on chip computing characteristics, achieving dynamic load balancing of computation/communication resources.
- **Seamless Operator Switching:** Deep integration with the FlagGems operator library allows high-performance operators to be invoked via environment variables without modifying model code.

## **FlagGems Universal Large-Model Operator Library**

FlagGems is a Triton-based, cross-architecture operator library collaboratively developed with industry partners. Its core strengths include:

- **Full-stack Coverage**: Over 100 operators, with a broader range of operator types than competing libraries.
- **Ecosystem Compatibility**: Supports 7 accelerator backends. Ongoing optimizations have significantly improved performance.
- **High Efficiency**: Employs unique code generation and runtime optimization techniques for faster secondary development and better runtime performance compared to alternatives.

## **FlagEval Evaluation Framework**

FlagEval (Libra)** is a comprehensive evaluation system and open platform for large models launched in 2023. It aims to establish scientific, fair, and open benchmarks, methodologies, and tools to help researchers assess model and training algorithm performance. It features:

- **Multi-dimensional Evaluation**: Supports 800+ model evaluations across NLP, CV, Audio, and Multimodal fields, covering 20+ downstream tasks including language understanding and image-text generation.
- **Industry-Grade Use Cases**: Has completed horizontal evaluations of mainstream large models, providing authoritative benchmarks for chip-model performance validation.

# Evaluation Results

## Benchmark Result

| Metrics   | Qwen3-4B-H100-CUDA | Qwen3-4B-FlagOS-Ascend |
| --------- | ------------------ | ---------------------- |
| LIVEBENCH | 0.501              | 0.502                  |
| AIME      | 0.700              | 0.733                  |
| GPQA      | 0.410              | 0.424                  |
| MMLU      | 0.669              | 0.670                  |
| MUSR      | 0.590              | 0.623                  |

# User Guide

## General Information 

**Environment Setup**

| System Component                | Version Information                     |
| ------------------------------- | --------------------------------------- |
| Accelerator Card Driver Version | Version: 25.0.rc1                       |
| Docker Version                  | Docker version 20.10.8, build 3967b7d   |
| Operating System                | PRETTY_NAME="openEuler 22.03 (LTS-SP4)" |
| FlagScale                       | Version: 0.8.0                          |
| FlagGems                        | Version: 2.2                            |

## Operation Steps

### Download Open-source Model Weights

```python
pip install modelscope
modelscope download --model Qwen/Qwen3-4B --local_dir /data/weights/Qwen3-4B/
```

### Download FlagOS Image

```python
#Download the image for the A3 chip
#docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_ascend_qwen3_4b
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease-ascend-release-model_qwen3-4b-tree_none-gems_2.2-scale_0.8.0-cx_none-python_3.11.11-torch_npu2.6.0rc1-pcp_cann8.2rc1.alpha002-gpu_ascend001-arc_arm64-driver_25.2.0:2512101714
#Download the image for the A2 chip
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagopen-910b-ubuntu24.04.2-py311
```

### Start the inference service (A3 chip)

```python
#Container Startup
docker run -itd --name flagos \
    -u root \
    -w /workspace \
    --privileged=true \
    --shm-size=1000g \
    --net=host \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
    -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
    -v /usr/local/dcmi:/usr/local/dcmi \
    -v /usr/local/sbin:/usr/local/sbin \
    -v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime \
    -v /etc/ascend_install.info:/etc/ascend_install.info \
    -v /data:/data \
    -v /root/.cache:/root/.cache \
    -e VLLM_USE_V1=1 \
    -e CPU_AFFINITY_CONF=2 \
    -e PYTORCH_NPU_ALLOC_CONF=max_split_size_mb:256 \
    -e USE_FLAGGEMS=true \
  flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_ascend_qwen3_4b bash

#Enter the container
docker exec -it flagos bash

#Special configuration is required
source /usr/local/Ascend/ascend-toolkit/set_env.sh && source /usr/local/Ascend/nnal/atb/set_env.sh

#Use 'pip show flag_scale' to find the installation path of FlagScale.
pip show flag_scale

# Modify the 4b.yaml file located at flag_scale/examples/qwen3/conf/serve
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /data/weights/Qwen3-4B/ # path of weight of Qwen3-4B
    served_model_name: Qwen3-4B-ascend-flagos
    tensor_parallel_size: 1
    gpu_memory_utilization: 0.8
    host: x.x.x.xxx  #Modify the host field in the 4b.yaml configuration file to use the machine's actual IP address.
    port: 9010
    block_size: 128
    max_model_len: 35536
    max_num_seqs: 16
    enforce_eager: true
    no_enable_prefix_caching: true
    no_enable_chunked_prefill: true

```

### Serve(A3 chip)

```python
flagscale serve qwen3

#After the service starts, you will see output similar to the following:
#INFO:     Started server process [392]
#INFO:     Waiting for application startup.
#INFO:     Application startup complete.
```

### Start the inference service (A2 chip)

```python
#Container Startup
docker run -itd --name gems_test \
    -u root \
    -w /workspace \
    --privileged=true \
    --shm-size=1000g \
    --net=host \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
    -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
    -v /usr/local/dcmi:/usr/local/dcmi \
    -v /usr/local/sbin:/usr/local/sbin \
    -v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime \
    -v /etc/ascend_install.info:/etc/ascend_install.info \
    -v /data:/data \
    -v /root/.cache:/root/.cache \
    -e VLLM_USE_V1=1 \
    -e CPU_AFFINITY_CONF=2 \
    -e PYTORCH_NPU_ALLOC_CONF=max_split_size_mb:256 \
    -e USE_FLAGGEMS=true \
    -e ASCEND_RT_VISIBLE_DEVICES=7 \
    flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagopen-910b-ubuntu24.04.2-py311 bash

#Enter the container
docker exec -it flagos bash

#Special configuration is required
source /usr/local/Ascend/ascend-toolkit/set_env.sh 
source /usr/local/Ascend/nnal/atb/set_env.sh

#Use 'pip show flag_scale' to find the installation path of FlagScale.
pip show flag_scale

# Modify the 4b.yaml file located at flag_scale/examples/qwen3/conf/serve to match the changes made for the A3 chip.

```

### Serve(A2 chip)

```python
#Start the vLLM service with FlagScale
flagscale serve qwen3 /workspace/FlagScale/examples/qwen3/conf/serve.yaml

#After the service starts, you will see output similar to the following:
#INFO:     Started server process [392]
#INFO:     Waiting for application startup.
#INFO:     Application startup complete.
```



# Service Invocation

## API-based Invocation Script

```
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:9010/v1/"
model = "Qwen3-4B-ascend-flagos"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like today?"}
]
response = openai.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.7,
    top_p=0.95,
    stream=False,
)
for item in response:
    print(item)
```

## AnythingLLM Integration Guide

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

# Frequently Asked Questions

### Q1: What should I do if the model fails to load?

- Check if the model weight path is correct.
- Ensure the Qwen3-4B model files are present in the `/share` directory inside the container.
- Check the container logs: `docker logs flagos`.

### Q2: API call returns a timeout error. What should I do?

- Verify that the server IP address is correct.
- Check the firewall settings to ensure port 9010 is open.
- Confirm that the service is running properly: `docker exec flagos ps aux | grep flagscale`.

### Q3: IP **errors**

- Modify the 4b.yaml file located at flag_scale/examples/qwen3/conf/serve
![ip](ip.jpg)

### Q4: The application experiences freezing issues during operation [limited to A2 chips only]

- *You may attempt to explicitly turn off PD fusion and prefix caching* 

 ![p2](p2.jpeg) 

# 

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support


# License

本模型的权重来源于Qwen/Qwen3-4B，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。