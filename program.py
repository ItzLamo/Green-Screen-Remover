import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Global variables
image_path = None
background_path = None
lower_green = np.array([35, 50, 50])
upper_green = np.array([85, 255, 255])
transparency = 1.0  # Default transparency
history = []  # To store undo/redo states
history_index = -1  # Current position in history

# Function to remove green screen
def remove_green_screen(image, background, transparency=1.0):
    background = cv2.resize(background, (image.shape[1], image.shape[0]))
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
    inverse_mask = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(image, image, mask=inverse_mask)
    new_background = cv2.bitwise_and(background, background, mask=mask)
    combined = cv2.add(foreground, new_background)
    return cv2.addWeighted(combined, transparency, background, 1 - transparency, 0)

# Function to handle image upload
def upload_image():
    global image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image_path = file_path
        display_image(image_path, image_preview)
        status_label.config(text="Green screen image uploaded.")
        add_to_history()

# Function to handle background upload
def upload_background():
    global background_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        background_path = file_path
        display_image(background_path, background_preview)
        status_label.config(text="Background image uploaded.")
        add_to_history()

# Function to display images in the GUI
def display_image(file_path, label):
    image = Image.open(file_path)
    image = image.resize((250, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Function to update green color range
def update_green_range(*args):
    global lower_green, upper_green
    lower_green = np.array([hue_min.get(), sat_min.get(), val_min.get()])
    upper_green = np.array([hue_max.get(), sat_max.get(), val_max.get()])
    status_label.config(text="Green color range updated.")
    add_to_history()

# Function to update transparency
def update_transparency(*args):
    global transparency
    transparency = transparency_slider.get()
    status_label.config(text=f"Transparency set to {transparency:.2f}")
    add_to_history()

# Function to process the images
def process_images(preview=False):
    if not image_path or not background_path:
        messagebox.showerror("Error", "Please upload both images!")
        return

    status_label.config(text="Processing...")
    root.update_idletasks()

    # Load images
    image = cv2.imread(image_path)
    background = cv2.imread(background_path)

    # Remove green screen
    final_image = remove_green_screen(image, background, transparency)

    # Display the result
    display_cv2_image(final_image, result_preview)

    if not preview:
        export_image(final_image)
    else:
        status_label.config(text="Preview generated.")

# Function to export the final image
def export_image(final_image):
    file_types = [("JPEG", "*.jpg"), ("PNG", "*.png")]
    output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=file_types)
    if output_path:
        if output_path.endswith(".jpg") or output_path.endswith(".jpeg"):
            cv2.imwrite(output_path, final_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        elif output_path.endswith(".png"):
            cv2.imwrite(output_path, final_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        status_label.config(text=f"Image saved as {output_path}")

# Function to display OpenCV images in the GUI
def display_cv2_image(cv2_image, label):
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(cv2_image)
    image = image.resize((250, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

# Function to reset the application
def reset():
    global image_path, background_path, history, history_index
    image_path = None
    background_path = None
    image_label.config(text="No image selected")
    background_label.config(text="No background selected")
    image_preview.config(image=placeholder_image)
    background_preview.config(image=placeholder_image)
    result_preview.config(image=placeholder_image)
    status_label.config(text="Ready")
    hue_min.set(35)
    sat_min.set(50)
    val_min.set(50)
    hue_max.set(85)
    sat_max.set(255)
    val_max.set(255)
    transparency_slider.set(1.0)
    history = []
    history_index = -1

# Function to add current state to history
def add_to_history():
    global history, history_index
    state = {
        "image_path": image_path,
        "background_path": background_path,
        "lower_green": lower_green.copy(),
        "upper_green": upper_green.copy(),
        "transparency": transparency,
    }
    if history_index < len(history) - 1:
        history = history[: history_index + 1]  # Remove future states if undo was used
    history.append(state)
    history_index += 1
    update_undo_redo_buttons()

# Function to undo the last action
def undo():
    global history_index
    if history_index > 0:
        history_index -= 1
        restore_state(history[history_index])
        update_undo_redo_buttons()

# Function to redo the last action
def redo():
    global history_index
    if history_index < len(history) - 1:
        history_index += 1
        restore_state(history[history_index])
        update_undo_redo_buttons()

# Function to restore a state from history
def restore_state(state):
    global image_path, background_path, lower_green, upper_green, transparency
    image_path = state["image_path"]
    background_path = state["background_path"]
    lower_green = state["lower_green"]
    upper_green = state["upper_green"]
    transparency = state["transparency"]

    if image_path:
        display_image(image_path, image_preview)
    if background_path:
        display_image(background_path, background_preview)
    hue_min.set(lower_green[0])
    sat_min.set(lower_green[1])
    val_min.set(lower_green[2])
    hue_max.set(upper_green[0])
    sat_max.set(upper_green[1])
    val_max.set(upper_green[2])
    transparency_slider.set(transparency)
    status_label.config(text="State restored.")

# Function to update undo/redo buttons
def update_undo_redo_buttons():
    undo_button.config(state=tk.NORMAL if history_index > 0 else tk.DISABLED)
    redo_button.config(state=tk.NORMAL if history_index < len(history) - 1 else tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Green Screen Remover")
root.geometry("1000x800")

# Use ttk for themed widgets
style = ttk.Style()
style.configure("TButton", padding=5, font=("Helvetica", 10))
style.configure("TLabel", font=("Helvetica", 10))

# Title
title_label = ttk.Label(root, text="Green Screen Remover", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# Instructions
instructions = ttk.Label(root, text="Upload a green screen image and a background image, then click 'Process and Save'.", wraplength=800)
instructions.grid(row=1, column=0, columnspan=4, pady=10)

# Image upload section
ttk.Label(root, text="Green Screen Image:").grid(row=2, column=0, padx=10, pady=10)
image_label = ttk.Label(root, text="No image selected", foreground="blue")
image_label.grid(row=2, column=1, padx=10, pady=10)
ttk.Button(root, text="Upload Image", command=upload_image).grid(row=2, column=2, padx=10, pady=10)

ttk.Label(root, text="Background Image:").grid(row=3, column=0, padx=10, pady=10)
background_label = ttk.Label(root, text="No background selected", foreground="blue")
background_label.grid(row=3, column=1, padx=10, pady=10)
ttk.Button(root, text="Upload Background", command=upload_background).grid(row=3, column=2, padx=10, pady=10)

# Sliders for green color range
ttk.Label(root, text="Hue Min:").grid(row=4, column=0, padx=10, pady=10)
hue_min = ttk.Scale(root, from_=0, to=179, orient=tk.HORIZONTAL, command=update_green_range)
hue_min.set(35)
hue_min.grid(row=4, column=1, padx=10, pady=10)

ttk.Label(root, text="Hue Max:").grid(row=4, column=2, padx=10, pady=10)
hue_max = ttk.Scale(root, from_=0, to=179, orient=tk.HORIZONTAL, command=update_green_range)
hue_max.set(85)
hue_max.grid(row=4, column=3, padx=10, pady=10)

ttk.Label(root, text="Sat Min:").grid(row=5, column=0, padx=10, pady=10)
sat_min = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=update_green_range)
sat_min.set(50)
sat_min.grid(row=5, column=1, padx=10, pady=10)

ttk.Label(root, text="Sat Max:").grid(row=5, column=2, padx=10, pady=10)
sat_max = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=update_green_range)
sat_max.set(255)
sat_max.grid(row=5, column=3, padx=10, pady=10)

ttk.Label(root, text="Val Min:").grid(row=6, column=0, padx=10, pady=10)
val_min = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=update_green_range)
val_min.set(50)
val_min.grid(row=6, column=1, padx=10, pady=10)

ttk.Label(root, text="Val Max:").grid(row=6, column=2, padx=10, pady=10)
val_max = ttk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=update_green_range)
val_max.set(255)
val_max.grid(row=6, column=3, padx=10, pady=10)

# Transparency slider
ttk.Label(root, text="Transparency:").grid(row=7, column=0, padx=10, pady=10)
transparency_slider = ttk.Scale(root, from_=0.0, to=1.0, orient=tk.HORIZONTAL, command=update_transparency)
transparency_slider.set(1.0)
transparency_slider.grid(row=7, column=1, padx=10, pady=10)

# Buttons for processing and resetting
ttk.Button(root, text="Preview", command=lambda: process_images(preview=True)).grid(row=8, column=1, padx=10, pady=10)
ttk.Button(root, text="Process and Save", command=process_images).grid(row=8, column=2, padx=10, pady=10)
ttk.Button(root, text="Reset", command=reset).grid(row=8, column=3, padx=10, pady=10)

# Undo/Redo buttons
undo_button = ttk.Button(root, text="Undo", command=undo, state=tk.DISABLED)
undo_button.grid(row=9, column=1, padx=10, pady=10)
redo_button = ttk.Button(root, text="Redo", command=redo, state=tk.DISABLED)
redo_button.grid(row=9, column=2, padx=10, pady=10)

# Create a grey placeholder image
placeholder_image = Image.new("RGB", (250, 200), color="grey")
placeholder_photo = ImageTk.PhotoImage(placeholder_image)

# Image preview frames with labels
ttk.Label(root, text="Green Screen Image").grid(row=10, column=0, padx=10, pady=10)
image_preview = ttk.Label(root, image=placeholder_photo)
image_preview.grid(row=11, column=0, padx=10, pady=10)

ttk.Label(root, text="Background Image").grid(row=10, column=1, padx=10, pady=10)
background_preview = ttk.Label(root, image=placeholder_photo)
background_preview.grid(row=11, column=1, padx=10, pady=10)

ttk.Label(root, text="Result").grid(row=10, column=2, padx=10, pady=10)
result_preview = ttk.Label(root, image=placeholder_photo)
result_preview.grid(row=11, column=2, padx=10, pady=10)

# Status bar
status_label = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
status_label.grid(row=12, column=0, columnspan=4, sticky=tk.W+tk.E, padx=10, pady=10)

# Run the application
root.mainloop()