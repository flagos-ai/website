# Introduction

MiniCPM-o 2.6-FlagOS-Cambricon provides an all-in-one deployment solution, enabling execution of MiniCPM-o 2.6 on Cambricon DSAs. As the first-generation release for the Cambricon-MLU series, this package delivers two key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on Cambricon-MLU.
2. Consistency Validation:
   - Evaluation tests verifying consistency of results between NVIDIA H100 and Cambricon-MLU.

# Technical Summary

## Serving Engine

We use FlagScale as the serving engine to improve the portability of distributed inference.

FlagScale is an end-to-end framework for large models across multiple chips, maximizing computational resource efficiency while ensuring model effectiveness. It ensures both ease of use and high performance for users when deploying models across different chip architectures:

- One-Click Service Deployment: FlagScale provides a unified and simple command execution mechanism, allowing users to fast deploy services seamlessly across various hardware platforms using the same command. This significantly reduces the entry barrier and enhances user experience.
- Automated Deployment Optimization: FlagScale automatically optimizes distributed parallel strategies based on the computational capabilities of different AI chips, ensuring optimal resource allocation and efficient utilization, thereby improving overall deployment performance.
- Automatic Operator Library Switching: Leveraging FlagScale's unified Runner mechanism and deep integration with FlagGems, users can seamlessly switch to the FlagGems operator library for inference by simply adding environment variables in the configuration file.

## Triton Support

We validate the execution of MiniCPM-o 2.6 model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the MiniCPM-o 2.6 model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

# Bundle Download

Requested by Cambricon, the file of docker image and model files should be applied by email.

|             | Usage                                                  | Cambricon                                                                                                                                         |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic Image | basic software environment that supports model running | ecosystem@cambricon.com <br> Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |
| Model       | model weight and configuration files                   | ecosystem@cambricon.com <br> Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |

# Evaluation Results
## Benchmark Result 
| Metrics          | MiniCPM-o 2.6-A100-CUDA   | MiniCPM-o 2.6-FlagOS-Cambricon |
|------------------|-------------------------|-----------------------------------|
| mmmu_val       | 48.33                   |  48.33                            |
| math_vision_test      | 22.57                  |  23.12                           |
| ocrbench_test            | 85.4                   |  85                           |
| blink_val| 54.87     |  55.23           |
| mmvet_v2| 59.07  |  57.35         |
| mmmu_pro_vision_test| 24.37  |  23.75              |
| mmmu_pro_standard_test| 30.75  |  30.29              |
| cmmmu_val| 39.11  |  38.56              |
| cii_bench_test| 50.98  |  49.67              |
# How to Run Locally
## 📌 Getting Started
### Environment Setup
```bash
#download ckpt
pip install modelscope 
modelscope download --model AI-ModelScope/MiniCPM-o-2_6 --local_dir /nfs/MiniCPM-o-2_6
# build and enter the container
docker run -e  DISPLAY=$DISPLAY --net=host --pid=host --ipc=host \-v /tmp/.X11-unix:/tmp/.X11-unix \--privileged \-it \-v /share/project:/share/project \-v /home:/home \-v /mnt/:/mnt/ \-v /data/:/data/  \-v /opt/data/:/opt/data/  \-v /usr/bin/cnmon:/usr/bin/cnmon \--name flagrelease_cambricon  \
zhiyuan_vllm:v0.2 /bin/bash
```
### Download and install FlagGems
``` bash
cd <CONTAINER_CKPT_PATH>   #Should be replaced with a custom path
git clone -b deepseek_release_cambricon https://github.com/FlagOpen/FlagGems.git 
cd FlagGems
pip install --index-url https://pypi.org/simple ./ --no-deps
cd ../
```
### Download FlagScale and unpatch the vendor's code to build vllm
```bash
git clone https://github.com/FlagOpen/FlagScale.git 
cd FlagScale
pip install --index-url https://pypi.org/simple ./ --no-deps
pip install cryptography -i https://mirrors.aliyun.com/pypi/simple/
pip install GitPython -i https://pypi.tuna.tsinghua.edu.cn/simple
git config --global user.name "your_name" 
git config --global user.email "your_email"
python tools/patch/unpatch.py --device-type cambricon_MLU --commit-id 57637057 --dir build
cd build/cambricon_MLU/FlagScale/vllm
pip install -e . -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
cd vllm_mlu
pip install -e . -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
cd ../../
```
### Example configuration file reference is as follows
```bash
# config the mini_cpm_o26 yaml
cd FlagScale/build/cambricon_MLU/FlagScale/examples/mini_cpm_o26/conf
# config_mini_cpm_o26.yaml configuration:
vim config_mini_cpm_o26.yaml
defaults:
  - _self_
  - serve: serve_mini_cpm_o26

experiment:
  exp_name: mini_cpm_o26
  exp_dir: outputs/${experiment.exp_name}
  task:
    type: serve
    backend: vllm
    entrypoint: null
  runner:
    hostfile: null
action: run
hydra:
  run:
    dir: ${experiment.exp_dir}/hydra

# serve_mini_cpm_o26.yaml configuration:
vim serve/serve_mini_cpm_o26.yaml
model_args:
  vllm_model:
    model-tag: /nfs/MiniCPM-o-2_6 # path of weight of MiniCPM-o-2_6
    served-model-name: minicpmo26-cambricon-flagos
    tensor-parallel-size: 1
    gpu-memory-utilization: 0.9
    port: 9010
    limit-mm-per-prompt: image=18
    action-args:
      - trust-remote-code
      - enable-chunked-prefill
deploy:
  command_line_mode: true
  models:
    vllm_model:
      num_gpus: 1
```

### Serve

【Verifiable on a single machine】
```bash
# serve
cd build/cambricon_MLU/FlagScale/
pip install .
flagscale serve mini_cpm_o26

curl http://ip:9010/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "minicpmo26-cambricon-flagos",
        "messages": [
        {
            "role": "user",
            "content": "hello"
        }
        ]
    }'
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

