# Introduction

QwQ-32B-FlagOS-Nvidia provides an all-in-one deployment solution, enabling execution of QwQ-32B on Nvidia GPUs. As the first-generation release for the NVIDIA-H100, this package delivers  two key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on NVIDIA-H100.
2. Consistency Validation:
   - Evaluation tests verifying consistency of results between the official and ours.

# Technical Summary

## Serving Engine

We use FlagScale as the serving engine to improve the portability of distributed inference.

FlagScale is an end-to-end framework for large models across multiple chips, maximizing computational resource efficiency while ensuring model effectiveness. It ensures both ease of use and high performance for users when deploying models across different chip architectures:

- One-Click Service Deployment: FlagScale provides a unified and simple command execution mechanism, allowing users to fast deploy services seamlessly across various hardware platforms using the same command. This significantly reduces the entry barrier and enhances user experience.
- Automated Deployment Optimization: FlagScale automatically optimizes distributed parallel strategies based on the computational capabilities of different AI chips, ensuring optimal resource allocation and efficient utilization, thereby improving overall deployment performance.
- Automatic Operator Library Switching: Leveraging FlagScale's unified Runner mechanism and deep integration with FlagGems, users can seamlessly switch to the FlagGems operator library for inference by simply adding environment variables in the configuration file.

## Triton Support

We validate the execution of QwQ-32B model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the QwQ-32B model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.
- Also included are Triton kernels from vLLM.

# Bundle Download

|             | Usage                                                  | Nvidia                                                       |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Basic Image | basic software environment that supports model running | `docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia` |

# Evaluation Results

## Benchmark Result

| Metrics               | QwQ-32B-H100-CUDA | QwQ-32B-FlagOS-Nvidia |
| :-------------------- | ----------------- | --------------------- |
| GSM8K (EM)            | 72.78             | 73.31                 |
| MMLU (Acc.)           | 79.75             | 79.77                 |
| CEVAL                 | 85.07             | 85.07                 |
| AIME 2024 (Pass@1)    | 80.00             | 76.67                 |
| GPQA-Diamond (Pass@1) | 64.14             | 63.13                 |
| MATH-500 (pass@1)     | 94.20             | 94.00                 |

# How to Run Locally

## 📌 Getting Started

### Download open-source weights

```bash
pip install modelscope
modelscope download --model Qwen/QwQ-32B --local_dir /nfs/QwQ-32B
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
cd FlagScale/examples/qwq_32b/conf
# Modify the configuration in config_qwq_32b.yaml
defaults:
  - _self_
  - serve: qwq_32b
experiment:
  exp_name: qwq_32b
  exp_dir: outputs/${experiment.exp_name}
  task:
    type: serve
  deploy:
    use_fs_serve: false
  runner:
    ssh_port: 22
  envs:
    CUDA_DEVICE_MAX_CONNECTIONS: 1
  cmds:
    before_start: source /root/miniconda3/bin/activate flagscale-inference && export USE_FLAGGEMS=1
action: run
hydra:
  run:
    dir: ${experiment.exp_dir}/hydra
```

```
cd FlagScale/examples/qwq_32b/conf/serve
# Modify the configuration in qwq_32b.yaml
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /nfs/QwQ-32B # path of weight of QwQ-32B
    served_model_name: qwq-32b-flagos
    tensor_parallel_size: 8
    max_model_len: 32768
    pipeline_parallel_size: 1
    max_num_seqs: 256 
    gpu_memory_utilization: 0.9
    port: 9010
    trust_remote_code: true
    enforce_eager: true
    enable_chunked_prefill: true
```

```
# install flagscale
cd FlagScale/
pip install .

#【Verifiable on a single machine】
```

### Serve

```
flagscale serve qwq_32b
```

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

The weights of this model are based on Qwen/QwQ-32B and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.