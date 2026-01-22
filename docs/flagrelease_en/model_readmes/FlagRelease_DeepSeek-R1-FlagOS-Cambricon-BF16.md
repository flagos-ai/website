# Introduction

DeepSeek-R1-FlagOS-Cambricon-BF16 provides an all-in-one deployment solution, enabling execution of DeepSeek-R1 on Cambricon DSAs. As the first-generation release for the Cambricon series, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on Cambricon.
2. High-Precision BF16 Checkpoints:
   - BF16 checkpoints dequantized from the official DeepSeek-R1 FP8 model to ensure enhanced inference accuracy and performance.
3. Consistency Validation:
   - Evaluation tests verifying consistency of results between NVIDIA H100 and Cambricon-MLU590.

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

We provide dequantized model weights in bfloat16 to run DeepSeek-R1 on Cambricon DSAs, along with adapted configuration files and tokenizer.
# Bundle Download

Requested by Cambricon, the file of docker image and model files should be applied by email.

|             | Usage                                                  | Cambricon                                                                                                                                         |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic Image | basic software environment that supports model running | ecosystem@cambricon.com <br> Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |
| Model       | model weight and configuration files                   | ecosystem@cambricon.com <br> Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |

# Evaluation Results
## Benchmark Result 
| Metrics          | DeepSeek-R1-H100-CUDA   | DeepSeek-R1-FlagOS-Cambricon-BF16 |
|------------------|-------------------------|-----------------------------------|
| GSM8K (EM)       | 95.75                   |  95.15                            |
| MMLU (Acc.)      | 85.34                   |  85.61                            |
| CEVAL            | 89.00                   |  89.38                            |
| AIME 2025(Pass@1)| 76.67     |  73.33           |
| GPQA-Diamond (Pass@1)| 70.20  |  73.23         |
| MATH-500 (Pass@1)| 93.20  |  92.60              |
# How to Run Locally
## 📌 Getting Started
### Environment Setup
```bash
# install FlagScale
git clone https://github.com/FlagOpen/FlagScale.git
cd FlagScale
pip install .

# download image and ckpt
flagscale pull --image <IMAGE> --ckpt deepseek-ai/DeepSeek-R1 --ckpt-path /nfs/DeepSeek-R1

# Note: For security reasons, this image does not have passwordless configuration. In multi-machine scenarios, you need to configure passwordless access for the image yourself.

# build and enter the container
docker run -e --net=host --pid=host --ipc=host -v /tmp/.X11-unix:/tmp/.X11-unix --privileged -it -v /nfs:/nfs -v /opt/data/:/opt/data/ -v /usr/bin/cnmon:/usr/bin/cnmon --name flagrelease_cambricon <IMAGE> /bin/bash
```
### Download and install FlagGems
``` bash
git clone https://github.com/FlagOpen/FlagGems.git
cd FlagGems
git checkout deepseek_release_cambricon
# no additional dependencies since they are already handled in the Docker environment
pip install ./ --no-deps
cd ../
```
### Download FlagScale and unpatch the vendor's code to build vllm
```bash
git clone https://github.com/FlagOpen/FlagScale.git
cd FlagScale
git checkout ae85925798358d95050773dfa66680efdb0c2b28
# please set the name and email in git config in advance, for example: git config --global user.name "your_name"; git config --global user.email "your_email"
python tools/patch/unpatch.py --device-type cambricon_MLU --commit-id 57637057 --dir build
cd build/cambricon_MLU/FlagScale/vllm
pip install -e . -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
cd vllm_mlu
pip install -e . -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
cd ../../
```
### Serve
```bash
# config the deepseek_r1 yaml
build/cambricon_MLU/FlagScale/
├── env.sh
├── examples/
│   └── deepseek_r1/
│       └── conf/
│           └── config_deepseek_r1.yaml # set hostfile, env.sh absolute path and ssh_port(optional), if it is passwordless access between containers, the docker field needs to be removed
│           └── serve/
│               └── deepseek_r1.yaml # set model parameters and server port
# install flagscale
pip install .
# serve
flagscale serve deepseek_r1
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
The weights of this model are based on deepseek-ai/DeepSeek-R1 and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.
