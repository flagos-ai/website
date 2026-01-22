# Introduction

DeepSeek-R1-FlagOS-Kunlunxin-INT8  provides an all-in-one deployment solution, enabling execution of DeepSeek-R1 on Kunlunxin GPUs. As the first-generation release for the Kunlunxin, this package delivers two key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on Kunlunxin.
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

We validate the execution of DeepSeek-R1 model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels  to run the DeepSeek-R1 model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. 

- Also included are Triton kernels from vLLM, such as fused MoE.

# Container Image Download

Requested by kunlunxin, the file of docker image and model files should be applied by email.

|             | Usage                                                  | kunlunxin                                                    |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Basic Image | basic software environment that supports model running | [kunlunxin-support@baidu.com](https://www.modelscope.cn/models/FlagRelease/MiniCPM_o_2.6-FlagOS-Cambricon/file/view/master/mailto%3Aecosystem@cambricon.com?status=1) Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |
| Model       | model weight and configuration files                   | [kunlunxin-support@baidu.com](https://www.modelscope.cn/models/FlagRelease/MiniCPM_o_2.6-FlagOS-Cambricon/file/view/master/mailto%3Aecosystem@cambricon.com?status=1) Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |

# Evaluation Results

## Benchmark Result 

| Metrics            | DeepSeek-R1-H100-CUDA | DeepSeek-R1-FlagOS-Kunlunxin-INT8 |
|:-------------------|--------------------------|-----------------------------|
| GSM8K (EM) | 95.75 | 95.38 |
| MMLU (Acc.) | 85.34 | 84.80 |
| CEVAL | 89.00 | 88.86 |
| AIME 2024 (Pass@1) | 23/30 | 23/30 |
| GPQA-Diamond (Pass@1) | 70.20 | 72.73 |
| MATH-500 pass@1 | 93.20 | 94.20 |


# How to Run Locally
## 📌 Getting Started
### Download the FlagOS image

```bash
docker pull iregistry.baidu-int.com/${PROJECT}/${REPO}:${TAG}
```

### Start the inference service

```bash
#Container Name Setting
CONTAINER_NAME=$1
CONTAINER_NAME=${CONTAINER_NAME:Flagrelease-Kunlunxin}
#Image Configuration
readonly PROJECT="xmlir"
readonly REPO="xmlir_ubuntu_2004_x86_64"
readonly TAG=${TAG:Flagrelease-DeepSeek-R1}
#XPU Device Configuration
XPU_NUM=8
DOCKER_DEVICE_CONFIG=" "
if [ $XPU_NUM -gt 0 ]; then
for ((idx=0; idx<=$XPU_NUM-1; idx++)); do
        DOCKER_DEVICE_CONFIG+=" --device=/dev/xpu${idx}:/dev/xpu${idx} "
done
DOCKER_DEVICE_CONFIG+=" --device=/dev/xpuctrl:/dev/xpuctrl "
fi
#Docker run command
docker run -it ${DOCKER_DEVICE_CONFIG}                 \
        --privileged \
        --net=host \
        --uts=host \
        --ipc=host \
        --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
        --tmpfs /dev/shm:rw,nosuid,nodev,exec,size=64g         \
        --cap-add=SYS_PTRACE         \
        -v /ssd1/:/ssd1/             \
        -v /ssd2/:/ssd2/             \
        -v /ssd3/:/ssd3/             \
        -v /ssd4/:/ssd4/             \
        -v /share/:/share/           \
        --name ${CONTAINER_NAME}     \
        -w /workspace \
        -e CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
        -e XPU_FORCE_SHARED_DEVICE_CONTEXT=1    \
        -e BKCL_ENABLE_XDR=1 \
        -e BKCL_USE_RDMA=1   \
        -e BKCL_RDMA_FORCE_TREE=1 \
        -e BKCL_TREE_THRESHOLD=0  \
        -e BKCL_FORCE_L3_RDMA=0   \
        -e BKCL_RDMA_NICS=eth1,eth1,eth2,eth2,eth3,eth3,eth4,eth4 \
        -e BKCL_SOCKET_IFNAME=eth0 \
        -e GLOO_SOCKET_IFNAME=eth0 \
        iregistry.baidu-int.com/${PROJECT}/${REPO}:${TAG} /bin/bash
```

### Serve

【Verifiable on four machine】

```bash
USE_FLAGGEMS=1 GEMS_VENDOR=kunlunxin flagscale serve deepseek_r1
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

This project and related model weights are licensed under the MIT License.
