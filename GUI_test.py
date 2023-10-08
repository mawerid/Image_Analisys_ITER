import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.image_label = tk.Label(root)
        self.image_label.pack(padx=10, pady=10)

        self.load_button = tk.Button(root, text="Open Directory", command=self.load_directory)
        self.load_button.pack(pady=10)

        # Store a list of loaded images and the current image index
        self.images = []
        self.current_image_index = -1

        # Navigation buttons
        self.prev_button = tk.Button(root, text="Previous", command=self.show_previous_image)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button = tk.Button(root, text="Next", command=self.show_next_image)
        self.next_button.pack(side=tk.LEFT)

    def load_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            image_files = [f for f in os.listdir(directory_path) if f.lower().endswith((".jpg", ".png", ".gif", ".bmp", ".jpeg"))]
            self.images = []

            for image_file in image_files:
                image_path = os.path.join(directory_path, image_file)
                image = Image.open(image_path)

                # Resize images if necessary
                max_width = 800
                max_height = 600
                width, height = image.size
                if width > max_width or height > max_height:
                    ratio = min(max_width / width, max_height / height)
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    image = image.resize((new_width, new_height), Image.ANTIALIAS)

                photo = ImageTk.PhotoImage(image)
                self.images.append((image, photo))

            if self.images:
                self.current_image_index = 0
                self.show_current_image()

    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.images):
            image, photo = self.images[self.current_image_index]
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_current_image()

    def show_next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_current_image()

    # Placeholder for your ML algorithm integration
    def run_ml_algorithm(self):
        if self.current_image_index >= 0:
            image, _ = self.images[self.current_image_index]
            # Implement your ML algorithm here using 'image'

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()
