# Training models with paddle and FlagCX

FlagCX is now fully integrated into Paddle as an **optional high-performance communication backend**. This integration enables efficient distributed training on multiple hardware platforms, including support for **heterogeneous training** on Nvidia and Iluvatar GPUs.  

Use the guides below to quickly get started with training models using Paddle + FlagCX.

## Homogeneous training

Train on a single type of hardware platform:

| Hardware        | User Guide |
|:---------------:|:----------|
| Nvidia GPU      | [](nvidia.md) |
| Kunlunxin XPU   | [](kunlun.md) |
| Iluvatar GPU    | [](iluvatar.md) |

## Heterogeneous training

Train across **different hardware platforms** simultaneously:

| Hardware Combination         | User Guide |
|:----------------------------:|:----------|
| Nvidia GPU + Iluvatar GPU    | [](nvidia_iluvatar_hetero_train.md) |

```{toctree}
:maxdepth: 3

nvidia
iluvatar
kunlun
nvidia_iluvatar_hetero_train
```
