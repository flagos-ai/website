# Introduction

DeepSeek-R1-Distill-Qwen-32B-FlagOS-Cambricon  provides an all-in-one deployment solution, enabling execution of DeepSeek-R1-Distill-Qwen-32B on Cambricon GPUs. As the first-generation release for the Cambricon-MLU, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on Cambricon.
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

We validate the execution of DeepSeek-R1-Distill-Qwen-32B model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the DeepSeek-R1-Distill-Qwen-32B model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. For more details, please refer to the "How to Run Locally" section.

- Also included are Triton kernels from vLLM, including fused MoE.

# Bundle Download
Requested by Cambricon, the file of docker image and model files should be applied by email.
            
|             | Usage                                                  | Cambricon                                                                                                                             |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| Basic Image | basic software environment that supports model running | ecosystem@cambricon.com <br> Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |
| Model       | model weight and configuration files                   | ecosystem@cambricon.com <br> Contact by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |
# Evaluation Results

## Benchmark Result 

| Metrics            | DeepSeek-R1-Distill-Qwen-32B-H100-CUDA | DeepSeek-R1-Distill-Qwen-32B-FlagOS-Cambricon |
|:-------------------|-----------------------|--------------------------|
| GSM8K (EM) | 87.64 | 86.81 |
| MMLU (Acc.) | 79.33 | 79.45 |
| CEVAL | 83.43 | 83.43 |
| AIME 2024 (Pass@1) | 73.33 | 70.00 |
| GPQA-Diamond (Pass@1) | 59.60 | 64.65 |
| MATH-500 (pass@1) | 92.80 | 93.40 |


# How to Run Locally
## 📌 Getting Started
### Environment Setup

```bash
#download ckpt
pip install modelscope 
modelscope download --model deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --local_dir /nfs/DeepSeek-R1-Distill-Qwen-32B
# build and enter the container
docker run -e  DISPLAY=$DISPLAY --net=host --pid=host --ipc=host \-v /tmp/.X11-unix:/tmp/.X11-unix \--privileged \-it \-v /nfs/DeepSeek-R1-Distill-Qwen-32B:/nfs/DeepSeek-R1-Distill-Qwen-32B \-v /home:/home \-v /mnt/:/mnt/ \-v /data/:/data/  \-v /opt/data/:/opt/data/  \-v /usr/bin/cnmon:/usr/bin/cnmon \--name flagrelease_cambricon  \
zhiyuan_vllm:v0.2 /bin/bash

```


### Download and install FlagGems

```bash

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
# config the deepseek_r1_distill_qwen_32b yaml
cd FlagScale/build/cambricon_MLU/FlagScale/examples/qwq_32b/conf
# config_deepseek_r1_distill_qwen_32b.yaml configuration:
vim config_deepseek_r1_distill_qwen_32b.yaml
defaults:
  - _self_
  - serve: serve_deepseek_r1_distill_qwen_32b
experiment:
  exp_name: deepseek_r1_distill_qwen_32b
  exp_dir: outputs/${experiment.exp_name}
  task:
    type: serve
  deploy:
    use_fs_serve: false
  runner:
    ssh_port: 22
  envs:
    CUDA_DEVICE_MAX_CONNECTIONS: 1
action: run
hydra:
  run:
    dir: ${experiment.exp_dir}/hydra

# serve_deepseek_r1_distill_qwen_32b.yaml configuration:
vim serve/serve_deepseek_r1_distill_qwen_32b.yaml
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /share/DeepSeek-R1-Distill-Qwen-32B # should be customized
    served_model_name: deepseek-r1-distill-qwen-32b-flagos
    tensor_parallel_size: 8
    max_model_len: 32768
    pipeline_parallel_size: 1
    max_num_seqs: 8 # Even at full 32,768 context usage, 8 concurrent operations won't trigger OOM
    gpu_memory_utilization: 0.9
    port: 9010
    trust_remote_code: true
    enforce_eager: true
    enable_chunked_prefill: true
```

### Serve
【Verifiable on a single machine】
```bash
# serve
cd build/cambricon_MLU/FlagScale/
pip install .
flagscale serve deepseek-r1-distill-qwen-32b-flagos

curl http://ip:9010/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "deepseek-r1-distill-qwen-32b-flagos",
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

The weights of this model are based on deepseek-ai/DeepSeek-R1-Distill-Qwen-32B and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.
