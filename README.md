# AutoSkirt

### Hybrid dynamic garment rigging for Autodesk Maya

**Availability:** Free to download  
**Technology:** Maya Muscle

## Overview

AutoSkirt is a custom rigging and dynamic setup tool for Autodesk Maya, built on the native Maya Muscle system.

Originally designed for skirt rigging, the tool can also be adapted to various types of clothing and garments.

Pure simulation is not always predictable or suitable for every animation scenario. AutoSkirt addresses this challenge by combining dynamic behavior with traditional keyframe animation, allowing artists to maintain creative control over the final result.

The goal is to simplify garment rigging while providing a flexible, artist-friendly animation workflow.

## Key Features

- Automated garment rigging setup
- Native Maya Muscle integration
- Dynamic garment behavior
- Collision-based interaction
- Manual animation controls
- Hybrid dynamic and keyframe animation workflow
- Support for secondary garment motion
- Adaptable setup for different garment types
- Quick access through a custom Maya shelf button

## Video Demonstration

[![AutoSkirt Video Demonstration](https://img.youtube.com/vi/aDL0SH53vbA/0.jpg)](https://youtu.be/aDL0SH53vbA)

[Watch the full step-by-step tutorial on YouTube](https://youtu.be/aDL0SH53vbA)

## Download

[Download autoSkirt.py](https://github.com/betonlufi/autoSkirt/raw/refs/heads/main/autoSkirt.py)

## Compatibility

- Autodesk Maya
- Python 3
- Maya Muscle (cMuscle)
- Windows installation workflow

The Maya Muscle plug-in must be available in your Maya installation.

Compatibility with individual Maya versions and other operating systems may vary.

## Installation

1. Download `autoSkirt.py` from this repository.
2. Copy the Python file into your Maya user scripts directory.

The default location on Windows is typically:

```text
Documents/maya/<version>/scripts/
```

Replace `<version>` with your installed Maya version.

3. Open Autodesk Maya.
4. Make sure the Maya Muscle plug-in is available and loaded.
5. Open the Script Editor and select the Python tab.
6. Run the following code:

```python
import importlib
import autoSkirt

importlib.reload(autoSkirt)
```

## Creating a Shelf Button

For quick access to the tool:

1. Select the launcher code in the Python Script Editor.
2. Drag the selected code onto your custom Maya shelf using the middle mouse button.
3. Use the newly created shelf button to launch AutoSkirt.

## Workflow

AutoSkirt is designed around three complementary animation approaches:

### Dynamic Animation

Use Maya Muscle dynamics and collision-based interaction to generate secondary garment motion.

### Manual Animation

Use traditional animation controls and keyframes to achieve specific poses, silhouettes, and art-directed movement.

### Hybrid Animation

Combine dynamic behavior with manual animation to balance natural secondary motion with artistic control.

For detailed setup instructions and a complete workflow demonstration, follow the step-by-step video tutorial above.

## Use Cases

- Skirt and dress rigging
- Character clothing deformation
- Secondary garment animation
- Dynamic clothing setups with manual adjustments
- Art-directed garment movement
- Character rigs requiring both dynamic and keyframe animation

## Design Philosophy

Simulation should support the animator, not limit creative control.

AutoSkirt is designed to provide a practical balance between automated secondary motion and direct artistic control, using Maya's existing rigging and dynamic systems.

## Important

Always save a backup of your scene before modifying an existing character rig.

Test the tool in a disposable scene before integrating it into a production workflow.

## Author

**Zoltan Vass**  
Character TD | Technical Artist | Maya Tools Developer

- [GitHub Profile](https://github.com/betonlufi)
- [LinkedIn](https://www.linkedin.com/in/zoli-vass-aaa9913a/)
- [Professional Showreel](https://youtu.be/Hp-Coxo68zo)
