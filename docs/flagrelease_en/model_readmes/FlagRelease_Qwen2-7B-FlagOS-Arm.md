# Introduction

Qwen2-7B-FlagOS-Arm  provides an all-in-one deployment solution, enabling execution of arm-Qwen2-7B on Amazon . As the first-generation release for the Amazon Graviton4 CPUs, this package delivers two key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on Amazon .
3. Consistency Validation:
   - Evaluation tests verifying consistency of results between the official and ours.

# Technical Summary

## Serving Engine

We use FlagScale as the serving engine to improve the portability of distributed inference.

FlagScale is an end-to-end framework for large models across multiple chips, maximizing computational resource efficiency while ensuring model effectiveness. It ensures both ease of use and high performance for users when deploying models across different chip architectures:

- One-Click Service Deployment: FlagScale provides a unified and simple command execution mechanism, allowing users to fast deploy services seamlessly across various hardware platforms using the same command. This significantly reduces the entry barrier and enhances user experience.
- Automated Deployment Optimization: FlagScale automatically optimizes distributed parallel strategies based on the computational capabilities of different AI chips, ensuring optimal resource allocation and efficient utilization, thereby improving overall deployment performance.
- Automatic Operator Library Switching: Leveraging FlagScale's unified Runner mechanism and deep integration with FlagGems, users can seamlessly switch to the FlagGems operator library for inference by simply adding environment variables in the configuration file.

## Triton Support

We validate the execution of arm-Qwen2-7B model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels  to run the arm-Qwen2-7B model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. 

- Also included are Triton kernels from vLLM, such as fused MoE.

# Evaluation Results

## Benchmark Result 

| Metrics            | Qwen2-7B-H100-CUDA | Qwen2-7B-FlagOS-Arm |
|:-------------------|--------------------------|-----------------------------|
| mmlu      |0.700                        | 0.687 |

Qwen2-7B is a pre-o1 model without "thinking" or "reasoning" abilities. We use MMLU instead of AIME or GPQA-diamond to evaluate Qwen2-7B

# How to Run Locally
## 📌 Getting Started
### Download open-source weights

```bash
pip install modelscope
modelscope download --model Qwen/Qwen2-7B-Instruct --local_dir /nfs/Qwen/Qwen2-7B-Instruct
```

### Download the FlagOS image

```bash
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease-arm
```

### Start the inference service

```bash
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
   flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease-arm \
  sleep infinity

docker exec -it flagos bash
```

### Serve

```bash
flagscale serve Qwen2-7B-Instruct
```

# Contributing

We warmly welcome global developers to join us:
1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support

# License

本模型的权重来源于Qwen/Qwen3-4B，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。