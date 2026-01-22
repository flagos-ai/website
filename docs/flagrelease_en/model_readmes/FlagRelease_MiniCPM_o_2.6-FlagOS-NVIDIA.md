# Introduction

MiniCPM_o_2.6-FlagOS-NVIDIA  provides an all-in-one deployment solution, enabling execution of MiniCPM_o_2.6 on NVIDIA GPUs. As the first-generation release for the NVIDIA-H100, this package delivers three key features:

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

We validate the execution of DeepSeed-R1 model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the MiniCPM_o_2.6 model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

# Evaluation Results

## Benchmark Result 

| Metrics                | MiniCPM_o_2.6-H100-CUDA | MiniCPM_o_2.6-H100-FlagOS |
| :--------------------- | ----------------------- | ------------------------- |
| mmmu_val               | 48.11                   | 48.33                     |
| math_vision_test       | 22.89                   | 22.30                     |
| ocrbench_test          | 85.80                   | 85.70                     |
| blink_val              | 54.87                   | 55.81                     |
| mmmvet_v2              | 57.66                   | 59.03                     |
| mmmu_pro_vision_test   | 24.37                   | 25.32                     |
| mmmu_pro_standard_test | 30.46                   | 30.81                     |
| cmmmu_val              | 39.33                   | 39.33                     |
| cii_bench_test         | 50.07                   | 50.33                     |


# How to Run Locally

## 📌 Getting Started

### Environment Setup

```bash
# install FlagScale
git clone https://github.com/FlagOpen/FlagScale.git
cd FlagScale
pip install .

# download image and ckpt
flagscale pull --image docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia --ckpt https://www.modelscope.cn/models/FlagRelease/MiniCPM_o_2.6-FlagOS-Nvidia.git --ckpt-path /nfs/MiniCPM_o_2.6

# Note: For security reasons, this image does not have passwordless configuration. In multi-machine scenarios, you need to configure passwordless access for the image yourself.

# build and enter the container
docker run -itd --name flagrelease_nv --privileged --gpus all --net=host --ipc=host --device=/dev/infiniband  --shm-size 512g --ulimit memlock=-1 -v /nfs:/nfs flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia /bin/bash
docker exec -it flagrelease_nv /bin/bash

conda activate flagscale-inference
```


### Download and install FlagGems

```bash
git clone https://github.com/FlagOpen/FlagGems.git
cd FlagGems
pip install ./ --no-deps
cd ../
```

### Download FlagScale and build vllm 

```bash
git clone https://github.com/FlagOpen/FlagScale.git
cd FlagScale/
git checkout ae85925798358d95050773dfa66680efdb0c2b28
cd vllm
pip install .
cd ../
```

### Serve

```bash
# config the minicpm_o_2.6 yaml

FlagScale/
├── examples/
│   └── minicpm_o_2.6/
│       └── conf/
│           └── config_minicpm_o_2.6.yaml # set hostfile and ssh_port(optional), if it is passwordless access between containers, the docker field needs to be removed
│           └── serve/
│               └── minicpm_o_2.6.yaml # set model parameters and server port

# install flagscale
pip install .

# serve
flagscale serve minicpm_o_2.6
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

The weights of this model are based on OpenBMB/MiniCPM-o-2_6 and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.