# Before start

We recommend that you refer to https://github.com/baaivision/Emu3.5 if you need to perform model fine-tuning on NVIDIA hardware or deploy the model on physical robots.

# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **Emu3.5-FlagOS** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

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

Unlike other models, we judge, based on expert experience, that the capability levels demonstrated by CUDA and FlagOS's Emu3.5 are equivalent or not. In the four task domains of visual editing, text-to-image generation, visual guidance, and visual storytelling, a comprehensive judgment is made from multiple aspects including structure, image-text consistency, authenticity, spatial relationships, and style. The two sets of images are consistent in proportions and structure; their color schemes, material details, and texture distributions are similar, but the results from CUDA adhere more closely to real-world logic. Regarding overall painting or rendering styles, such as lighting methods, line characteristics, and detail density, the styles match. In localized precise editing, FlagOS exhibits more stable core features, whereas CUDA excels in maintaining texture and style continuity. Taking all dimensions into account, they can be considered to perform comparably overall.
You can find origin.tar and flagos.tar in the root directory of this model, which contain sample outputs from Emu3.5-CUDA and Emu3.5-FlagOS, respectively, across the four task domains.


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
modelscope download --model FlagRelease/Emu3.5-FlagOS --local_dir /data/Emu3.5-FlagOS

```

### Download FlagOS Image

```bash
docker pull harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_emu3p5
```

### Start the inference service

```bash
#Container Startup
docker run --rm --init --detach   --net=host --uts=host --ipc=host   --security-opt=seccomp=unconfined   --privileged=true   --ulimit stack=67108864   --ulimit memlock=-1   --ulimit nofile=1048576:1048576   --shm-size=32G   -v /data/Emu3.5-FlagOS:/share   --gpus all   --name flagos   harbor.baai.ac.cn/flagrelease-public/flagrelease_nvidia_emu3p5  sleep infinity
```

### Use Emu3.5

```bash
docker exec -it flagos bash
cd /workspace/FlagScale
python run.py --config-path examples/emu3.5/conf/ --config-name image_generation.yaml # to get image_generation results, like text to image
python run.py --config-path examples/emu3.5/conf/ --config-name interleaved_generation.yaml # to get interleaved_generation results, like visual_guidance
```
you can change /workspace/FlagScale/flagscale/inference/emu_utils/prompt_case.py to change the prompts.


# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support


# License

本模型的权重来源于BAAI/Emu3.5，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。
