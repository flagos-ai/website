# Introduction

DeepSeek-R1-Distill-Qwen-32B-FlagOS-NVIDIA  provides an all-in-one deployment solution, enabling execution of DeepSeek-R1-Distill-Qwen-32B on NVIDIA GPUs. As the first-generation release for the NVIDIA-H100, this package delivers two key features:

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

We validate the execution of DeepSeek-R1-Distill-Qwen-32B model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the DeepSeek-R1-Distill-Qwen-32B model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems).
- Also included are Triton kernels from vLLM.


# Evaluation Results

## Benchmark Result 

| Metrics               | DeepSeek-R1-Distill-Qwen-32B-H100-CUDA | DeepSeek-R1-Distill-Qwen-32B-H100-FlagOS |
| :-------------------- | -------------------------------------- | ---------------------------------------- |
| GSM8K (EM)            | 87.64                                  | 87.79                                    |
| MMLU (Acc.)           | 79.33                                  | 79.35                                    |
| CEVAL                 | 83.43                                  | 83.21                                    |
| AIME 2024 (Pass@1)    | 73.33                                  | 73.33                                    |
| GPQA-Diamond (Pass@1) | 59.60                                  | 59.60                                    |
| MATH-500 pass@1       | 92.80                                  | 92.00                                    |


# How to Run Locally

## 📌 Getting Started

### Download open-source weights

```bash
pip install modelscope
modelscope download --model deepseek-ai/DeepSeek-R1-Distill-Qwen-32B --local_dir /nfs/DeepSeek-R1-Distill-Qwen-32B
```

### Download the FlagOS image

```bash
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia
```

### Start the inference service

```bash
docker run -itd --name flagrelease_nv  --privileged --gpus all --net=host --ipc=host --device=/dev/infiniband --shm-size 512g --ulimit memlock=-1 -v /nfs/DeepSeek-R1-Distill-Qwen-32B:/nfs/DeepSeek-R1-Distill-Qwen-32B flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:deepseek-flagos-nvidia /bin/bash

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
cd FlagScale/examples/deepseek_r1_distill_qwen_32b/conf
# Modify the configuration in config_deepseek_r1_distill_qwen_32b.yaml
defaults:
self
serve: deepseek_r1_distill_qwen_32b
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
  cmds:
    before_start: source /root/miniconda3/bin/activate flagscale-inference && export USE_FLAGGEMS=1
action: run
hydra:
  run:
    dir: ${experiment.exp_dir}/hydra
```

```
cd FlagScale/examples/deepseek_r1_distill_qwen_32b/conf/serve
# Modify the configuration in deepseek_r1_distill_qwen_32b.yaml
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /models/DeepSeek-R1-Distill-Qwen-32B # path of weight of DeepSeek-R1-Distill-Qwen-32B
    served_model_name: deepseek-r1-distill-qwen-32b-flagos
    tensor_parallel_size: 8
    max_model_len: 32768
    pipeline_parallel_size: 1
    max_num_seqs: 256 # Even at full 32,768 context usage, 8 concurrent operations won't trigger OOM
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
flagscale serve deepseek_r1_distill_qwen_32b
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