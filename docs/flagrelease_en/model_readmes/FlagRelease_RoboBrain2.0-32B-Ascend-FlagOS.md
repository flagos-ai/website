# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **RoboBrain2.0-32B-Ascend-FlagOS** model is adapted for the Ascend chip using the FlagOS software stack, enabling:

### Integrated Deployment

- Deep integration with the open-source [FlagScale framework](https://github.com/FlagOpen/FlagScale)
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS-Ascend** container image supporting deployment within minutes

### Consistency Validation

- Rigorously evaluated through benchmark testing: Performance and results from the FlagOS software stack are compared against native stacks on multiple public.

# Technical Overview

## **FlagScale Distributed Training and Inference Framework**

FlagScale is an end-to-end framework for large models across heterogeneous computing resources, maximizing computational efficiency and ensuring model validity through core technologies. Its key advantages include:

- **Unified Deployment Interface:** Standardized command-line tools support one-click service deployment across multiple hardware platforms, significantly reducing adaptation costs in heterogeneous environments.
- **Intelligent Parallel Optimization:** Automatically generates optimal distributed parallel strategies based on chip computing characteristics, achieving dynamic load balancing of computation/communication resources.
- **Seamless Operator Switching:** Deep integration with the FlagGems operator library allows high-performance operators to be invoked via environment variables without modifying model code.

## **FlagGems Universal Large-Model Operator Library**

FlagGems is a Triton-based, cross-architecture operator library collaboratively developed with industry partners. Its core strengths include:

- **Full-stack Coverage**: Over 100 operators, with a broader range of operator types than competing libraries.
- **Ecosystem Compatibility**: Supports 7 accelerator backends. Ongoing optimizations have significantly improved performance.
- **High Efficiency**: Employs unique code generation and runtime optimization techniques for faster secondary development and better runtime performance compared to alternatives.

## **FlagEval Evaluation Framework**

FlagEval (Libra)** is a comprehensive evaluation system and open platform for large models launched in 2023. It aims to establish scientific, fair, and open benchmarks, methodologies, and tools to help researchers assess model and training algorithm performance. It features:
  - **Multi-dimensional Evaluation**: Supports 800+ model evaluations across NLP, CV, Audio, and Multimodal fields, covering 20+ downstream tasks including language understanding and image-text generation.
  - **Industry-Grade Use Cases**: Has completed horizontal evaluations of mainstream large models, providing authoritative benchmarks for chip-model performance validation.

# Evaluation Results

## Benchmark Result 

| Metric                   | RoboBrain2.0-32B-H100-CUDA | RoboBrain2.0-32B-Ascend-FlagOS |
|--------------------------|----------------------------|--------------------------------|
| SAT                      | 86.670                     | 82.670                        |
| all_angles_bench         | 50.840                     | 50.980                        |
| Where2Place              | 69.580                     | 76.630                        |
| blink_val_ev             | 72.830                     | 72.110                        |
| robo_spatial_home_all    | 68.774                     | 69.531                        |
| egoplan_bench2           | 51.780                     | 49.130                        |
| erqa                     | 44.500                     | 41.750                        |
| cv_bench_test            | 83.190                     | 82.920                        |
| embspatial_bench         | 74.310                     | 73.820                        |
| vsi_bench_tiny           | 42.690                     | 40.710                        |
| Where2Place-nothink      | 73.590                     | 73.020                        |
| blink_val_ev-nothink     | 68.350                     | 68.930                        |
| cv_bench_test-nothink    | 83.920                     | 84.000                        |
| robo_spatial_home_all-nothink | 72.430                | 73.772                        |
| embspatial_bench-nothink | 78.570                     | 78.300                        |
| all_angles_bench-nothink | 50.140                     | 49.770                        |
| vsi_bench_tiny-nothink   | 39.820                     | 41.330                        |
| SAT-nothink              | 76.670                     | 77.330                        |
| egoplan_bench2-nothink   | 57.230                     | 56.620                        |
| erqa-nothink             | 40.250                     | 41.750                        |

# User Guide

**Environment Setup**

| Accelerator Card Driver Version | Kernel Mode Driver Version: 2.3.0          | 
| ------------- | ------------------------------------------------------------ |  
| Docker Version                  | Docker version 20.10.8, build 3967b7d| 
| Operating System                | Description:    5.10.0-216.0.0.115.oe2203sp4.aarch64       | 
| FlagScale                       | Version: 0.8.0                        | 
| FlagGems                        | Version: 2.2                          | 

## Operation Steps

### Download Open-source Model Weights

```bash
pip install modelscope
modelscope download --model BAAI/RoboBrain2.0-32B --local_dir /data/weights/RoboBrain2.0-32B

```

### Download FlagOS Image

```bash
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_ascend_robobrain2_32b
```

### Start the inference service

```bash
#Container Startup
docker run -itd --name flagos \
    -u root \
    -w /workspace \
    --privileged=true \
    --shm-size=1000g \
    --net=host \
    -v /usr/local/Ascend/driver:/usr/local/Ascend/driver \
    -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
    -v /usr/local/dcmi:/usr/local/dcmi \
    -v /usr/local/sbin:/usr/local/sbin \
    -v /usr/share/zoneinfo/Asia/Shanghai:/etc/localtime \
    -v /etc/ascend_install.info:/etc/ascend_install.info \
    -v /data:/data \
    -v /root/.cache:/root/.cache \
    -e VLLM_USE_V1=1 \
    -e CPU_AFFINITY_CONF=2 \
    -e PYTORCH_NPU_ALLOC_CONF=max_split_size_mb:256 \
    -e USE_FLAGGEMS=true \
    flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_ascend_robobrain2_32b bash
source /usr/local/Ascend/ascend-toolkit/set_env.sh && source /usr/local/Ascend/nnal/atb/set_env.sh
```

### Modify Configs About HostIP

1. use `pip show flag_scale` to find flag_scale's path like `/root/miniconda3/lib/python3.11/site-packages/flag_scale`, then `vim /root/miniconda3/lib/python3.11/site-packages/flag_scale/examples/robobrain2/conf/serve/32b.yaml`
2. the content of this file is:
```
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /data/weights/RoboBrain2.0-32B/ # path of weight of deepseek r1
    served_model_name: RoboBrain2.0-32B-ascend-flagos
    tensor_parallel_size: 8
    gpu_memory_utilization: 0.8
    host: 10.1.15.113
    port: 9010
    block_size: 128
    enforce_eager: true
    no_enable_prefix_caching: true
    no_enable_chunked_prefill: true

```
3. you should modify the `host:10.1.15.113` to your real ip

### Serve

```bash
flagscale serve robobrain2

```


## Service Invocation

### API-based Invocation Script

```bash
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:9010/v1/"
model = "RoboBrain2.0-32B-ascend-flagos"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like today?"}
]
response = openai.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.7,
    top_p=0.95,
    stream=False,
)
for item in response:
    print(item)

```

### AnythingLLM Integration Guide

#### 1. Download & Install

- Visit the official site: https://anythingllm.com/
- Choose the appropriate version for your OS (Windows/macOS/Linux)
- Follow the installation wizard to complete the setup

#### 2. Configuration

- Launch AnythingLLM
- Open settings (bottom left, fourth tab)
- Configure core LLM parameters
- Click "Save Settings" to apply changes

#### 3. Model Interaction

- After model loading is complete:
  - Click **"New Conversation"**
  - Enter your question (e.g., “Explain the basics of quantum computing”)
  - Click the send button to get a response

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support


# License

The weights of this model are based on BAAI/RoboBrain2.0-32B and are open-sourced under the Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt.