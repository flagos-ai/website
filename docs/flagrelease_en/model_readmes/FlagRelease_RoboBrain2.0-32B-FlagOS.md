# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **RoboBrain2.0-32B-FlagOS-Nvidia** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

### Integrated Deployment

- Deep integration with the open-source [FlagScale framework](https://github.com/FlagOpen/FlagScale)
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS- H100** container image supporting deployment within minutes

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

| Metrics                  | RoboBrain2.0-32B-H100-CUDA | RoboBrain2.0-32B-FlagOS-Nvidia |
| ------------------------ | -------------------------- | ------------------------------ |
| Where2Place-think        | 69.58                      | 70.25                          |
| Blink-think              | 72.83                      | 70.52                          |
| CVBench-think            | 83.19                      | 83.27                          |
| RoboSpatial-Home-think   | 68.7739                    | 71.4644                        |
| EmbspatialBench-think    | 74.31                      | 73.65                          |
| All-Angles Bench-think   | 50.84                      | 49.44                          |
| VSI-Bench-think          | 42.69                      | 40.43                          |
| SAT-think                | 86.67                      | 85.33                          |
| EgoPlan-Bench2-think     | 51.78                      | 48.83                          |
| ERQA-think               | 44.50                      | 43.00                          |
| Where2Place-nothink      | 73.59                      | 72.58                          |
| Blink-nothink            | 68.35                      | 71.68                          |
| CVBench-nothink          | 83.92                      | 84.19                          |
| RoboSpatial-Home-nothink | 72.4301                    | 71.172                         |
| EmbspatialBench-nothink  | 78.57                      | 78.38                          |
| All-Angles Bench-nothink | 50.14                      | 49.62                          |
| VSI-Bench-nothink        | 39.82                      | 39.72                          |
| SAT-nothink              | 76.67                      | 75.33                          |
| EgoPlan-Bench2-nothink   | 57.23                      | 56.93                          |
| ERQA-nothink             | 40.25                      | 42.00                          |

# 

# User Guide

## General Information 

**Basic Information**

| Type            | Location                                                                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------|
| Model Weights   | https://www.modelscope.cn/models/BAAI/RoboBrain2.0-32B/files                                                                                 |
| Container Image | flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b                                        |

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
modelscope download --model BAAI/RoboBrain2.0-32B --local_dir /share/project/jiyuheng/ckpt/32b_stage2_K1
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
  -v /share:/share \
  --gpus all \
  --name flagos \
  flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b \
  sleep infinity
  
docker exec -it flagos bash
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
model = "RoboBrain2.0-32B-nvidia-flagos"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like today?"}
]
response = openai.chat.completions.create(
    model=model,
    messages=messages,
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
- Ensure the  model files are present in the `/share` directory inside the container.
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

# Contact Us

![image](image_.jpeg)

# License

The weights of this model are based on Qwen/Qwen3-4B and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.