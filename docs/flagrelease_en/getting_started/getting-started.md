# Getting Started

This section covers general steps from downloading open-source model weights to deploying and executing models:

The outputs of FlagRelease include validated large-model files and integrated FlagOS Docker images. By using these artifacts, users can rapidly deploy and run large models on different hardware platforms without performing model migration themselves or configuring complex software environments.

General workflow

1. Download open-source model weights
    Visit the FlagRelease pages on ModelScope or Hugging Face, select the required large model and the corresponding hardware-specific version, and download the model weight files directly
2. Download the FlagOS Image
   Obtain the officially provided integrated FlagOS Docker image, which includes the unified software stack and built-in hardware adaptation support.
3. Deployment and execution
   - Combine the downloaded model weights with the FlagOS image to run the model directly on the target hardware.
   - FlagOS automatically manages hardware resources and supports multi-chip parallel execution, eliminating the need for manual environment configuration.

For model specific installation and deployment, click the URLs listed in the [Release Notes](/release_notes/) and follow the steps demonstrated in model main page.
