---
frameworks:
- ""
language:
- zh
- en
license: apache-2.0
tasks: []
---

# Introduction
Following its debut at the World Artificial Intelligence Conference (WAIC 2026) on July 19, ModelBest, in partnership with OpenBMB, officially open‑sourced the next‑generation edge model “Little Cannon” MiniCPM5‑2B on September 7. With 2B parameters, the model attained a score of 17 on the authoritative Artificial Analysis (AA‑Index) leaderboard, securing first place worldwide among models under 4B parameters, and recorded an average score of 54.26 across multiple authoritative benchmark evaluations, markedly outperforming same‑size counterparts including Qwen3.5‑2B (41.66), Qwen3‑1.7B (40.89), and Gemma‑4‑E2B‑it (37.62). Natively supporting hybrid thinking for seamless switching between fast responses and deep reasoning, it offers a 512K ultra‑long context window and comes with built‑in core agent capabilities covering tool calling, deep search and code generation, and can serve directly as an edge agent foundation for smartphones, PCs, smart cockpits and other devices. ModelBest additionally released UltraX, its tiered data governance technology, together with full‑process agent training technology.

### Integrated Deployment

- Out-of-the-box inference commands for Mac native Runtime installation and Linux Docker deployment, with platform-specific hardware and software parameters.

### Consistency Validation

- On Apple M5 Pro, the FlagOS serving route has been validated through model loading, native-operator tests, real OpenAI-compatible HTTP requests, and repeatable batch-one performance measurements. Linux/CIX validation with the same release checkpoint is pending.

# Evaluation Results

## Benchmark Result

| Metrics | MiniCPM5-2B-Origin | MiniCPM5-2B-W8A8-Channel-FlagOS |
| --- | ---: | ---: |
| Math-500 | 93.46 | 91.4 |
| mmlu_pro_other | 51.52 | 53.03 |

Benchmark scores are provided by the model release owner; these accuracy evaluations were not rerun as part of the vLLM 0.24 Runtime validation below.

# Validated batch-one performance

| Model Format | Test Platform | PP512 (tokens/s) | TG128 (tokens/s) | Total (tokens/s) |
| --- | --- | ---: | ---: | ---: |
| W8A8 | Mac M5 Pro CPU | 1146.82 | 64.91 | 265.65 |
| W8A8 | CIX P1 | 235.15 | 14.31 | 57.91 |

Performance figures provided by the model release owner. PP512 denotes prefill throughput for 512 input tokens; TG128 denotes decode throughput for 128 output tokens; Total is the combined workload throughput, not the decode-only rate.

## User Guide

### Mac

Test environment: **M5 Pro CPU Only**, macOS arm64, 64 GiB memory.
Install the native FlagOS Runtime package with vLLM `0.24.0+cpu`.

### Linux

Test environment: **CIX P1**, Linux arm64, eight Cortex-A720 cores, 32 GiB or more memory.
Use the CIX Docker image with vLLM `0.24.0+cpu`.

Mac validation passed with the selected release weights; Linux validation with those exact files is pending.

## Operation Steps

### Shared Model Download (Linux and Mac)

Install the ModelScope command-line tool:

```bash
python3 -m pip install --user modelscope
```

After repository publication, or using authorized access, download the W8A8 Channel checkpoint. Run this same download step on either platform:

```bash
export MODEL_REPO="FlagRelease/MiniCPM5-2B-W8A8-arm-FlagOS"
export MODEL_DIR="$HOME/Models/MiniCPM5-2B-W8A8-Channel-FlagOS"

modelscope download \
  --model "$MODEL_REPO" \
  --local_dir "$MODEL_DIR"
```

Verify all model files and the release weight identity before serving. Keep the full repository contents, including its configuration and tokenizer; do not combine them with files from a different checkpoint.

Follow only the platform section for your host: [Linux / CIX P1](#linux--cix-p1-docker) or [Mac / M5 Pro](#mac--m5-pro-native-runtime). Each section includes checksum verification before inference.

The checkpoint contract is:

- Architecture: 42-layer `LlamaForCausalLM`, text-only inference.
- Model-body weights: symmetric INT8 per output channel, compressed-tensors `int-quantized` format.
- Input activations: dynamic symmetric per-token INT8.
- Weight scales: FP32 `row_channel`; embedding and `lm_head`: BF16.
- Default documented serving context: 8192 tokens; the model configuration declares up to 131072 tokens.

### Linux / CIX P1 (Docker)

The unified release checkpoint still requires end-to-end validation in this image. Keep strict coverage enabled and use the repository files downloaded above.

#### 1. Prepare the Linux Host

The CIX path is a Docker deployment, not an installation of the macOS Runtime. It requires Linux arm64, Docker, a CIX P1 board with at least 32 GiB memory, and access to the BAAI Harbor registry. Log in if the registry requires authentication:

```bash
sudo docker login harbor.baai.ac.cn
```

Confirm that `uname -m` reports `aarch64`, then check the CPU topology before applying the CIX affinity:

```bash
uname -m
lscpu -e=CPU,CORE,ONLINE,MAXMHZ
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
  printf '%s ' "${cpu##*/}"
  cat "$cpu/regs/identification/midr_el1" 2>/dev/null || echo unreadable
done
```

The validated CIX P1 policy uses Cortex-A720 CPUs `0,1,6,7,8,9,10,11`; do not include the Cortex-A520 CPUs `2,3,4,5`.

Verify the downloaded model files; stop if either check fails:

```bash
(cd "$MODEL_DIR" && sha256sum -c SHA256SUMS)
(cd "$MODEL_DIR" && printf '%s  %s\n' \
  'ce27c62b10b4e7bbecbf84b7c820d3b293f9f7ff93a5963aecd785009abda905' \
  'model-00000-of-00001.safetensors' | sha256sum -c -)
```

#### 2. Pull the Docker Image

Pull the candidate W8 environment by immutable digest and inspect its identity:

```bash
export CIX_IMAGE='harbor.baai.ac.cn/flagrelease-public/minicpm5-2b-w8a8-armv9-tree_3.7.2_git4db2332e-gems_0.0.post1.dev3404_g03ff66323-vllm_0.24.0_cpu-plugin_0.0.0-cx_none-python_3.11.2-torch_2.11.0_cpu-pcp_none-gpu_cpu-arc_arm64-driver_none:202609051345'

export CIX_IMAGE_REF="${CIX_IMAGE%:*}@${CIX_IMAGE_DIGEST}"
sudo docker pull "$CIX_IMAGE_REF"

```

The previously recorded local image ID is `sha256:b2cb881280c866d8b3a8be29409695f6522fa46b0207fa886e41b7d6a6a22f90`. The inspected repository digest must contain the value in `CIX_IMAGE_DIGEST`.

#### 3. Create the Container

Create an idle container with the exact W8A8 Channel repository directory from Shared Model Download mounted read-only. Use the same files as macOS; do not substitute the earlier CIX checkpoint:

```bash
export MODEL_DIR="$HOME/Models/MiniCPM5-2B-W8A8-Channel-FlagOS"
export RUN_DIR=/data/minicpm5-runtime/w8

# Repeat the release identity check immediately before mounting the model.
(cd "$MODEL_DIR" && sha256sum -c SHA256SUMS) || exit 1
(cd "$MODEL_DIR" && printf '%s  %s\n' \
  'ce27c62b10b4e7bbecbf84b7c820d3b293f9f7ff93a5963aecd785009abda905' \
  'model-00000-of-00001.safetensors' | sha256sum -c -) || exit 1

mkdir -p "$RUN_DIR/inductor" "$RUN_DIR/vllm" "$RUN_DIR/artifacts"

sudo docker run --detach \
  --name minicpm5-w8-runtime \
  --network host \
  --cpuset-cpus 0,1,6,7,8,9,10,11 \
  --entrypoint /bin/bash \
  -e MODEL=/models/minicpm5 \
  -e PORT=18041 \
  -e SERVED_MODEL_NAME=minicpm5-w8 \
  -e QUANT_MODE=w8 \
  -e TASKSET_CORES=0,1,6,7,8,9,10,11 \
  -e OMP_NUM_THREADS=8 \
  -e TORCHINDUCTOR_CACHE_DIR=/cache/inductor \
  -e VLLM_CACHE_ROOT=/cache/vllm \
  -v "$MODEL_DIR:/models/minicpm5:ro" \
  -v "$RUN_DIR/inductor:/cache/inductor" \
  -v "$RUN_DIR/vllm:/cache/vllm" \
  -v "$RUN_DIR/artifacts:/artifacts" \
  "$CIX_IMAGE_REF" -c 'exec sleep infinity'

sudo docker inspect minicpm5-w8-runtime \
  --format 'cpuset={{.HostConfig.CpusetCpus}} mounts={{json .Mounts}}'
```

Do not use `--privileged`. Do not mount empty host directories over `/var/cache/flagos/triton` or `/var/cache/flagos/kleidiai`, because doing so hides the validated caches included in the image.

#### 4. Start vLLM

Start the vLLM service through the image entry point:

```bash
sudo docker exec --detach minicpm5-w8-runtime /bin/bash -lc \
  'exec /usr/local/bin/serve-minicpm5 > /artifacts/server.log 2>&1'

ready=0
for attempt in $(seq 1 120); do
  if curl --noproxy '*' --max-time 5 -fsS http://127.0.0.1:18041/v1/models; then
    ready=1
    break
  fi
  sleep 5
done
if [ "$ready" -ne 1 ]; then
  tail -n 100 "$RUN_DIR/artifacts/server.log"
  exit 1
fi
```

The entry point ultimately runs `vllm serve` with the model mounted at `/models/minicpm5`, served model name `minicpm5-w8`, port 18041, maximum model length 8192, maximum 2048 batched tokens, one sequence, the `uni` executor and compilation mode 3.

#### 5. Send an HTTP Request

Send a request from the CIX host:

```bash
curl --noproxy '*' --fail-with-body --max-time 300 \
  http://127.0.0.1:18041/v1/chat/completions \
  -H 'Content-Type: application/json' \
  --data '{
    "model": "minicpm5-w8",
    "messages": [
      {"role": "user", "content": "Introduce FlagOS in one sentence."}
    ],
    "chat_template_kwargs": {"enable_thinking": false},
    "max_tokens": 128,
    "temperature": 0
  }' \
  | tee "$RUN_DIR/artifacts/chat-response.json"
```

#### 6. Check Kernel Coverage

Verify non-empty output and strict pure-W8 kernel coverage:

```bash
python3 - <<'PY'
import json
import os

run_dir = os.environ["RUN_DIR"]
with open(f"{run_dir}/artifacts/chat-response.json") as file:
    response = json.load(file)
with open(f"{run_dir}/artifacts/coverage.json") as file:
    coverage = json.load(file)

routes = coverage["route_stats"]
assert response["choices"][0]["message"]["content"].strip()
assert response["usage"]["completion_tokens"] > 0
assert coverage["strict"] is True
assert coverage["fallback_allowed"] is False
assert {"prefill", "decode"} <= coverage["phases"].keys()
assert coverage["attention_backend"] == "CPUAttentionBackend"
assert routes["prepared_w8_native_linears"] == 168
assert routes["prepared_w8_decode_w4_shadows"] == 0
print("CIX W8 body checks PASS; output-head and per-phase route review still required")
print(response["usage"], routes)
PY

sudo docker inspect minicpm5-w8-runtime \
  --format '{{range .Config.Env}}{{println .}}{{end}}' \
  | grep '^FLAGGEMS_CIX_P1_W8_DECODE_W4_SHADOW=0$'
```

These checks require 168 native W8 body linears and zero W4 decode shadows. They are necessary but not sufficient for release acceptance: retain the model checksums, HTTP response, full coverage JSON and server log. Verify the BF16-stored output head uses a supported W8 execution route and that both prefill and decode actually execute W8 kernels without W4 shadow or fallback. Only publish CIX performance after this exact checkpoint passes the full acceptance procedure.

#### 7. Stop the Container

Stop and remove the W8 container after validation:

```bash
sudo docker stop -t 30 minicpm5-w8-runtime
sudo docker rm minicpm5-w8-runtime
```

### Mac / M5 Pro (Native Runtime)

#### 1. Check the Mac Host and Model Files

This installation package targets Apple M5 Pro (Mac17,9). Check your Mac:

```bash
uname -m
sysctl -n hw.model
```

The expected values are `arm64` and `Mac17,9`.

Verify the downloaded model files; stop if either check fails:

```bash
(cd "$MODEL_DIR" && shasum -a 256 -c SHA256SUMS)
(cd "$MODEL_DIR" && printf '%s  %s\n' \
  'ce27c62b10b4e7bbecbf84b7c820d3b293f9f7ff93a5963aecd785009abda905' \
  'model-00000-of-00001.safetensors' | shasum -a 256 -c -)
```

#### 2. Install the Prebuilt Runtime

Use the matching **FlagOS Runtime 0.2.0-alpha.1** release files:
`install.sh`, `install.sh.sha256`,
`flagos-runtime-0.2.0-alpha.1-darwin-arm64-m5pro.tar.gz` and its
`.sha256` sidecar. Run from the directory containing these files:

```bash
shasum -a 256 -c install.sh.sha256
shasum -a 256 -c flagos-runtime-0.2.0-alpha.1-darwin-arm64-m5pro.tar.gz.sha256
bash install.sh --asset flagos-runtime-0.2.0-alpha.1-darwin-arm64-m5pro.tar.gz

export PATH="$HOME/Library/FlagOS/current/bin:$PATH"
test "$(vllm --version)" = "0.24.0+cpu"
```

This is the offline release-package installation path, with no `sudo` and no
host Python package installation. Public upload is a separate release-owner
step; the local candidate must not be replaced with the existing alpha.2
download, which contains vLLM 0.20.2. Existing release tags are immutable.

The installer validates checksums and hardware, installs below
`~/Library/FlagOS/`, and activates the selected Runtime. Paths containing
whitespace are rejected. Python, PyTorch, vLLM 0.24, FlagTree-CPU/Triton CPU,
FlagGems, vLLM-Plugin-FL, libtriton_jit and OpenMP are included. End users do
not build these components. The separate four-wheel developer wheelhouse is
not a complete standalone environment.

#### 3. Start vLLM

The packaged `vllm` launcher loads the M5 Pro profile and enables vLLM-Plugin-FL. First startup may take several minutes for imports and JIT compilation. No GPU-memory option is needed.

```bash
vllm serve "$MODEL_DIR" \
  --host 127.0.0.1 \
  --port 8000 \
  --served-model-name minicpm5-w8a8 \
  --max-model-len 8192 \
  --max-num-batched-tokens 2048 \
  --max-num-seqs 1 \
  --language-model-only \
  --generation-config vllm \
  --distributed-executor-backend uni \
  --disable-log-stats \
  --no-enable-prefix-caching \
  --compilation-config '{"mode":3}'
```

The inference path is:

```text
vllm launcher
  -> validated Apple M5 Pro profile
  -> stock vLLM 0.24.0 CPU backend with audited macOS build integration
  -> vLLM-Plugin-FL quantized Linear integration
  -> FlagGems W8 Arm kernels
  -> FlagTree-CPU / Triton CPU Arm lowering
  -> libtriton_jit, OpenMP, and native SDOT/I8MM execution
```

#### 4. Send an HTTP Request

In another terminal:

```bash
curl --noproxy '*' --fail --max-time 300 http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "minicpm5-w8a8",
    "messages": [
      {"role": "user", "content": "Introduce yourself briefly."}
    ],
    "chat_template_kwargs": {"enable_thinking": false},
    "max_tokens": 128,
    "temperature": 0.6
  }'
```

The included MiniCPM chat template accepts `enable_thinking: true` or `false` through `chat_template_kwargs`. Do not add the Qwen-specific `--reasoning-parser qwen3` option.

#### 5. Optional: Build the Runtime from Locked Source

Install Apple command-line developer tools and `uv`. With the verified
Runtime from Mac step 2 available as a compiler/Python bootstrap, unpack the
companion source package and run:

```bash
tar -xzf flagos-runtime-0.2.0-alpha.1-source.tar.gz
cd flagos-runtime-0.2.0-alpha.1-source
bash scripts/bootstrap_build_env.sh "$HOME/Library/FlagOS/current"
```

This creates an isolated Python 3.11 build environment, installs the exact
dependencies in `requirements-build.lock`, materializes the following
source commits, applies the bundled v0.24 adapter patch, compiles and
relocates native components, and produces the Runtime and wheelhouse under
`artifacts/`.

| Component | Locked source commit |
| --- | --- |
| vLLM `0.24.0+cpu` | `ee0da84ab9e04ac7610e28580af62c365e898389` |
| FlagTree-CPU / triton-cpu | `1feeab7e3505282d840e2898a1101ecff3a1c4b5` |
| FlagGems | `09c2947d702d47065f383da00187d75a70399a9b` |
| vLLM-Plugin-FL base, plus `patches/plugin-minicpm-v024.patch` | `2ccd0485ae4faba007ad0562fc00e776d67c2eed` |
| libtriton_jit | `a4eb4db996a63afe281f6ac6418182c63105d73a` |

The full URLs and Git tree IDs are in `sources.lock.json`; patch and
dependency-lock hashes are in `runtime-manifest.json`.
The build recompiles vLLM's CPU extension, libtriton_jit and the FlagGems
Arm operator bundle. It reuses the verified Triton compiler binary and
relocatable Python/OpenMP toolchain; it does **not** claim to compile Python,
PyTorch and LLVM from scratch. Detailed compiler-rebuild boundaries and
individual build/test commands are in the source package's `BUILDING.md`.

The M5 Pro profile selects vLLM 0.24's supported V1 CPU model runner and
native CPU slot-mapping metadata helper. Quantized model arithmetic remains
on the tuned FlagGems/Triton CPU SDOT/I8MM routes with strict mode enabled.

## AnythingLLM Usage Guide

1. Download and install the macOS build from the [AnythingLLM website](https://anythingllm.com/).
2. Start the FlagOS vLLM server with the command above.
3. Select the generic OpenAI-compatible provider in AnythingLLM.
4. For macOS, set the base URL to `http://127.0.0.1:8000/v1` and model name to `minicpm5-w8a8`. For CIX P1, use `http://127.0.0.1:18041/v1` and `minicpm5-w8`. Use `EMPTY` if an API key value is required.
5. Save the settings and start a new conversation after model loading completes.

## Technical Overview

### FlagOS

FlagOS is an open-source system software stack connecting models, system software, and chips through a unified workflow. This release uses one immutable, shared Runtime while distributing model weights independently.

### FlagGems

[FlagGems](https://github.com/flagos-ai/FlagGems) supplies the quantized Arm routes. On macOS, W4/W8 arithmetic is executed through Triton CPU and `libtriton_jit`; that Runtime does not embed or link KleidiAI/TLE compute kernels. The CIX image is intentionally different and combines FlagTree/Triton CPU and Inductor with CIX-gated native/KleidiAI W4/W8, attention, KV and fused paths.

### FlagTree / FlagTree-CPU

[FlagTree](https://github.com/flagos-ai/FlagTree) is the unified compiler project. This macOS Runtime uses FlagTree-CPU (the `triton-cpu` source repository) for Triton CPU code generation and Arm lowering.

The CIX image uses its separately validated Triton CPU commit and CIX P1 SVE2/I8MM/SDOT target configuration. Neither platform's binary cache or performance policy should be copied to another Arm processor without rebuilding and revalidation.

### FlagScale / vLLM-Plugin-FL

[FlagScale](https://github.com/flagos-ai/FlagScale) covers large-model training and inference workflows. [vLLM-Plugin-FL](https://github.com/flagos-ai/vllm-plugin-FL) registers the FlagOS CPU platform and connects supported compressed-tensors Linear layers to FlagGems.

### FlagCX

[FlagCX](https://github.com/flagos-ai/FlagCX) is the FlagOS cross-chip communication library. It is part of the broader FlagOS stack but is not required for this single-host CPU-only inference path.

### FlagEval

[FlagEval](https://github.com/FlagOpen/FlagEval) provides reproducible model and system evaluation workflows. Final correctness results for this exact model artifact will be published only after the complete evaluation is auditable.

## Contributing

1. Submit issues to report problems.
2. Create pull requests to contribute code.
3. Improve build and deployment documentation.
4. Expand model and hardware coverage.

## Production boundaries

- Run W4 and W8 serially on a 32 GiB CIX P1 host.
- Keep CIX strict coverage enabled and do not enable silent fallback.
- Keep `FLAGGEMS_CIX_P1_W8_DECODE_W4_SHADOW=0`; acceptance requires pure W8 decode.
- Do not apply the CIX CPU affinity, image, cache or performance numbers to Apple Silicon or another Arm CPU.
- Do not apply the M5 Pro native Runtime profile or its performance numbers to CIX P1.
- Both platforms must use the W8A8 Channel release checkpoint and SHA256 specified above. Do not reuse performance figures from the earlier CIX checkpoint file.
- Native macOS validation has passed; Linux/CIX validation and performance for the unified checkpoint remain pending.

## License

The model weights are derived from MiniCPM5-2B and remain subject to the upstream MiniCPM model license and usage terms. Runtime components remain under their respective upstream licenses; consult the Runtime third-party notices and each locked source repository before redistribution.

