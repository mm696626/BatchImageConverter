import tkinter as tk
from tkinter import filedialog

import batchConvert


def browse_folder(entry_widget):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)

def perform_action():
    image_folder = image_folder_path.get()
    output_folder = output_folder_path.get()
    batchConvert.batch_convert(image_folder, output_folder)

# Set up the main window
root = tk.Tk()
root.title("Wii Photo Channel Image Converter")

image_folder_label = tk.Label(root, text="Image Folder:")
image_folder_label.grid(row=0, column=0, padx=10, pady=10)

image_folder_path = tk.Entry(root, width=40)
image_folder_path.grid(row=0, column=1, padx=10, pady=10)

image_folder_browse = tk.Button(root, text="Browse", command=lambda: browse_folder(image_folder_path))
image_folder_browse.grid(row=0, column=2, padx=10, pady=10)

output_folder_label = tk.Label(root, text="Output Folder")
output_folder_label.grid(row=1, column=0, padx=10, pady=10)

output_folder_path = tk.Entry(root, width=40)
output_folder_path.grid(row=1, column=1, padx=10, pady=10)

output_folder_browse = tk.Button(root, text="Browse", command=lambda: browse_folder(output_folder_path))
output_folder_browse.grid(row=1, column=2, padx=10, pady=10)

convert_button = tk.Button(root, text="Convert", command=perform_action)
convert_button.grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
