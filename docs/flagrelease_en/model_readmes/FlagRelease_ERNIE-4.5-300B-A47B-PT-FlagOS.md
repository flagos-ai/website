# Introduction

**FlagOS** is a unified heterogeneous computing software stack for large models, co-developed with leading global chip manufacturers. With core technologies such as the **FlagScale** distributed training/inference framework, **FlagGems** universal operator library, **FlagCX** communication library, and **FlagTree** unified compiler, the **FlagRelease** platform leverages the FlagOS stack to automatically produce and release various combinations of <chip + open-source model>. This enables efficient and automated model migration across diverse chips, opening a new chapter for large model deployment and application.

Based on this, the **ERNIE-4.5-300B-A47B-PT-FlagOS-Nvidia** model is adapted for the Nvidia chip using the FlagOS software stack, enabling:

### Integrated Deployment

- Deep integration with the open-source [FlagScale framework](https://github.com/FlagOpen/FlagScale)
- Out-of-the-box inference scripts with pre-configured hardware and software parameters
- Released **FlagOS**-A800 container image supporting deployment within minutes

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

| Metrics   | ERNIE-4.5-300B-A47B-PT-H100-CUDA | ERNIE-4.5-300B-A47B-PT-FlagOS-Nvidia |
| --------- | -------------------------------- | ------------------------------------ |
| AIME      | 0.667                            | 0.700                                |
| GPQA      | 0.669                            | 0.669                                |
| LiveBench | 0.685                            | 0.690                                |
| MMLU      | 0.773                            | 0.788                                |
| MUSR      | 0.724                            | 0.710                                |

# User Guide

## General Information 

**Basic Information**

| Type            | Location                                                     |
| --------------- | ------------------------------------------------------------ |
| Model Weights   | https://www.modelscope.cn/models/PaddlePaddle/ERNIE-4.5-300B-A47B-PT/files |
| Container Image | flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_ernie_rank0 |

**Environment Setup**

| System Component                | Version Information                  |
| ------------------------------- | ------------------------------------ |
| Accelerator Card Driver Version | Driver Version: 535.154.05           |
| Docker Version                  | Docker version 24.0.0, build 98fdcd7 |
| Operating System                | Description:    Ubuntu 20.04 LTS     |
| FlagScale                       | Version: 0.8.0                       |
| FlagGems                        | Version: 2.2                         |

## Operation Steps【***need two machines***】

### Download Open-source Model Weights

**Execution under shared storage on master node IP**

```python
pip install modelscope
modelscope download --model PaddlePaddle/ERNIE-4.5-300B-A47B-PT --local_dir /share/models/ERNIE-4.5-300B-A47B-PT
```

### Download FlagScale

**Execution under shared storage on master node IP**  [Prerequisite: Network connectivity to github.com is required]

```python
cd /share/repos
git clone https://github.com/FlagOpen/FlagScale.git && cd FlagScale&& git checkout 230dc1d879d8c2af1e449fc29b0cd1867e07c0c3

# Modify the installation backend of FlagScale
cd /share/repos/FlagScale; 
vim pyproject.toml
# Comment out line 3, which contains 'build-backend'
```

### Download FlagOS Image

**Dual-machine execution**

```python
docker pull flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_ernie_rank0 
```

### Start the inference service

**Dual-machine execution**【**Mount weights and flagscale to `/repos` and `/models` respectively**】

```
#Container Startup
docker run --rm --init --detach \
  --net=host --uts=host --ipc=host \
  --security-opt=seccomp=unconfined \
  --privileged=true \
  --ulimit stack=67108864 \
  --ulimit memlock=-1 \
  --ulimit nofile=1048576:1048576 \
  --shm-size=32G \
  -v /share:/share \
  --gpus all \
  --name flagos \
  flagrelease-registry.cn-beijing.cr.aliyuncs.com/flagrelease/flagrelease:flagrelease_nv_robobrain2_32b \
  sleep infinity
  
docker exec -it flagos bash
```

### **Modify configuration files**

**Execution on Master Node IP**---**Edit the `hostfile.txt` file**

Change the IP in hostfile.txt to the corresponding machine's IP

```python
vim /repos/FlagScale/examples/ernie45/conf/hostfile.txt
# ip slots type=xxx[optional]
# master node
x.x.x.x slots=8 type=gpu 
# worker nodes
x.x.x.x slots=8 type=gpu
```

**Execution on Master Node IP**---**Modify the `serve.yaml` file**

In serve.yaml, set USE_FLAGGEMS to true; change docker to the name of the launched container (e.g., flagos); set ssh_port to the worker nodes' IP and the port where openssh-server is running (usually 22)

```python
vim /repos/FlagScale/examples/ernie45/conf/serve.yaml
defaults:
- _self_
- serve: 300b

experiment:
  exp_name: ernie45_300b
  exp_dir: outputs/${experiment.exp_name}
  task:
    type: serve
  runner:
    hostfile: examples/ernie45/conf/hostfile.txt
    nnodes: 2
    nproc_per_node: 8
    docker: flagos # Change to the name of the launched container (e.g., flagos)
    ssh_port: 22 # Change to the worker nodes' IP and the port where openssh-server is running (usually 22)
  deploy:
    use_fs_serve: false
  envs:
    CUDA_VISIBLE_DEVICES: 0,1,2,3,4,5,6,7
    CUDA_DEVICE_MAX_CONNECTIONS: 1
    USE_FLAGGEMS: true
    RAY_CGRAPH_get_timeout: 60 # should be set when USE_FLAGGEMS=true, default is 10 from ray
  cmds:
    before_start: source /root/miniconda3/bin/activate flagscale-inference

action: run

hydra:
  run:
    dir: ${experiment.exp_dir}/hydra

```

**Execution on Master Node IP**---**Modify the `serve/300b.yaml` file**

In serve/300b.yaml, set the model path to /models/ERNIE-4.5-300B-A47B-PT

```python
vim /repos/FlagScale/examples/ernie45/conf/serve/300b.yaml
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /models/ERNIE-4.5-300B-A47B-PT # add Post-trained models
    host: 0.0.0.0
    max_model_len: 128000
    max_num_seqs: 256 # for high-throughput server
    uvicorn_log_level: warning
    port: 30000
  engine_args_specific:
    vllm:
      tensor_parallel_size: 8
      pipeline_parallel_size: 2
      gpu_memory_utilization: 0.98
      trust_remote_code: true
      enforce_eager: true # enforce_eager is recommended to be set true, false may trigger unknown but reproduced NCCL exception
      enable_chunked_prefill: true
  profile:
    prefix_len: 0
    input_len: 1024
    output_len: 1024
    num_prompts: 128
    range_ratio: 1
```

### **Enter the `flagscale-inference` environment and reinstall `flagscale`**

**Dual-machine execution**

```python
conda activate flagscale-inference
cd /repos/FlagScale
pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple --no-build-isolation
```

### unpatch the vendor's code

**Execution on Master Node IP**

```python
cd /repos/FlagScale
python3 tools/patch/unpatch.py --backend=vllm
```

### build vllm

**Dual-machine execution**

```python
cd /repos/FlagScale/third_party/vllm
pip install . -i https://pypi.tuna.tsinghua.edu.cn/simple --no-build-isolation
```

### **Set up passwordless access from the master container to worker host machines**

```python
Write the contents of the ~/.ssh/id_rsa.pub file from the flagos container on the master node into the ~/.ssh/authorized_keys file on the worker nodes' physical machines.
```

### Serve

**Execution on Master Node IP**

```python
cd /repos/FlagScale
flagscale serve ernie45

#After the service starts, you will see output similar to the following:
#INFO 07-08 09:49:51 [api_server.py:1349] Starting vLLM API server 0 on http://0.0.0.0:30000

```

# Service Invocation

## API-based Invocation Script

```
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:30000/v1/"
model = "/models/ERNIE-4.5-300B-A47B-PT"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather like today?"}
]
response = openai.chat.completions.create(
    model=model,
    messages=messages,
    stream=False,
)
for item in response:
    print(item)
```

## AnythingLLM Integration Guide

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

# Frequently Asked Questions

### Q1: What should I do if the model fails to load?

- Check if the model weight path is correct.
- Ensure the  model files are present in the `/share` directory inside the container.
- Check the container logs: `docker logs flagos`.

### Q2: API call returns a timeout error. What should I do?

- Verify that the server IP address is correct.
- Check the firewall settings to ensure port 9010 is open.
- Confirm that the service is running properly: `docker exec flagos ps aux | grep flagscale`.

### Q3: When installing vLLM, if you encounter errors. What should I do?

- You need to retry a few times.
- Confirm reachability to GitHub.com and associated endpoints.
- Validate network bandwidth (50MB/s or higher recommended for reliable operation).

# Contributing

We warmly welcome global developers to join us:

1. Submit Issues to report problems
2. Create Pull Requests to contribute code
3. Improve technical documentation
4. Expand hardware adaptation support

# Contact Us

![image](image_.jpeg)

# License

This project and related model weights are licensed under the MIT License.

Release Date: 2025.07.08