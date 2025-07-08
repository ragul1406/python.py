import os
from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")
        self.root.geometry("500x400")
        self.images = []

        self.init_gui()

    def init_gui(self):
        Label(self.root, text="Image Converter", font=("Arial", 20)).pack(pady=10)

        Button(self.root, text="Select Images", command=self.select_images).pack(pady=5)
        Button(self.root, text="Choose Output Folder", command=self.select_output_folder).pack(pady=5)

        Label(self.root, text="Choose Format").pack()
        self.format_var = StringVar(self.root)
        self.format_var.set("PNG")
        OptionMenu(self.root, self.format_var, "PNG", "JPG", "BMP", "GIF").pack(pady=5)

        Label(self.root, text="Resize (width x height)").pack()
        self.width_entry = Entry(self.root, width=10)
        self.width_entry.pack()
        self.height_entry = Entry(self.root, width=10)
        self.height_entry.pack()

        Label(self.root, text="JPEG Compression Quality (1-100)").pack()
        self.quality_entry = Entry(self.root, width=10)
        self.quality_entry.insert(0, "85")
        self.quality_entry.pack()

        Button(self.root, text="Convert Images", command=self.convert_images).pack(pady=20)

    def select_images(self):
        self.images = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if self.images:
            messagebox.showinfo("Selected", f"{len(self.images)} images selected.")

    def select_output_folder(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            messagebox.showinfo("Output Folder", f"Images will be saved to:\n{self.output_dir}")

    def convert_images(self):
        if not self.images:
            messagebox.showerror("Error", "No images selected.")
            return
        if not hasattr(self, 'output_dir'):
            messagebox.showerror("Error", "No output folder selected.")
            return

        format_selected = self.format_var.get().upper()
        try:
            width = int(self.width_entry.get()) if self.width_entry.get() else None
            height = int(self.height_entry.get()) if self.height_entry.get() else None
            quality = int(self.quality_entry.get()) if self.quality_entry.get() else 85

            for img_path in self.images:
                try:
                    with Image.open(img_path) as img:
                        if width and height:
                            img = img.resize((width, height))

                        filename = os.path.splitext(os.path.basename(img_path))[0]
                        output_path = os.path.join(self.output_dir, f"{filename}.{format_selected.lower()}")

                        if format_selected == "JPG":
                            img = img.convert("RGB")  # Ensure no alpha channel
                            img.save(output_path, format_selected, quality=quality)
                        else:
                            img.save(output_path, format_selected)

                except Exception as e:
                    messagebox.showwarning("Conversion Error", f"Failed to convert {img_path}.\n{str(e)}")

            messagebox.showinfo("Success", "All images converted successfully!")

        except ValueError:
            messagebox.showerror("Input Error", "Invalid width, height, or quality value.")

if __name__ == "__main__":
    root = Tk()
    app = ImageConverterApp(root)
    root.mainloop()
