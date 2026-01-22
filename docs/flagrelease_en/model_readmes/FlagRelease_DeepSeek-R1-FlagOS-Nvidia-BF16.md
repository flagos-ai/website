# Introduction

DeepSeek-R1-FlagOS-NVIDIA-BF16 provides an all-in-one deployment solution, enabling execution of DeepSeek-R1 on Nvidia GPUs. As the first-generation release for the NVIDIA-H100 series, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Verified model files, available on Hugging Face ([Model Link](https://huggingface.co/FlagRelease/DeepSeek-R1-FlagOS-Nvidia-BF16)).
   - Pre-built Docker image for rapid deployment on NVIDIA-H100.
2. High-Precision BF16 Checkpoints:
   - BF16 checkpoints dequantized from the official DeepSeek-R1 FP8 model to ensure enhanced inference accuracy and performance.
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

We validate the execution of DeepSeed-R1 model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the DeepSeek-R1 model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

## BF16 Dequantization

We provide dequantized model weights in bfloat16 to run DeepSeek-R1 on NVIDIA GPUs, along with adapted configuration files and tokenizer.

# Bundle Download

|             | Usage                                                  | Nvidia                                                       |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Basic Image | basic software environment that supports model running | `docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia` |
| Model       | model weight and configuration files                   | https://www.modelscope.cn/models/FlagRelease/DeepSeek-R1-FlagOS-Nvidia-BF16 |

# Evaluation Results

## Benchmark Result 

| Metrics               | DeepSeek-R1-H100-CUDA | DeepSeek-R1-H100-FlagOS |
| --------------------- | --------------------- | ----------------------- |
| GSM8K (EM)            | 95.75                 | 95.83                   |
| MMLU (Acc.)           | 85.34                 | 85.56                   |
| CEVAL                 | 89.00                 | 89.60                   |
| AIME 2024 (Pass@1)    | 76.67                 | 70.00                   |
| GPQA-Diamond (Pass@1) | 70.20                 | 71.21                   |
| MATH-500 (Pass@1)     | 93.20                 | 94.80                   |
| MMLU-Pro (Acc.)       | TBD                   | TBD                     |


# How to Run Locally

## 📌 Getting Started

### Download open-source weights

```bash
pip install modelscope
modelscope download --model deepseek-ai/DeepSeek-R1 --local_dir /nfs/DeepSeek-R1
```

### Download the FlagOS image

```bash
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia
```

### Start the inference service

```bash
docker run -itd --name flagrelease_nv  --privileged --gpus all --net=host --ipc=host --device=/dev/infiniband --shm-size 512g --ulimit memlock=-1 -v /nfs:/nfs flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia /bin/bash

docker exec -it flagrelease_nv /bin/bash

conda activate flagscale-inference
```

### Download and install FlagGems

```
git clone https://github.com/FlagOpen/FlagGems.git
cd FlagGems
pip install .
cd ../
```

### Modify the configuration

```bash
cd FlagScale/examples/deepseek_r1/conf
# Modify the configuration in config_deepseek_r1.yaml
defaults:
  - _self_
  - serve: deepseek_r1
experiment:
  exp_name: deepseek_r1
  exp_dir: outputs/${experiment.exp_name}
  task:
    type: serve
  deploy:
    use_fs_serve: false
  runner:
    hostfile: examples/deepseek_r1/conf/hostfile.txt  # set hostfile
    docker: flagrelease_nv # set docker
    ssh_port: 22
  envs:
    CUDA_DEVICE_MAX_CONNECTIONS: 1
  cmds:
    before_start: source /root/miniconda3/bin/activate flagscale-inference && export GLOO_SOCKET_IFNAME=bond0 && export USE_FLAGGEMS=1 # The environment variable GLOO_SOCKET_IF_NAME must be set to the name of the network interface (e.g., eth0, enp0s3) corresponding to the subnet used for inter-machine communication. You can check interface details (IP addresses, names) using the ifconfig command.
action: run
hydra:
  run:
    dir: ${experiment.exp_dir}/hydra
```

```
cd FlagScale/examples/deepseek_r1/conf
# Modify the configuration in hostfile.txt
# ip slots type=xxx[optional]
# master node
x.x.x.x slots=8 type=gpu
# worker nodes
x.x.x.x slots=8 type=gpu
```

```
cd FlagScale/examples/deepseek_r1/conf/serve
# Modify the configuration in deepseek_r1.yaml
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /nfs/deepseek_r1 # path of weight of deepseek r1
    tensor_parallel_size: 8
    pipeline_parallel_size: 4
    gpu_memory_utilization: 0.9
    max_model_len: 32768
    max_num_seqs: 256
    enforce_eager: true
    trust_remote_code: true
    enable_chunked_prefill: true
```

```
# install flagscale
cd FlagScale/
pip install .
# Configure passwordless container access by adding its key to other hosts. [Requires activation using four machines]
```

### Serve

```
flagscale serve deepseek_r1
```

# 

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support

# 📞 Contact Us

Scan the QR code below to add our WeChat group
send "FlagRelease"

![WeChat](image/group.png)

# License

The weights of this model are based on deepseek-ai/DeepSeek-R1 and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.