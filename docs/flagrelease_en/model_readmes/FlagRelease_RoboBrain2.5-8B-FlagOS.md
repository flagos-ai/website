# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **RoboBrain2.5-8B-FlagOS** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

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

| Metrics           | RoboBrain2.5-8B-CUDA | RoboBrain2.5-8B-FlagOS |
|-------------------|--------------------------|-----------------------------|
| erqa | 41.250 | 38.600 |
| Where2Place | 1.220 | 0.110 |
| blink_val_ev | 78.180 | 77.600 |
| cv_bench_test | 87.490 | 86.470 |
| embspatial_bench | 75.910 | 75.800 |
| SAT | 69.330 | 68.670 |
| vsi_bench_tiny | 38.340 | 37.500 |
| robo_spatial_home_all | 49.429 | 51.714 |
| all_angles_bench | 48.360 | 47.940 |
| egoplan_bench2 | 49.050 | 48.450 |
| EmbodiedVerse-Open-Sampled | 44.320 | 44.340 |
| ERQAPlus | 21.880 | 20.620 |

# User Guide

**Environment Setup**

| Accelerator Card Driver Version | Driver Version: 570.158.01          |
| ------------------------------- | ----------------------------------- |
| CUDA SDK Build                  | Build cuda_13.0.r13.0/compiler.36424714_0 |
| FlagTree                        | Version: 0.4.0+3.5                  |
| FlagGems                        | Version: 4.2.0                      |
| VLLM-FL                         | Version: 0.0.0                      |

## Operation Steps

### Download Open-source Model Weights

```bash
pip install modelscope
modelscope download --model FlagRelease/RoboBrain2.5-8B-FlagOS --local_dir /share/RoboBrain2.5-8B-NV
```

### Download FlagOS Image

```bash
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease-nvidia-release-model_robo25-tree_0.4.03.5-gems_4.2.0-vllmpluginfl_0.0.0-cx_none-python_3.12.3-torch_2.9.0-pip_cuda13.0-gpu_nvidia003-arc_amd64-driver_570.158.01
```

### Start the inference service

```bash
#Container Startup
docker run --init --detach --net=host --user 0 --ipc=host \
           -v /share:/share --security-opt=seccomp=unconfined \
           --privileged --ulimit=stack=67108864 --ulimit=memlock=-1 \
           --shm-size=512G --gpus all -e USE_FLAGGEMS=1 \
           --name flagos harbor.baai.ac.cn/flagrelease-public/flagrelease-nvidia-release-model_robo25-tree_0.4.03.5-gems_4.2.0-vllmpluginfl_0.0.0-cx_none-python_3.12.3-torch_2.9.0-pip_cuda13.0-gpu_nvidia003-arc_amd64-driver_570.158.01 sleep infinity
```

### Serve

```bash
docker exec -it flagos bash
vllm serve /share/RoboBrain2.5-8B-NV --port 9010 --served-model-name RoboBrain2.5-8B-nvidia-flagos
```


## Service Invocation

### API-based Invocation Script

```bash
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:9010/v1/"
model = "RoboBrain2.5-8B-nvidia-flagos"
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

本模型的权重来源于BAAI/RoboBrain2.5-8B-NV，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。