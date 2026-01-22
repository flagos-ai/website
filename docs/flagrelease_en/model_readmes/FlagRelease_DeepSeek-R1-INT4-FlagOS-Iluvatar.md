# Introduction

DeepSeek-R1-INT4-FlagOS-Iluvatar  provides an all-in-one deployment solution, enabling execution of DeepSeek-R1-INT4 on Iluvatar GPUs. As the first-generation release for the ILUVATAR, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on ILUVATAR.
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

We validate the execution of DeepSeek-R1-INT4 model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the DeepSeek-R1-INT4 model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

# Introduction

DeepSeek-R1-INT4-FlagOS-Iluvatar  provides an all-in-one deployment solution, enabling execution of DeepSeek-R1-INT4 on Iluvatar GPUs. As the first-generation release for the ILUVATAR-BI150, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on ILUVATAR-BI150.
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

We validate the execution of DeepSeek-R1-INT4 model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the DeepSeek-R1-INT4 model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

# Bundle Download

Requested by Iluvatar, the file of docker image and model files should be applied by email.

|             | Usage                                                  | Cambricon                                                    |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Basic Image | basic software environment that supports model running | services@iluvatar.comContact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |

# Evaluation Results

## Benchmark Result 

| Metrics            | DeepSeek-R1-INT4-H100-CUDA | DeepSeek-R1-INT4-FlagOS-Iluvatar |
|:-------------------|-----------------------|--------------------------|
| GSM8K (EM) | 95.75 | 95.07 |
| MMLU (Acc.) | 85.34 | 85.02 |
| CEVAL | 89.00 | 88.78 |
| AIME 2024 (Pass@1) | 76.67 | 76.67(±0.67) |
| GPQA-Diamond (Pass@1) | 70.20 | 69.7 |
| MATH-500 (pass@1) | 93.20 | 94.2 |


# How to Run Locally
## 📌 Getting Started
### Download open-source weights

```bash

pip install modelscope
modelscope download --model deepseek-ai/DeepSeek-R1 --local_dir /nfs/DeepSeek-R1

```
contact services@iluvatar.comContact to obtain the quanted weights

### Download the FlagOS image

```bash
docker pull baai_v4 
```

### Start the inference service

```bash
docker run --shm-size="32g" -itd -v /dev:/dev -v /usr/src/:/usr/src -v /lib/modules/:/lib/modules -v /home:/home -v /nfs:/nfs -v /mnt/share/:/data1 --privileged --cap-add=ALL --pid=host --net=host --name baai_v4 baai:v4

docker exec -it baai_v4 bash
```

### Download FlagScale and unpatch the vendor's code to build vllm

```bash
git clone https://ghfast.top/https://github.com/FlagOpen/FlagScale.git
cd FlagScale 
git checkout ae85925798358d95050773dfa66680efdb0c2b28
# unpatch 
python3 tools/patch/unpatch.py --device-type bi_V150 --commit-id 758e33e0 --key-path ~/flagscale_0402_key  --dir build
NOTE: need to set git config
# compile vllm
cd build/bi_V150/FlagScale/vllm
bash clean_vllm.sh; bash build_vllm.sh; bash install_vllm.sh
cd ..
```

### Serve

```bash
# config the deepseek-r1-int4 yaml
FlagScale/
├── examples/
│   └── deepseek_r1_int4/
│       └── conf/
│           └── hostfile.txt   #Modify local IP
│           └── config_deepseek_r1_int4.yaml  #Modify container name
│           └── serve/
│               └── deepseek_r1_int4.yaml  # Add batch limit: max-num-seqs: 4

# compile flagscale
pip install .
# start server
flagscale serve deepseek_r1_int4
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

