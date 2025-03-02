import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
import batchConvert
import os


def browse_folder(entry_widget):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_widget.config(state=tk.NORMAL)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)
        entry_widget.config(state=tk.DISABLED)


def browse_files(entry_widget):
    files_selected = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.webp *.heic *.heif *.gif")])
    if files_selected:
        entry_widget.config(state=tk.NORMAL)
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ', '.join(files_selected))
        entry_widget.config(state=tk.DISABLED)


def save_default_output_path():
    folder_selected = filedialog.askdirectory(title="Select Default Output Path")
    if folder_selected:
        with open("default_output_path.txt", "w") as file:
            file.write(folder_selected)
            output_folder_path.config(state=tk.NORMAL)
            output_folder_path.delete(0, tk.END)
            output_folder_path.insert(0, folder_selected)
            output_folder_path.config(state=tk.DISABLED)
            messagebox.showinfo("Saved", "Default output path has been saved.")
    else:
        messagebox.showwarning("Invalid Input", "Please select an output folder first.")


def load_default_output_path():
    if os.path.exists("default_output_path.txt"):
        with open("default_output_path.txt", "r") as file:
            saved_path = file.read().strip()
            output_folder_path.config(state=tk.NORMAL)
            output_folder_path.delete(0, tk.END)
            output_folder_path.insert(0, saved_path)
            output_folder_path.config(state=tk.DISABLED)


def remove_default_output_path():
    if os.path.exists("default_output_path.txt"):
        os.remove("default_output_path.txt")
        output_folder_path.config(state=tk.NORMAL)
        output_folder_path.delete(0, tk.END)
        output_folder_path.config(state=tk.DISABLED)
        messagebox.showinfo("Removed", "Default output path has been removed.")
    else:
        messagebox.showerror("Error", "No default output path exists.")

def clear_output_folder_path(output_folder):
    output_folder_path.config(state=tk.NORMAL)
    if os.path.exists("default_output_path.txt"):
        with open("default_output_path.txt", "r") as file:
            default_output_path = file.read().strip()

        if os.path.abspath(output_folder) != os.path.abspath(default_output_path):
            output_folder_path.delete(0, tk.END)

    else:
        output_folder_path.delete(0, tk.END)
    output_folder_path.config(state=tk.DISABLED)

def convert_image_folder():
    image_folder = image_folder_path.get()
    output_folder = output_folder_path.get()
    delete_original = delete_checkbox_var.get()
    output_format = format_var.get()
    wii_photo_channel_size_limit = resize_checkbox_var.get()

    if not image_folder or not output_folder:
        messagebox.showerror("Invalid Input", "An image folder and output folder must be given!")
        return

    batchConvert.convert_folder(image_folder, output_folder, output_format, wii_photo_channel_size_limit)

    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".heic", ".heif", ".gif"}

    if delete_original:
        for filename in os.listdir(image_folder):
            file_path = os.path.join(image_folder, filename)
            file_extension = os.path.splitext(filename)[1].lower()
            if os.path.isfile(file_path) and file_extension in image_extensions:
                os.remove(file_path)

    messagebox.showinfo("Done", "Conversion Complete!")

    image_folder_path.config(state=tk.NORMAL)
    image_folder_path.delete(0, tk.END)
    image_folder_path.config(state=tk.DISABLED)
    clear_output_folder_path(output_folder)

def convert_image_files():
    image_files = image_file_path.get()
    output_folder = output_folder_path.get()
    delete_original = delete_checkbox_var.get()
    output_format = format_var.get()
    wii_photo_channel_size_limit = resize_checkbox_var.get()

    if not image_files or not output_folder:
        messagebox.showerror("Invalid Input", "Images and output folder must be given!")
        return

    image_files = image_files.split(", ")
    batchConvert.convert_images(image_files, output_folder, output_format, wii_photo_channel_size_limit)

    if delete_original:
        for file in image_files:
            if os.path.exists(file):
                os.remove(file)

    messagebox.showinfo("Done", "Conversion Complete!")

    image_file_path.config(state=tk.NORMAL)
    image_file_path.delete(0, tk.END)
    clear_output_folder_path(output_folder)
    image_file_path.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Batch Image Converter")
icon = PhotoImage(file='images/photo-channel-icon.png')
root.iconphoto(True, icon)

image_folder_label = tk.Label(root, text="Input Image Folder")
image_folder_label.grid(row=0, column=0, padx=10, pady=10)

image_folder_path = tk.Entry(root, width=40)
image_folder_path.grid(row=0, column=1, padx=10, pady=10)
image_folder_path.config(state=tk.DISABLED)

image_folder_browse = tk.Button(root, text="Browse Folder", command=lambda: browse_folder(image_folder_path))
image_folder_browse.grid(row=0, column=2, padx=10, pady=10)

image_file_label = tk.Label(root, text="Input Image Files")
image_file_label.grid(row=1, column=0, padx=10, pady=10)

image_file_path = tk.Entry(root, width=40)
image_file_path.grid(row=1, column=1, padx=10, pady=10)
image_file_path.config(state=tk.DISABLED)

image_file_browse = tk.Button(root, text="Browse Files", command=lambda: browse_files(image_file_path))
image_file_browse.grid(row=1, column=2, padx=10, pady=10)

output_folder_label = tk.Label(root, text="Output Image Folder")
output_folder_label.grid(row=2, column=0, padx=10, pady=10)

output_folder_path = tk.Entry(root, width=40)
output_folder_path.grid(row=2, column=1, padx=10, pady=10)
output_folder_path.config(state=tk.DISABLED)

output_folder_browse = tk.Button(root, text="Browse", command=lambda: browse_folder(output_folder_path))
output_folder_browse.grid(row=2, column=2, padx=10, pady=10)

format_label = tk.Label(root, text="Select Output Format")
format_label.grid(row=3, column=0, padx=10, pady=10)

format_var = tk.StringVar()
format_var.set("JPEG Baseline")

formats = ["JPEG Baseline", "JPEG Progressive", "PNG"]
format_dropdown = tk.OptionMenu(root, format_var, *formats)
format_dropdown.grid(row=3, column=1, padx=10, pady=10)

delete_checkbox_var = tk.BooleanVar()
delete_checkbox = tk.Checkbutton(root, text="Delete Original Images After Conversion", variable=delete_checkbox_var)
delete_checkbox.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

resize_checkbox_var = tk.BooleanVar(value=True)
resize_checkbox = tk.Checkbutton(root, text="Convert Images Within the Wii Photo Channel's Size Limit (8192x8192)", variable=resize_checkbox_var)
resize_checkbox.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

convert_folder_button = tk.Button(root, text="Convert Folder", command=convert_image_folder)
convert_folder_button.grid(row=6, column=0, columnspan=1, pady=20)

convert_files_button = tk.Button(root, text="Convert Files", command=convert_image_files)
convert_files_button.grid(row=6, column=1, columnspan=1, pady=20)

save_default_button = tk.Button(root, text="Save Default Output Folder Path", command=save_default_output_path)
save_default_button.grid(row=7, column=0, columnspan=1, pady=20)

remove_default_button = tk.Button(root, text="Remove Default Output Folder Path", command=remove_default_output_path)
remove_default_button.grid(row=7, column=1, columnspan=1, pady=20)

reload_default_button = tk.Button(root, text="Reload Default Output Folder Path", command=load_default_output_path)
reload_default_button.grid(row=7, column=2, columnspan=1, pady=20)

load_default_output_path()

root.mainloop()
