# v0.4.0

**Added Features**

- Added new low-level DSL- tle
  The new DSL-tle (Triton Language Extension) extends fundamental primitives for both GPUs and DSAs respectively. Ameng them, achieved 20% performance improvement on add compared to the standard Triton.
- Unified backend specialization for GPGPU and DSA/NPU
  The unified backend specialization is applied to ILUVATAR and Huawei Ascend.
- Added new access backend
  enflame is added.
**Changed Features**
- Enhanced the unified intermediate representation layer for DSA architecture chips
  The unified IR layer has been validated on Ascend and AIPU.
- Upgraded C++ runtime to multi-chip architecture
     Nvidia, Huawei Ascend, Moore Threads, and ILUVATAR are supported.
- Developer experience improvements
  The improvements include the following:
  - Provided pre-download and offline installation mode
  - Provided the installation method via PyPI
  - Migrated related dependencies SDK to Kingsoft Cloud
