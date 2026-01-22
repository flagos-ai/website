# Introduction

Qwen2.5-VL-32B-Instruct-FlagOS-Nvidia  provides an all-in-one deployment solution, enabling execution of Qwen2.5-VL-32B-Instruct on Nvidia GPUs. As the first-generation release for the NVIDIA-H100, this package delivers two key features:

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

We validate the execution of Qwen2.5-VL-32B-Instruct model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels—approximately 70%—to run the Qwen2.5-VL-32B-Instruct model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). 
- Also included are Triton kernels from vLLM


# Evaluation Results

## Benchmark Result 

| Metrics            | Qwen2.5-VL-32B-Instruct-H100-CUDA | Qwen2.5-VL-32B-Instruct-H100-Flagos |
|:-------------------|-----------------------|-----------------------|
| mmmu_val |  60.890 | 57.44 |
| math_vision_test | 30.290 | 33.63 |
| orcbench_test | - | 82.059 |
| blink_val | 58.680 | 57.55 | 
| mmvet_v2 | 70.058 | 71.1219 | 
| mmmu_pro_vision_test |  35.360 | 41.62 |
| mmmu_pro_standard_test | 43.550 | 38.4 |
| cmmmu_val |  49.440 | 49.11 |
| cii_bench_test | 62.610 | 55.16 | 


# How to Run Locally
## 📌 Getting Started
### Download open-source weights

```bash

pip install modelscope
modelscope download --model Qwen/Qwen2.5-VL-32B-Instruct  --local_dir /nfs/Qwen2.5-VL-32B-Instruct

```

### Download the FlagOS image

```bash
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b
```

### Start the inference service

```bash
docker run --rm --init --detach \
  --net=host --uts=host --ipc=host \
  --security-opt=seccomp=unconfined \
  --privileged=true \
  --ulimit stack=67108864 \
  --ulimit memlock=-1 \
  --ulimit nofile=1048576:1048576 \
  --shm-size=32G \
  -v /nfs:/nfs \
  --gpus all \
  --name flagos \
  flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b \
  sleep infinity

docker exec -it flagos bash
```

### Modify serve configuration

1. Use  `pip show flag_scale` to find the location of installed flag_scale framework like `/usr/local/lib/python3.12/dist-packages`
2. `cd  /usr/local/lib/python3.12/dist-packages/flag_scale/examples/`
3. Use `mv robobrain2 qwen25_vl` to modify the config name
4. `vim qwen25_vl/serve/32b.yaml` to replace the content of RoboBrain2-32B to this model:

```
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /share/project/jiyuheng/ckpt/32b_stage2_K1
    served_model_name: RoboBrain2.0-32B-nvidia-flagos
    tensor_parallel_size: 8
    pipeline_parallel_size: 1
    gpu_memory_utilization: 0.9
    limit_mm_per_prompt: image=18 # should be customized, 18 images/request is enough for most scenarios
    port: 9010
    trust_remote_code: true
    enforce_eager: false # set true if use FlagGems
    enable_chunked_prefill: true

```

you should modify the 32b.yaml to:

```
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /nfs/Qwen2.5-VL-32B-Instruct
    served_model_name: Qwen2.5-VL-32B-Instruct-nvidia-flagos
    tensor_parallel_size: 8
    pipeline_parallel_size: 1
    gpu_memory_utilization: 0.9
    limit_mm_per_prompt: image=18
    port: 9010
    trust_remote_code: true
    enforce_eager: false # set true if use FlagGems
    enable_chunked_prefill: true

```

### Serve

```bash
flagscale serve qwen25_vl
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
