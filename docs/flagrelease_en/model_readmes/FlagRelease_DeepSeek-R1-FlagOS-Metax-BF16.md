# Introduction

DeepSeek-R1-FlagOS-Metax-BF16 provides an all-in-one deployment solution, enabling execution of DeepSeek-R1 on Metax GPUs. As the first-generation release for the Metax series, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Verified model files, available on Hugging Face ([Model Link](https://huggingface.co/FlagRelease/DeepSeek-R1-FlagOS-Metax-BF16)).
   - Pre-built Docker image for rapid deployment on Metax.
2. High-Precision BF16 Checkpoints:
   - BF16 checkpoints dequantized from the official DeepSeek-R1 FP8 model to ensure enhanced inference accuracy and performance.
3. Consistency Validation:
   - Evaluation tests verifying consistency of results between NVIDIA H100 and Metax.

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

- Most Triton kernels are provided by FlagGems (GitHub - FlagOpen/FlagGems: FlagGems is an operator library for large language models implemented in). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

## BF16 Dequantization

We provide dequantized model weights in bfloat16 to run DeepSeek-R1 on Metax GPUs, along with adapted configuration files and tokenizer.

# Bundle Download

|             | Usage                                                  | Metax                                                                                                       |
| ----------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| Basic Image | basic software environment that supports model running | `docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-metax` |
| Model       | model weight and configuration files                   | https://www.modelscope.cn/models/FlagRelease/DeepSeek-R1-FlagOS-Metax-BF16                                  |

# Evaluation Results

## Benchmark Result 

| Metrics            | DeepSeek-R1-H100-CUDA   | DeepSeek-R1-FlagOS-Metax-BF16 |
|--------------------|-------------------------|-------------------------------|
| GSM8K (EM)         | 95.75                   |  95.38                        |
| MMLU (Acc.)        | 85.34                   |  85.38                        |
| CEVAL              | 89.00                   |  89.23                        |
| AIME 2024 (Pass@1) | 76.67                   |  76.67                          | 
| GPQA-Diamond (Pass@1) | 70.20                |  71.72                        | 
| AIME 2024 (Pass@1) | 93.20      |  93.80           | 

# How to Run Locally
## 📌 Getting Started
### Environment Setup

```bash
# install FlagScale
git clone https://github.com/FlagOpen/FlagScale.git
cd FlagScale
pip install .

# download image and ckpt
flagscale pull --image flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-metax --ckpt https://www.modelscope.cn/FlagRelease/DeepSeek-R1-FlagOS-Metax-BF16.git --ckpt-path <CKPT_PATH>

# Note: For security reasons, this image does not have passwordless configuration. In multi-machine scenarios, you need to configure passwordless access for the image yourself.

# build and enter the container
docker run -it --device=/dev/dri --device=/dev/mxcd --group-add video --name flagrelease_metax --device=/dev/mem --network=host --security-opt seccomp=unconfined --security-opt apparmor=unconfined --shm-size '100gb' --ulimit memlock=-1 -v /usr/local/:/usr/local/ -v <CKPT_PATH>:<CKPT_PATH> flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-metax /bin/bash
```

### Download and install FlagGems

```bash 
git clone https://github.com/FlagOpen/FlagGems.git
cd FlagGems
git checkout deepseek_release_metax
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
python tools/patch/unpatch.py --device-type metax_C550 --commit-id 57637057  --dir build
cd build/metax_C550/FlagScale/vllm
source env.sh 
python setup.py bdist_wheel
cd ../
```

### Serve

```bash
# config the deepseek_r1 yaml
build/metax_C550/FlagScale/
├── examples/
│   └── deepseek_r1/
│       └── conf/
│           └── config_deepseek_r1.yaml # set hostfile and ssh_port(optional), if it is passwordless access between containers, the docker field needs to be removed
│           └── serve/
│               └── deepseek_r1.yaml # set model parameters and server port

# install flagscale
pip install .

# serve
flagscale serve deepseek_r1
```

# Usage Recommendations
When custom service parameters, users can run:

```bash
flagscale serve <MODEL_NAME> <MODEL_CONFIG_YAML>
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

<p style="color: lightgrey;">如果您是本模型的贡献者，我们邀请您根据<a href="https://modelscope.cn/docs/ModelScope%E6%A8%A1%E5%9E%8B%E6%8E%A5%E5%85%A5%E6%B5%81%E7%A8%8B%E6%A6%82%E8%A7%88" style="color: lightgrey; text-decoration: underline;">模型贡献文档</a>，及时完善模型卡片内容。</p>


# Initial installation steps：

## 📌 Getting Started

### Environment Setup

```bash
# Download checkpoint
pip install modelscope  
modelscope download --model FlagRelease/DeepSeek-R1-FlagOS-Metax-BF16 --local_dir <Download URL> 

# build and enter the container 【Perform this operation on four machines】
docker run -it --device=/dev/dri --device=/dev/mxcd --group-add video --name flagrelease_metax --device=/dev/mem --network=host --security-opt seccomp=unconfined --security-opt apparmor=unconfined --shm-size '100gb' --ulimit memlock=-1 -v /usr/local/:/usr/local/ -v <CKPT_PATH>:<CKPT_PATH> flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-metax /bin/bash  
```

### Modify the `config.json` for Deepseek-R1-671b

```
# Locate and remove the following JSON configuration:
"quantization_config": {  
  "activation_scheme": "dynamic",  
  "fmt": "e4m3",  
  "quant_method": "fp8",  
  "weight_block_size": [  
    128,  
    128  
  ]  
},  
```

### Configure environment variables

```
# Create an ‘env.sh’ file with:
export GLOO_SOCKET_IF_NAME=ens20np0  # Note: The value of GLOO_SOCKET_IF_NAME should be the network interface name for inter-machine communication. Use `ifconfig` to check network interfaces.  
export VLLM_LOGGING_LEVEL=DEBUG  
export VLLM_PP_LAYER_PARTITION=16,15,15,15  
export MACA_SMALL_PAGESIZE_ENABLE=1  
source env.sh  
```

### Start Ray Cluster

```
# On the **main node** (first machine), run:
ray start --head --num-gpus=8  

# On **other nodes**, execute `ray start --address='<main_node_ip:port>'` (use the IP and port displayed by the main node).
# After all nodes start Ray, run `ray status` on the main node. Ensure **32 GPUs** are recognized.
# Note: If environment variables are modified, restart Ray on all nodes (`ray stop`). Stop worker nodes first, then the main node.
```

### Serve

```bash
# On the main node:
vllm serve /nfs/deepseek_r1_BF16 -pp 4 -tp 8 --trust-remote-code --distributed-executor-backend ray --dtype bfloat16 --max-model-len 4096 --swap-space 16 --gpu-memory-utilization 0.90  
# Once the model loads fully, use the API for inference.**Test with ‘client.py’**

```

 `client.py` 

```bash
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "<model path>",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    }'
```

# 