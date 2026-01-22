# Introduction

QwQ-32B-FlagOS-iluvatar  provides an all-in-one deployment solution, enabling execution of QwQ-32B on iluvatar GPUs. As the first-generation release for the iluvatar-BI-V150, this package delivers two key features:

1. Comprehensive Integration:
   - Integrated with FlagScale (https://github.com/FlagOpen/FlagScale).
   - Open-source inference execution code, preconfigured with all necessary software and hardware settings.
   - Pre-built Docker image for rapid deployment on iluvatar-BI-V150.
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

We validate the execution of QwQ-32B model with a Triton-based operator library as a PyTorch alternative.

We use a variety of Triton-implemented operation kernels  to run the QwQ-32B model. These kernels come from two main sources:

- Most Triton kernels are provided by FlagGems (https://github.com/FlagOpen/FlagGems). You can enable FlagGems kernels by setting the environment variable USE_FLAGGEMS. 

- Also included are Triton kernels from vLLM, such as fused MoE.

# Evaluation Results

## Benchmark Result 


| Metrics   | Qwen3-4B-H100-CUDA | Qwen3-4B-FlagOS-Iluvatar|
| --------- | ------------------ | ---------------------- |
| LIVEBENCH | 0.501              | 0.497                  |
| AIME      | 0.700              | 0.767                  |
| GPQA      | 0.410              | 0.338                  |
| MMLU      | 0.669              | 0.675                  |
| MUSR      | 0.590              | 0.586                  |

# How to Run Locally

## 📌 Getting Started

### Download open-source weights

```bash
pip install modelscope
modelscope download --model Qwen/Qwen3-4B --local_dir /nfs/Qwen/Qwen3-4B

```

### Download the FlagOS image

Please contact services@iluvatar.com by email to request the image files required for the model, and be sure to include your organization name, contact person, contact information, equipment source, and specific requirements.

```bash
docker pull <IMAGE>
```

### Start the inference service

```bash
docker run --shm-size="32g" -itd -v /dev:/dev -v /usr/src/:/usr/src -v /lib/modules/:/lib/modules -v /nfs/:/nfs/ --privileged --cap-add=ALL --pid=host --net=host --name flagos <IMAGE>

docker exec -it flagos bash
```

### Serve

```bash
flagscale serve qwen3
```

## Service Invocation

### API-based Invocation Script

```bash
import openai
openai.api_key = "EMPTY"
openai.base_url = "http://<server_ip>:9010/v1/"
model = "Qwen3-4B-metax-flagos"
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

本模型的权重来源于Qwen/Qwen3-4B，以apache2.0协议https://www.apache.org/licenses/LICENSE-2.0.txt开源。