# Before start

We recommend that you refer to https://github.com/FlagOpen/RoboBrain-X0/tree/main if you need to perform model fine-tuning on NVIDIA hardware or deploy the model on physical robots other than AgileX.

# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **RoboBrain-X0-Preview-FlagOS** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

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

Unlike other models, we use the MAPE (Mean Absolute Percentage Error) of the action tensor to evaluate whether the FlagOS version of the model computes correctly. To achieve this, we built upon the standard usage of the RoboBrain-X0 model while controlling the random seeds of the random, numpy, and torch libraries, and configured PyTorch to use deterministic GPU kernels. Additionally, before each inference step, we fix the norm process and sampling parameters to eliminate random completely. In the subsequent usage section, we will provide detailed instructions on how to restore these randomized settings for normal RoboBrain-X0 model operation.
The MAPE between CUDA and FlagOS(CUDA as ground truth) is 2.2994%. You can easily reproduce this result using our image.

# User Guide

**Environment Setup**

| Item | Version          | 
| ------------- | ------------------------------------------------------------ |  
| Docker Version                  | Docker version 28.1.0, build 4d8c241 | 
| Operating System                | Ubuntu 22.04.5 LTS    | 
| FlagScale                       | Version: 0.9.0                        | 
| FlagGems                        | Version: 3.0                          | 

## Operation Steps

### Download Open-source Model Weights

```bash
pip install modelscope
modelscope download --model BAAI/RoboBrain-X0-Preview --local_dir /share/RoboBrain-X0-Preview

```

### Download FlagOS Image

```bash
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_x0_norand
```

### Start the inference service

```bash
#Container Startup
docker run --rm --init --detach   --net=host --uts=host --ipc=host   --security-opt=seccomp=unconfined   --privileged=true   --ulimit stack=67108864   --ulimit memlock=-1   --ulimit nofile=1048576:1048576   --shm-size=32G   -v /share:/share   --gpus all   --name flagos   harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_x0_norand   sleep infinity
```

### Serve

```bash
docker exec -it flagos bash
cd /workspace/RoboBrain-X0/agilex
python server_agilex.py
```

### Call the server

You should start a new SSH session, then execute:
```bash
docker exec -it flagos bash
cd /workspace
python3 client_x0.py --base-img orbbec_0_latest.jpg --left-wrist-img orbbec_1_latest.jpg --right-wrist-img orbbec_2_latest.jpg
```

### Validate the MAPE

If you want to validate the MAPE between CUDA and FlagOS, you can:
1. Restart the container
2. Find /workspace/RoboBrain-X0/agilex/server_agilex.py
3. Use Vim or other editor, comment all lines include "flag_gems"
, then you get x0-CUDA enviroment. Repeat "Serve" and "Call the server", then you get action tensor from CUDA and FlagOS.

### Eliminate the no-rand constrain

1. Find /workspace/RoboBrain-X0/agilex/server_agilex.py
2. Comment line below:
```python
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
```
3. Find the following codes(not contiguous, different lines):
```python
#"repetition_penalty": 1.0, "use_cache": True,
#scale = np.array(action_stats['action.eepose']['scale_'])
#offset = np.array(action_stats['action.eepose']['offset_'])
#delta_actions_denorm = inverse_transform(np.array(delta_actions), scale, offset)
```
4. Undo comments above, but you must use your real stats_file. If you do not possess knowledge about this file, or if you are not planning to deploy this model on a real AgileX robot, then do not perform this processing.
5. Restart the container and then Repeat "Serve" and "Call the server".

### About low-bit precision

1. You can try to load Model in BF16 for lower memory occupancy or quicker inference. But BF16 have only 7 precision bits, which cannnot constrain MAPE under 5% even if you launch two CUDA server on different GPUid on the same GPU server. 


# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support


# License

本模型的权重来源于BAAI/RoboBrain-X0-Preview，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。
