---
license: apache-2.0
---
<div align="center">
<img src="https://github.com/FlagOpen/RoboBrain2.5/raw/main/assets/logo2.png" width="500"/>
</div>

<h1 align="center">RoboBrain 2.5: Depth in Sight, Time in Mind. </h1>

<p align="center">
        </a>&nbsp&nbsp⭐️ <a href="https://superrobobrain.github.io/">Project Page</a></a>&nbsp&nbsp | &nbsp&nbsp🤗 <a href="https://huggingface.co/collections/BAAI/robobrain25/">Hugging Face</a>&nbsp&nbsp | &nbsp&nbsp🤖 <a href="https://github.com/FlagOpen/RoboBrain2.5">Github</a>&nbsp&nbsp 
</p>

## 🔥 Overview
**RoboBrain-2.5** is a next-generation Embodied AI foundation model that significantly evolves its predecessor's core capabilities in general perception, spatial reasoning, and temporal modeling through extensive training on high-quality spatiotemporal data. It achieves a paradigm shift in 3D Spatial Reasoning, transitioning from 2D relative points to predicting 3D coordinates with depth information, understanding absolute metric constraints, and generating complete manipulation trajectories tailored for complex tasks with physical constraints. Furthermore, it establishes a breakthrough in Temporal Value Prediction by constructing a General Reward Modeling Method that provides dense progress tracking and multi-granular execution state estimation across varying viewpoints. This empowers VLA reinforcement learning with immediate, dense feedback signals, enabling robots to achieve high task success rates and robustness in fine-grained manipulation scenarios.

<div align="center">
<img src="https://github.com/FlagOpen/RoboBrain2.5/raw/main/assets/rb25_feature.png" />
</div>

<div align="center">
<img src="https://github.com/FlagOpen/RoboBrain2.5/raw/main/assets/rb25_result.png" />
</div>

## 🚀 Key Highlights

### 1. Comprehensive Upgrade in ✨ Native 3D Spatial Reasoning ✨ 
Compared to version 2.0, **RoboBrain-2.5** achieves a leap in spatial perception and reasoning capabilities:
*   **From 2D to 3D:** Upgraded from predicting coordinate points on 2D images to predicting coordinate points with depth information in **3D space** (3D Spatial Referring).
*   **Relative to Absolute:** Evolved from understanding relative spatial relationships to measuring **absolute 3D spatial metric information** (3D Spatial Measuring). The model can comprehend precise physical constraint instructions (e.g., "hovering 1-5 cm above").
*   **Point to Trace:** Advanced from predicting a single target point for pick-and-place to predicting a **series of key points** that describe the complete manipulation process (3D Spatial Trace), naturally possessing spatial planning capabilities with 3D absolute metrics.


### 2. Breakthrough in ✨ Dense Temporal Value Estimation ✨ 
**RoboBrain-2.5** makes significant progress in temporal modeling by constructing a General Reward Model (GRM):
*   **Dense Progress Prediction:** Capable of multi-granularity task progress prediction across different tasks, viewpoints, and embodiments.
*   **Execution State Estimation:** Understands task goals and estimates various states during execution (e.g., success, failure, error occurrence).
*   **Empowering VLA Reinforcement Learning:** Provides real-time, dense feedback signals and rewards for VLA (Vision-Language-Action) reinforcement learning. With only **one demonstration**, it achieves a task success rate of **95%+** in complex, fine-grained manipulations.

### 3. More Powerful Core Capabilities from previous version 2.0
**RoboBrain 2.5** also maintains the three core capabilities of version 2.0, which supports ***interactive reasoning*** with long-horizon planning and closed-loop feedback, ***spatial perception*** for precise point and bbox prediction from complex instructions, ***temporal perception*** for future trajectory estimation, and ***scene reasoning*** through real-time structured memory construction and update.

## 🛠️ Setup

```bash
# clone repo.
git clone https://github.com/FlagOpen/RoboBrain2.5.git
cd RoboBrain2.5

# build conda env.
conda create -n robobrain2_5 python=3.10
conda activate robobrain2_5
pip install -r requirements.txt
```


## 💡 Quickstart

### 1. Usage for General VQA
```python
from inference import UnifiedInference

model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# Example:
prompt = "What is shown in this image?"
image = "http://images.cocodataset.org/val2017/000000039769.jpg"

pred = model.inference(prompt, image, task="general")
print(f"Prediction:\n{pred}")
```

### 2. Usage for Visual Grounding (VG)
```python
from inference import UnifiedInference

model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# Example:
prompt = "the person wearing a red hat"
image = "./assets/demo/grounding.jpg"

# Visualization results will be saved to ./result, if `plot=True`.
pred = model.inference(prompt, image, task="grounding", plot=True, do_sample=False)
print(f"Prediction:\n{pred}")
```

### 3. Usage for Affordance Prediction (Embodied)
```python
from inference import UnifiedInference

model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# Example:
prompt = "the affordance area for holding the cup"
image = "./assets/demo/affordance.jpg"

# Visualization results will be saved to ./result, if `plot=True`.
pred = model.inference(prompt, image, task="pointing", plot=True, do_sample=False)
print(f"Prediction:\n{pred}")
```

### 4. Usage for Refering Prediction (Embodied)
```python
from inference import UnifiedInference

model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# Example:
prompt = "Identify spot within the vacant space that's between the two mugs"
image = "./assets/demo/pointing.jpg"

# Visualization results will be saved to ./result, if `plot=True`.
pred = model.inference(prompt, image, task="pointing", plot=True, do_sample=True)
print(f"Prediction:\n{pred}")
```

### 5. Usage for Navigation Tasks (Embodied)
```python
from inference import UnifiedInference

model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# Example 1:
prompt_1 = "Identify spot within toilet in the house"
image = "./assets/demo/navigation.jpg"

# Visualization results will be saved to ./result, if `plot=True`.
pred = model.inference(prompt_1, image, task="pointing", plot=True, do_sample=True)
print(f"Prediction:\n{pred}")

# Example 2:
prompt_2 = "Identify spot within the sofa in the house"
image = "./assets/demo/navigation.jpg"

# Visualization results will be saved to ./result, if `plot=True`.
pred = model.inference(prompt_2, image, task="pointing", plot=True, do_sample=True)
print(f"Prediction:\n{pred}")
```

### 6. Usage for ✨ 3D Trajectory Prediction ✨ (Embodied)
```python
from inference import UnifiedInference

model = UnifiedInference("BAAI/RoboBrain2.5-8B-NV")

# Example:
prompt = "reach for the banana on the plate"
image = "./assets/demo/trajectory.jpg"

# Visualization results will be saved to ./result, if `plot=True`.
pred = model.inference(prompt, image, task="trajectory", plot=True, do_sample=False)
print(f"Prediction:\n{pred}")
```

### 7. Usage for ✨ Temporal Value Estimation ✨ (Embodied)
***We highly recommend referring to [Robo-Dopamine](https://github.com/FlagOpen/Robo-Dopamine) for detailed usage instructions.***
```bash
# clone Robo-Dopamine repo.
git clone https://github.com/FlagOpen/Robo-Dopamine.git
cd Robo-Dopamine
```
```python
import os
from examples.inference import GRMInference

# model = GRMInference("tanhuajie2001/Robo-Dopamine-GRM-3B")
model = GRMInference("BAAI/RoboBrain2.5-8B-NV")

TASK_INSTRUCTION = "organize the table"
BASE_DEMO_PATH = "./examples/demo_table"
GOAL_IMAGE_PATH = "./examples/demo_table/goal_image.png" 
OUTPUT_ROOT = "./results"

output_dir = model.run_pipeline(
    cam_high_path  = os.path.join(BASE_DEMO_PATH, "cam_high.mp4"),
    cam_left_path  = os.path.join(BASE_DEMO_PATH, "cam_left_wrist.mp4"),
    cam_right_path = os.path.join(BASE_DEMO_PATH, "cam_right_wrist.mp4"),
    out_root       = OUTPUT_ROOT,
    task           = TASK_INSTRUCTION,
    frame_interval = 30,
    batch_size     = 1,
    goal_image     = GOAL_IMAGE_PATH,
    eval_mode      = "incremental",
    visualize      = True
)

print(f"Episode ({BASE_DEMO_PATH}) processed with Incremental-Mode. Output at: {output_dir}")

```
