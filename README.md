# AutoSkirt for Autodesk Maya

**AutoSkirt** is a free rigging and dynamic setup tool built on the **Maya Muscle** system. While designed with skirts in mind, it can be used on almost any piece of clothing or garment. 

Because pure simulation isn't always predictable, AutoSkirt gives you full manual control alongside dynamics—allowing you to easily combine **Maya Muscle simulation with traditional keyframe animation** for the best results.

## 🎥 Video Walkthrough
Watch the full step-by-step tutorial and demo on YouTube: [Insert your YouTube link here]

## 🚀 Installation & Usage

1. Download `autoSkirt.py` from this repository.
2. Copy the file into your Maya scripts directory:
   ```text
   C:\Users\<username>\Documents\maya\2026\scripts\autoSkirt.py
   ```
   *(Note: Replace `<username>` with your actual Windows user name, or use your respective Maya version folder).*
3. Open **Autodesk Maya** and launch the **Script Editor**.
4. In a **Python** tab, paste and run the following code:
   ```python
   import importlib
   import autoSkirt

   importlib.reload(autoSkirt)
   ```
5. *(Optional)* Highlight the code in the Script Editor and drag it to your custom **Shelf** using the middle mouse button to create a quick-launch button.
