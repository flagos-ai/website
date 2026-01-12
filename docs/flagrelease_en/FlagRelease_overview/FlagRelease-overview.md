# FlagGems Overview

FlagRelease is a platform dedicated to the automatic migration, adaptation and release of large models for multi-architecture AI chips. FlagRelease aims to enable mainstream large models to be migrated, validated, and released on diverse domestic AI hardware with lower cost and higher efficiency through automated, standardized, and intelligent adaptation workflows.

Built upon the unified and open-source AI system software stack FlagOS, which provides cross-hardware adaptation capabilities, FlagRelease establishes a standardized pipeline that supports automatic migration of large models to different hardware architectures, automated evaluation of migration results, built-in automated deployment and tuning, and multi-chip model packaging and release.

The artifacts released through the FlagRelease platform are published on [ModelScope](https://modelscope.cn/organization/FlagRelease?tab=model) and [Hugging Face](https://huggingface.co/FlagRelease) under the FlagRelease organization, where users can obtain different hardware-specific versions of open-source large models. These models can be downloaded and used directly on the corresponding hardware environments without requiring users to perform model migration themselves, significantly reducing the migration cost for end users.

Currently, the outputs of the FlagRelease platform include validated, hardware-adapted model files and integrated Docker images. Each image contains the core components of FlagOS along with all required model dependencies, allowing users to deploy and use the models directly on the target chips. In addition, each model release provides evaluation results as technical references, enabling users to clearly understand the model’s correctness and performance characteristics across different hardware platforms.

Furthermore, every released model is accompanied by configuration and usage instructions for AnythingLLM, helping users quickly verify the availability of the migrated models and facilitating downstream development and application based on these models.

Typical scenarios:

You may use FlagRelease for quick deployment and execution in the following scenarios:

- Research and experimentation: rapidly deploy large models for inference without concern for underlying hardware differences.
- Production environments: directly deploy hardware-specific versions of models as services, ensuring performance and stability across different AI chips.