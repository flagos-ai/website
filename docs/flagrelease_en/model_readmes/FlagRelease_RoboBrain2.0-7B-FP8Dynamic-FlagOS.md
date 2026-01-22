# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **RoboBrain2.0-7B-FP8Dynamic-FlagOS** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

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

| Metrics               | RoboBrain2.0-7B-H100-CUDA | RoboBrain2.0-7B-FP8Dynamic-FlagOS |
| --------------------- | ------------------------- | --------------------------------- |
| SAT                   | 75.330                    | 72.000                            |
| all_angles_bench      | 47.700                    | 46.480                            |
| Where2Place           | 63.590                    | 63.060                            |
| blink_val_ev          | 56.360                    | 55.200                            |
| robo_spatial_home_all | 54.227                    | 54.312                            |
| egoplan_bench2        | 33.230                    | 33.310                            |
| erqa                  | 38.750                    | 39.750                            |
| cv_bench_test         | 85.750                    | 85.770                            |
| embspatial_bench      | 76.320                    | 75.270                            |
| vsi_bench_tiny        | 36.100                    | 38.700                            |

# User Guide

## General Information 

**Environment Setup**

| System Component                | Version Information                   |
| ------------------------------- | ------------------------------------- |
| Accelerator Card Driver Version | Driver Version: 535.183.06            |
| Docker Version                  | Docker version 20.10.5, build 55c4c88 |
| Operating System                | Description:     Ubuntu 22.04.4 LTS   |
| FlagScale                       | Version: 0.8.0                        |
| FlagGems                        | Version: 2.2                          |

## Operation Steps

### Download Open-source Model Weights

```python
pip install modelscope
modelscope download --model FlagRelease/RoboBrain2.0-7B-FP8Dynamic-FlagOS --local_dir /nfs/RoboBrain2.0-7B-FP8Dynamic
```

### Download FlagOS Image

```python
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b
```

### Start the inference service

```
#Container Startup
docker run --rm --init --detach \
  --net=host --uts=host --ipc=host \
  --security-opt=seccomp=unconfined \
  --privileged=true \
  --ulimit stack=67108864 \
  --ulimit memlock=-1 \
  --ulimit nofile=1048576:1048576 \
  --shm-size=32G \
  -v /nfs:/nfs \
  --gpus all \
  --name flagos \
  flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b \
  sleep infinity
  
docker exec -it flagos bash
```

### **Modify configuration files**

```
#Use 'pip show flag_scale' to find the installation path of FlagScale.
pip show flag_scale
# Modify the 7b.yaml file located at flag_scale/examples/robobrain2/conf/serve
set the 【model path】 to /share/RoboBrain2.0-7B-FP8Dynamic
set the 【tensor_parallel_size】 to 4
set the 【served-model-name】 to RoboBrain2-7B-nvidia-flagos-FP8Dynamic
# Modify the serve.yaml file located at flag_scale/examples/robobrain2/conf
Change all the 32b to 7b in it.
```

### Serve

```python
flagscale serve robobrain2

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
model = "RoboBrain2-7B-nvidia-flagos-FP8Dynamic"
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
- Ensure the model files are present in the `/share` directory inside the container.
- Check the container logs: `docker logs flagos`.

### Q2: API call returns a timeout error. What should I do?

- Verify that the server IP address is correct.
- Check the firewall settings to ensure port 9010 is open.
- Confirm that the service is running properly: `docker exec flagos ps aux | grep flagscale`.

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support

# License

本模型以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。