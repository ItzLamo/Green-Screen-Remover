# Green Screen Remover

## Overview
The **Green Screen Remover** is a Python app that removes green backgrounds from images and replaces them with custom backgrounds. It features a user-friendly interface for uploading images, adjusting settings, and exporting results.

---

## Features
- Remove green backgrounds using chroma keying.
- Replace the green screen with a custom background.
- Adjust green screen range (Hue, Saturation, Value) and transparency.
- Preview the result before saving.
- Undo/Redo changes.
- Export images in JPEG or PNG format.
- Responsive design for different screen sizes.

---

## Requirements
Install the required libraries:
```bash
pip install opencv-python numpy Pillow
```

---

## How to Use
1. **Upload Images**:
   - Click **Upload Image** for the green screen image.
   - Click **Upload Background** for the background image.

2. **Adjust Settings**:
   - Use sliders to fine-tune the green screen range and transparency.

3. **Preview and Save**:
   - Click **Preview** to see the result.
   - Click **Process and Save** to export the final image.

4. **Undo/Redo**:
   - Use **Undo** and **Redo** to revert or reapply changes.

5. **Reset**:
   - Click **Reset** to clear all inputs.

---

## Code Structure
- **Tkinter**: For the GUI.
- **OpenCV**: For image processing.
- **Pillow**: For image manipulation.

---

## Example
1. Upload a green screen image.
2. Upload a background image.
3. Adjust sliders for the best result.
4. Preview and save the final image.

---

Enjoy using the Green Screen Remover App! 🚀
