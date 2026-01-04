# Use cases

This section includes use cases for FlagGems.

## 1. Basic C++ runtime usage

Demonstrates basic usage of C++ runtime operators across multiple GPUs, multi-threading support, and compatibility with `torch.compile`.

```{code-block} python
import threading
import torch
import flag_gems  # noqa: F401

# Test basic tensor addition on multiple GPUs
x = torch.randn(10, device="cuda:0")
out = torch.ops.flag_gems.add_tensor(x, x)
print(out)

x = torch.randn(10, device="cuda:1")
out = torch.ops.flag_gems.add_tensor(x, x)
print(out)

x = torch.randn(10, device="cuda:2")
out = torch.ops.flag_gems.add_tensor(x, x)
print(out)

# Test multi-threading support
def f(x):
    print(torch.ops.flag_gems.add_tensor(x, x))

t = threading.Thread(target=f, args=(torch.randn(10, device="cuda:3"),))
t.start()
t.join()

# Test with torch.compile
def f(x, y):
    return torch.ops.flag_gems.add_tensor(x, y)

F = torch.compile(f)
x = torch.randn(2, 1, 3, device="cuda:1", requires_grad=True)
y = torch.randn(4, 1, device="cuda:1", requires_grad=True)
out = F(x, y)
ref = x + y
print(out)
print(ref)
```

## 2. Pre-tuning for inference

Pre-tunes GEMM and other operators for specific model architectures (LLaMA, Qwen variants) by running representative shapes to populate kernel caches, reducing autotuning overhead during inference.

```{code-block} python
import argparse
import torch
import flag_gems

device = flag_gems.device
DTYPES = {
    "float16": torch.float16,
    "bfloat16": torch.float32,
    "float32": torch.float32,
}

# Model-specific shapes for pre-tuning
LLAMA_SHAPES = {
    "mm": [
        [1024, 4096], [128256, 4096], [14336, 4096],
        [4096, 14336], [4096, 4096], [6144, 4096], [28672, 4096],
    ],
}

# ... other model shapes ...

MODEL_SHAPES = {
    "llama": LLAMA_SHAPES,
    "qwen": QWEN_SHAPES,
    # ... other models ...
}

def pretune_mm(max_tokens, max_reqs, shapes, dtype):
    for M in range(1, max_tokens + 1, 32):
        for N, K in shapes:
            tensor_a = torch.randn([M, K], dtype=dtype, device=device)
            tensor_b = torch.randn([K, N], dtype=dtype, device=device)
            flag_gems.mm(tensor_a, tensor_b)

# ... other pretune functions ...

OPERATORS = {
    "mm": pretune_mm,
    "mm_logits": pretune_mm_logits,
    "addmm": pretune_addmm,
    "index": pretune_index,
}

def args_parser():
    parser = argparse.ArgumentParser(description="pretune for gemm")
    parser.add_argument("--model", type=str, default="llama")
    parser.add_argument("--dtype", type=str, default="bfloat16")
    parser.add_argument("--max_tokens", type=int, default=16384)
    parser.add_argument("--max_reqs", type=int, default=1024)
    return parser.parse_args()

if __name__ == "__main__":
    args = args_parser()
    model = MODEL_SHAPES.get(args.model)
    dtype = DTYPES.get(args.dtype)
    max_tokens = args.max_tokens
    max_reqs = args.max_reqs
    if not model:
        exit(0)
    for op, func in OPERATORS.items():
        shapes = model.get(op)
        if not shapes:
            continue
        func(max_tokens, max_reqs, shapes, dtype)
```

## 3. LLaVA model testing

Validates accuracy of FlagGems integration with LLaVA multimodal model by comparing logits output with and without FlagGems enabled, using cosine similarity as fallback metric.

```{code-block} python
import pytest
import requests
import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
import flag_gems

device = flag_gems.device

@pytest.mark.parametrize("prompt", ["USER: <image>\nWhat's the content of the image? ASSISTANT:"])
@pytest.mark.parametrize("url", [
    "https://www.ilankelman.org/stopsigns/australia.jpg",
    "https://www.ilankelman.org/themes2/towerpisaleaning.jpg",
    "https://www.ilankelman.org/themes1/sunsetrainbowbb.jpg",
])
def test_accuracy_llava(prompt, url):
    model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf")
    processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")
    torch.manual_seed(1234)
    model.to(device).eval()
    image = Image.open(requests.get(url, stream=True).raw)
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device=flag_gems.device)
    
    with torch.no_grad():
        ref_output = model(**inputs).logits
    
    with flag_gems.use_gems():
        res_output = model(**inputs).logits
    
    maxdiff = torch.max(torch.abs(ref_output - res_output))
    succeed = True
    if not torch.allclose(ref_output, res_output, atol=1e-3, rtol=1e-3):
        score = torch.nn.functional.cosine_similarity(
            ref_output.flatten(), res_output.flatten(), dim=0, eps=1e-6
        )
        succeed = score >= 0.99
    
    assert succeed, f"LLAVA FAIL with maxdiff {maxdiff} and score {score}"
```

## 4. LLaMA model testing

Tests FlagGems accuracy with LLaMA-2-7B model by comparing generated text tokens between reference and FlagGems-enabled runs.

```{code-block} python
import pytest
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import flag_gems

device = flag_gems.device

@pytest.mark.parametrize("prompt", [
    "How are you today?", "What is your name?", 
    "Who are you?", "Where are you from?"
])
def test_accuracy_llama(prompt):
    tokenizer = AutoTokenizer.from_pretrained("sharpbai/Llama-2-7b-hf")
    model = AutoModelForCausalLM.from_pretrained("sharpbai/Llama-2-7b-hf")
    model.to(device).eval()
    inputs = tokenizer(prompt, return_tensors="pt").to(device=device)
    
    with torch.no_grad():
        ref_output = model.generate(**inputs, max_length=100, num_beams=5)
    
    with flag_gems.use_gems():
        res_output = model.generate(**inputs, max_length=100, num_beams=5)
    
    maxdiff = torch.max(torch.abs(ref_output - res_output))
    assert torch.allclose(
        ref_output, res_output, atol=1e-3, rtol=1e-3
    ), f"LLAMA FAIL with maxdiff {maxdiff}"
```

## 5. BERT model testing

Validates FlagGems accuracy across different data types (float16, float32, bfloat16) with BERT model by comparing hidden states against float32 reference.

```{code-block} python
import copy
import pytest
import torch
from transformers import AutoTokenizer, BertConfig, BertModel
import flag_gems

device = flag_gems.device

@pytest.mark.parametrize("prompt", [
    "How are you today?", "What is your name?", 
    "Who are you?", "Where are you from?"
])
@pytest.mark.parametrize("dtype", [torch.float16, torch.float32, torch.bfloat16])
def test_accuracy_bert(prompt, dtype):
    config = BertConfig()
    model = BertModel(config)
    tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Reference model in float32
    ref_model = copy.deepcopy(model)
    ref_model.to(torch.float32).to(device).eval()
    ref_inputs = copy.deepcopy(inputs).to(torch.float32)
    with torch.no_grad():
        ref_outputs = ref_model(**ref_inputs).last_hidden_state.to(dtype)
    
    # Test model in target dtype
    res_model = copy.deepcopy(model)
    res_model.to(dtype).to(device).eval()
    res_inputs = copy.deepcopy(inputs).to(dtype)
    with flag_gems.use_gems():
        with torch.no_grad():
            res_outputs = res_model(**res_inputs).last_hidden_state
    
    maxdiff = torch.max(torch.abs(ref_outputs - res_outputs))
    succeed = True
    if not torch.allclose(ref_outputs, res_outputs, atol=1e-3, rtol=1e-3):
        score = torch.nn.functional.cosine_similarity(
            ref_outputs.flatten(), res_outputs.flatten(), dim=0, eps=1e-6
        )
        succeed = score >= 0.99
    
    assert succeed, f"BERT_{dtype} FAIL with maxdiff {maxdiff} and score {score}"
```

## 6. vLLM integration

Demonstrates full integration of FlagGems with vLLM inference engine, enabling both standard PyTorch operator replacement and vLLM-specific custom kernel patches.

```{code-block} python
import random
import time
import numpy as np
import torch
from vllm import LLM, SamplingParams
import flag_gems

flag_gems.enable()  # Enable gems for PyTorch (aten) operators
flag_gems.apply_gems_patches_to_vllm(verbose=True)  # Patch vLLM custom ops

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=120)

def main():
    llm = LLM(
        model="Qwen/Qwen2.5-7B-Instruct",
        tensor_parallel_size=1,
        max_model_len=1024,
        gpu_memory_utilization=0.98,
    )
    outputs = llm.generate(prompts, sampling_params)
    print("-" * 50)
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}\nGenerated text: {generated_text!r}")
    print("-" * 50)
    time.sleep(10)

if __name__ == "__main__":
    main()
```

## 7.DeepSeek with vLLM

Shows FlagGems integration with DeepSeek-V3 model in vLLM, including forcing specific attention backend and using bfloat16 precision.

```{code-block} python
import torch
from vllm import LLM, SamplingParams
from vllm.attention.selector import global_force_attn_backend
from vllm.platforms import _Backend
import flag_gems

global_force_attn_backend(_Backend.TRITON_MLA)

def main():
    prompts = [
        "Hello, my name is",
        "The president of the United States is",
        "The capital of France is",
        "The future of AI is",
    ]
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95, max_tokens=120)
    model_name = "deepseek-ai/DeepSeek-V3"
    
    llm = LLM(
        model=model_name,
        max_model_len=2048,
        gpu_memory_utilization=0.98,
        enforce_eager=True,
        dtype="bfloat16",
        trust_remote_code=True,
    )
    
    flag_gems.enable()
    with torch.no_grad():
        outputs = llm.generate(prompts, sampling_params)
        for output in outputs:
            prompt = output.prompt
            generated_text = output.outputs[0].text
            print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

if __name__ == "__main__":
    main()
```

## 8. PyTorch 2.0 Compliance Testing

Validates PyTorch 2.0 compliance of FlagGems operators using torch.library.opcheck to ensure proper schema, autograd, faketensor, and AOT dispatch support.

```{code-block} python
import torch
from torch.library import opcheck
import flag_gems  # noqa: F401

inputs = [
    (torch.randn(2, 8, 4, device="cuda:0"), torch.randn(4, device="cuda:0")),
    (torch.randn(3, 8, 4, device="cuda:0", requires_grad=True), torch.randn(3, 1, 4, device="cuda:0")),
    (torch.randn(2, 8, 4, device="cuda:0"), torch.randn(1, 4, device="cuda:0", requires_grad=True)),
    (torch.randn(2, 1, 4, device="cuda:0", requires_grad=True), torch.randn(2, 8, 1, device="cuda:0", requires_grad=True)),
]

for arg in inputs:
    opcheck(
        torch.ops.flag_gems.add_tensor.default,
        arg,
        test_utils=(
            "test_schema",
            "test_autograd_registration",
            "test_faketensor",
            "test_aot_dispatch_static",
            "test_aot_dispatch_dynamic",
        ),
    )
```