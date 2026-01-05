# Application integration

FlagCX integrates with upper-layer applications such as [PyTorch](https://pytorch.org/) and
[PaddlePaddle](https://github.com/PaddlePaddle/).
The table below lists the frameworks supported by FlagCX and their related communication operations,
where the `batch_XXX` and `XXX_coalesced` ops refer to the usage of group primitives.

| Framework                        | PyTorch                      | PaddlePaddle |
| :------------------------------- | :--------------------------- | :----------- |
| send                             | ✓                            | ✓            |
| recv                             | ✓                            | ✓            |
| all_gather                       | ✓                            | ✓            |
| all_gather_into_tensor_coalesced | ✓ (in order, no aggregation) | ☓            |
| all_reduce                       | ✓                            | ✓            |
| all_reduce_coalesced             | ✓ (in order, no aggregation) | ☓            |
| all_to_all                       | ✓                            | ✓            |
| all_to_all_single                | ✓                            | ✓            |
| barrier                          | ✓                            | ✓            |
| batch_isend_irecv                | ✓                            | ✓            |
| broadcast                        | ✓                            | ✓            |
| gather                           | ✓                            | ✓            |
| reduce                           | ✓                            | ✓            |
| reduce_scatter                   | ✓                            | ✓            |
| reduce_scatter_tensor_coalesced  | ✓ (in order, no aggregation) | ☓            |
| scatter                          | ✓                            | ✓            |

Note that PyTorch support is enabled via the FlagCX Torch plugin, which provides native integration with the PyTorch distributed backend.
This plugin has undergone comprehensive validation across diverse communication backends and hardware platforms,
ensuring robust functionality, consistent performance, and compatibility in multi-chip heterogeneous environments.

| FlagCX Backend  | NCCL | IXCCL | CNCL | MCCL | XCCL | DUCCL | HCCL | MUSACCL | RCCL |
| :-------------- | :--- | :---- | :--- | :--- | :--- | :---- | :--- | :------ | :--- |
| PyTorch Support | ✓    | ✓     | ✓    | ✓    | ✓    | ✓     | ✓    | ✓       | ✓    |


```{tip}
To enable heterogeneous cross-chip communication using the PyTorch DDP FlagCX backend,
it is recommended to use identical PyTorch versions across all nodes.
Mismatched versions may lead to initialization failures during process group setup.
Helpful advice for doing things better or more easily.
```
