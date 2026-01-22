# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **Kimi-K2-Instruct-FlagOS** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

### Integrated Deployment

- Deep integration with the open-source [FlagScale framework](https://github.com/FlagOpen/FlagScale)
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS**-A800 container image supporting deployment within minutes

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

| Metrics   | Kimi-K2-Instruct-FlagOS-H100-CUDA | Kimi-K2-Instruct-FlagOS-FlagOS-Nvidia |
| --------- | -------------------------------- | ------------------------------------ |
| AIME-0shot@avg1      | 0.667                            | 0.700                                |
| LiveBench-0shot@avg1 | 0.685                            | 0.690                                |
| MMLUpro-5shots@avg1      | 0.773                            | 0.788                                |
| MUSR-0shot@avg1      | 0.724                            | 0.710                                |

# User Guide

## General Information 

**Environment Setup**

| System Component                | Version Information                  |
| ------------------------------- | ------------------------------------ |
| Docker Version                  | Docker version 24.0.0, build 98fdcd7 |
| Operating System                | Description:    Ubuntu 20.04 LTS     |
| FlagScale                       | Version: 0.8.0                       |
| FlagGems                        | Version: 2.2                         |

## Operation Steps【***need two machines***】

### Download Open-source Model Weights

**Execution under shared storage on master node IP**

```python
pip install modelscope
modelscope download --model moonshotai/Kimi-K2-Instruct --local_dir /share/models/Kimi-K2-Instruct
```

### Download FlagOS Image

**Dual-machine execution**

```python
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_kimi_k2
```

### Start the inference service

**Dual-machine execution**

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
  -v /share/models:/models \
  --gpus all \
  --name flagos \
  harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_kimi_k2 \
  sleep infinity
  
docker exec -it flagos bash
```

### **Modify configuration files**

**Dual-machine execution**---**Edit the `hostfile.txt` file**

Change the IP in hostfile.txt to the corresponding machine's IP

```python
vim /root/miniconda3/envs/flagscale-inference/lib/python3.12/site-packages/flag_scale/examples/kimik2/conf/hostfile.txt
# ip slots type=xxx[optional]
# master node
x.x.x.x slots=8 type=gpu 
# worker nodes
x.x.x.x slots=8 type=gpu
```

**Dual-machine execution**---**Modify the `serve.yaml` file**

```python
vim /root/miniconda3/envs/flagscale-inference/lib/python3.12/site-packages/flag_scale/examples/kimik2/conf/serve.yaml
```

Modify 
```
hostfile: examples/kimik2/conf/hostfile.txt
```
to
```
hostfile: /root/miniconda3/envs/flagscale-inference/lib/python3.12/site-packages/flag_scale/examples/kimik2/conf/hostfile.txt
```

Modify 
```
USE_FLAGGEMS: false
```
to
```
USE_FLAGGEMS: true
```

### **Enter the `flagscale-inference` environment**

**Execution on master node IP**

```python
conda activate flagscale-inference
cd /repos/FlagScale
pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple --no-build-isolation
```

### **Set up passwordless access from the master container to worker host machines**

```python
Write the contents of the ~/.ssh/id_rsa.pub file from the flagos container on the master node into the ~/.ssh/authorized_keys file on the worker nodes' physical machines.
```

### Serve

**Execution on Master Node IP**

```python
flagscale serve kimik2

#After the service starts, you will see output similar to the following:
#INFO 07-08 09:49:51 [api_server.py:1349] Starting vLLM API server 0 on http://0.0.0.0:30000

```

# Service Invocation

## API-based Invocation Script

```
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:30000/v1/"
model = "Kimi-K2-Instruct-nvidia-origin"
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
- Ensure the  model files are present in the `/models` directory inside the container.
- Check the container logs: `docker logs flagos`.

### Q2: API call returns a timeout error. What should I do?

- Verify that the server IP address is correct.
- Check the firewall settings to ensure port 9010 is open.
- Confirm that the service is running properly: `docker exec flagos ps aux | grep flagscale`.

### Q3: When installing vLLM, if you encounter errors. What should I do?

- You need to retry a few times.
- Confirm reachability to GitHub.com and associated endpoints.
- Validate network bandwidth (50MB/s or higher recommended for reliable operation).

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support

# Contact Us

![image](image_.jpeg)

# License

The weights of this model are based on moonshotai/Kimi-K2-Instruct and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.