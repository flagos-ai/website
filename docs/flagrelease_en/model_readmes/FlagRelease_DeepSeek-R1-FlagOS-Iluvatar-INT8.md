# Introduction

DeepSeek-R1-FlagOS-Iluvatar-INT8 provides an all-in-one deployment solution, enabling execution of DeepSeek-R1 on Iluvatar GPUs. As the first-generation release for the ILUVATAR series, this package delivers three key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Verified model files, available on Hugging Face ([Model Link](https://huggingface.co/FlagRelease/DeepSeek-R1-FlagOS-Iluvatar-INT8)).
   - Pre-built Docker image for rapid deployment on Iluvatar.
2. INT8 Checkpoints:
   - INT8 checkpoints dequantized from the official DeepSeek-R1 FP8 model to ensure enhanced inference performance.
3. Consistency Validation:
   - Evaluation tests verifying consistency of results between Nvidia H100 and Iluvatar.

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

## INT8 Dequantization

We provide dequantized model weights in bfloat16 to run DeepSeek-R1 on Iluvatar GPUs, along with adapted configuration files and tokenizer.

# Bundle Download

Requested by Iluvatar, the file of docker image and model files should be applied by email.

|             | Usage                                                  | Cambricon                                                    |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------ |
| Basic Image | basic software environment that supports model running | [services@iluvatar.comContact](https://www.modelscope.cn/models/FlagRelease/DeepSeek-R1-INT4-FlagOS-Iluvatar/file/view/master/mailto%3Aservices@iluvatar.comContact?status=1) by email，please indicate the unit/contact person/contact information/equipment source/specific requirements |

# Evaluation Results

## Benchmark Result 

| Metrics               | DeepSeek-R1-H100-CUDA | DeepSeek-R1-FlagOS-Iluvatar-INT8 |
| --------------------- | --------------------- | -------------------------------- |
| GSM8K (EM)            | 95.75                 | 95.53                            |
| MMLU (Acc.)           | 85.34                 | 82.16                            |
| CEVAL                 | 89.00                 | 80.31                            |
| MATH-500 (Pass@1)     | 93.20                 | TBD                              |
| GPQA-Diamond (Pass@1) | 70.20                 | TBD                              |
| AIME 2024 (Pass@1)    | 76.67                 | TBD                              |

# How to Run Locally

## 📌 Getting Started

### Download open-source weights

```
pip install modelscope
modelscope download --model deepseek-ai/DeepSeek-R1 --local_dir /mnt/share/DeepSeek-R1
```
contact services@iluvatar.comContact to obtain the quanted weights

### Download the FlagOS image

```
docker pull baai:v5
```

### Start the inference service

```
docker run --shm-size="32g" -itd -v /dev:/dev -v /usr/src/:/usr/src -v /lib/modules/:/lib/modules -v /mnt/share:/data1 --privileged --cap-add=ALL --pid=host --net=host --name flagrelease_bi baai:v5

docker exec -it flagrelease_bi /bin/bash
```

### Download and install FlagGems

```
git clone https://github.com/FlagOpen/FlagGems.git
cd FlagGems
git checkout deepseek_release_iluvatar
# no additional dependencies since they are already handled in the Docker environment
pip install ./ --no-deps
cd ../
```

### Download and install FlagScale

```
git clone https://github.com/FlagOpen/FlagScale.git 
cd FlagScale
# unpatch 
python tools/patch/unpatch.py \
  --backend vllm FlagScale \
  --task inference --device-type BI_V150 \
  --key-path ~/0523_qwen3_key/  # The key needs to be obtained from the vendor
# compile vllm
cd build/BI_V150/FlagScale/third_party/vllm
bash clean_vllm.sh && bash build_vllm.sh && bash install_vllm.sh
cd ../../
 
```

### Modify the configuration

```
cd FlagScale/build/BI_V150/FlagScale/examples/deepseek_r1/conf/
# Modify the configuration in config_deepseek_r1.yaml
defaults:
  - _self_
  - serve: deepseek_r1

experiment:
  exp_name: deepseek_r1
  exp_dir: outputs/${experiment.exp_name}
  task:
    type: serve
  deploy:
    use_fs_serve: false
  runner:
    hostfile: examples/deepseek_r1/conf/hostfile.txt  # set hostfile
    docker: flagrelease_bi # set docker
  envs:
    CUDA_DEVICE_MAX_CONNECTIONS: 1
  cmds:
    before_start: export TRITON_CACHE_DIR="/cache" && export USE_FLAGGEMS=true && export NCCL_SOCKET_IFNAME=ens1f0 && export VLLM_FORCE_NCCL_COMM=1 && export GLOO_SOCKET_IFNAME=ens1f0 && export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

action: run

hydra:
  run:
    dir: ${experiment.exp_dir}/hydra
```

```
cd FlagScale/build/BI_V150/FlagScale/examples/deepseek_r1/conf/
# Modify the configuration in hostfile.txt
# ip slots type=xxx[optional]
# master node
x.x.x.x slots=16 type=gpu
# worker nodes
x.x.x.x slots=16 type=gpu
```

```
cd FlagScale/build/BI_V150/FlagScale/examples/deepseek_r1/conf/serve
# Modify the configuration in deepseek_r1.yaml
- serve_id: vllm_model
  engine: vllm
  engine_args:
    model: /data1/models/DeeSeek-R1_INT8  # path of weight of deepseek r1
    tensor-parallel-size: 8
    pipeline-parallel-size: 4
    max_num_seqs: 256
    max-model-len: 5120
    gpu-memory-utilization: 0.8
    port: 9010 # port to serve
    trust-remote-code: true
```

```
# install flagscale
cd FlagScale/build/BI_V150/FlagScale/
pip3 install . --no-build-isolation

#【Verifiable on a single machine】
```

### Serve

```
flagscale serve <Model>
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

# License

This project and related model weights are licensed under the MIT License.