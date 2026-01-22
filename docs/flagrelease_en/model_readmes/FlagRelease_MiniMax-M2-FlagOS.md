# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **MiniMax-M2-FlagOS** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

### Integrated Deployment

- Deep integration with the open-source [FlagScale framework](https://github.com/FlagOpen/FlagScale)
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS-Nvidia** container image supporting deployment within minutes

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

| Metrics           | MiniMax-M2-H100-CUDA | MiniMax-M2-FlagOS |
|-------------------|--------------------------|-----------------------------|
| AIME_0fewshot_@avg1 | 43.330 | 50.000 |
| GPQA_0fewshot_@avg1 | 64.260 | 65.180 |
| LiveBench-0fewshot_@avg1 | 46.010 | 45.660 |
| MMLU_5fewshot_@avg1 | 77.750 | 77.930 |
| MUSR_0fewshot_@avg | 67.590 | 65.870 |

# User Guide

**Environment Setup**

| Accelerator Card Driver Version | Kernel Mode Driver Version: 2.3.0          | 
| ------------- | ------------------------------------------------------------ |  
| Docker Version                  | Docker version 27.5.1, build 27.5.1-0ubuntu3~22.04.2| 
| Operating System                | Description:    Ubuntu 22.04.4 LTS     | 
| FlagScale                       | Version: 0.8.0                        | 
| FlagGems                        | Version: 3.0                         | 

## Operation Steps

### Download Open-source Model Weights

```bash
pip install modelscope
modelscope download --model FlagRelease/MiniMax-M2-FlagOS --local_dir /share/MiniMax-M2

```

### Download FlagOS Image

```bash
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_minimaxm2
```

### Start the inference service

```bash
#Container Startup
docker run --init --detach --net=host --user 0 --ipc=host \
           -v /share:/share --security-opt=seccomp=unconfined \
           --privileged --ulimit=stack=67108864 --ulimit=memlock=-1 \
           --shm-size=512G --gpus all -e USE_FLAGGEMS=1 \
           --name flagos harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_minimaxm2 sleep infinity
```

### Serve

```bash
source .venv/bin/activate
flagscale serve minimax

```


## Service Invocation

### API-based Invocation Script

```bash
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:9010/v1/"
model = "MiniMax-M2-nvidia-flagos"
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

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support


# License

本模型的权重来源于MiniMax/MiniMax-M2，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。