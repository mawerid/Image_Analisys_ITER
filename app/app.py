import os
import numpy as np
import cv2 as cv
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt

from model.model import run, graph
matplotlib.use("TkAgg")


class App(tk.Tk):
    """
    Класс для создания главного окна приложения
    """

    def __init__(self):
        """
        Конструктор класса
        """
        super().__init__()
        self._started = 0
        self.title("Graph Illustration")
        self.geometry("1440x700")
        self.current_image_index = -1
        self.image_files = []

    def load_directory(self, entry):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.image_files = [f for f in os.listdir(self.directory_path) if f.lower(
            ).endswith((".jpg", ".png", ".gif", ".bmp", ".jpeg"))]
            print(self.image_files)

            if self.image_files:
                self.current_image_index = 0
                self.show_current_image()

        entry.delete(0, tk.END)
        entry.insert(0, self.directory_path)

    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = os.path.join(
                self.directory_path, self.image_files[self.current_image_index])
            print(image_path)
            image = cv.imread(image_path)
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            self.image_shape = image.shape

            image_copy = image.copy()
            photo = self.prepare_image(image)

            self.image1_label.config(image=photo)
            self.image1_label.image = photo

            conv_image, self.resolution, self.scale = self.run_ml_algorithm(
                image_copy)

            conv_photo = self.prepare_image(conv_image)

            self.image2_label.config(image=conv_photo)
            self.image2_label.image = conv_photo

            self.info_value1.config(text=self.info_label1.cget(
                "text") + self.image_files[self.current_image_index])
            self.info_value1.text = self.info_label1.cget(
                "text") + self.image_files[self.current_image_index]
            self.info_value2.config(
                text=self.info_label2.cget("text") + str(self.image_shape))
            self.info_value2.text = self.info_label2.cget(
                "text") + str(self.image_shape)
            self.info_value3.config(text=self.info_label3.cget(
                "text") + (str(self.resolution) + self.scale))
            self.info_value3.text = self.info_label3.cget(
                "text") + (str(self.resolution) + self.scale)

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_current_image()

    def show_next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_current_image()

    def prepare_image(self, image: np.ndarray) -> ImageTk.PhotoImage:
        if type(image) != np.ndarray:
            return None

        if image.shape != (512, 572):
            image = cv.resize(
                image, (512, 572), interpolation=cv.INTER_AREA)

        image = Image.fromarray(image)
        return ImageTk.PhotoImage(image)

    def run_ml_algorithm(self, image) -> Tuple[np.ndarray, int, str]:
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_files):
            return run(image, self.image_files[self.current_image_index])

    def draw_graph(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_files):
            graph(self.image_files[self.current_image_index])
            plt.show()

    def drawfront(self):

        # Left part of the window
        self.left_frame = ttk.Frame(self, padding=(7, 7), relief="solid")
        self.left_frame.grid(row=0, column=0, rowspan=15,
                             padx=(2, 2), pady=(2, 2), sticky='nsew')

        # Image area
        self.current_image_index = -1

        # Navigation buttons
        self.nav_frame = ttk.Frame(self.left_frame, padding=(5, 5))
        self.nav_frame.grid(row=0, column=0, rowspan=2,
                            padx=(2, 2), pady=(2, 2), sticky='ew')

        self.nav_label = ttk.Label(
            self.nav_frame, text="Navigation", font=("TkDefaultFont", 11))
        self.nav_label.grid(row=0, column=0, pady=(7, 7), padx=(0, 7))

        self.prev_button = tk.Button(
            self.nav_frame, text="Previous", command=self.show_previous_image)
        self.prev_button.grid(row=1, column=0, padx=(2, 2), pady=(2, 2))

        self.next_button = tk.Button(
            self.nav_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=1, column=1, padx=(2, 10), pady=(2, 2))

        # Image section
        self.images_frame = ttk.Frame(
            self.left_frame, padding=(5, 5), relief="solid")
        self.images_frame.grid(
            row=2, column=0, columnspan=5, rowspan=5, sticky="nsew")

        self.image1_frame = ttk.Frame(self.images_frame, padding=(5, 5))
        self.image1_frame.pack(side=tk.LEFT, padx=(0, 0), pady=(0, 0))
        self.image1_label = ttk.Label(self.image1_frame, text="")
        self.image1_label.grid(row=0, column=0, padx=(0, 5))

        self.image2_frame = ttk.Frame(self.images_frame, padding=(5, 5))
        self.image2_frame.pack(side=tk.RIGHT, padx=(0, 0), pady=(0, 0))
        self.image2_label = ttk.Label(self.image2_frame, text="")
        self.image2_label.grid(row=0, column=0, padx=(5, 0))

        self.graph_button_frame = ttk.Frame(self.left_frame, padding=(5, 5))
        self.graph_button_frame.grid(row=7, column=0, pady=(
            5, 5), padx=(5, 5), columnspan=2, sticky="ew")
        self.graph_button = ttk.Button(
            self.graph_button_frame, text="Graph", command=lambda: self.draw_graph(), width=10)
        self.graph_button.pack(side=tk.LEFT)

        # Right part of the window
        self.right_frame = ttk.Frame(self, padding=(2, 2))
        self.right_frame.grid(row=0, column=1, padx=(
            2, 2), pady=(2, 2), sticky='nsew')

        # Upload section
        self.upload_section = ttk.Frame(self.right_frame, padding=(7, 7))
        self.upload_section.grid(row=0, column=1, columnspan=2, padx=(
            0, 0), pady=(0, 0), sticky='nsew')

        self.upload_label = ttk.Label(
            self.upload_section, text="Load directory", font=("TkDefaultFont", 11))
        self.upload_label.pack(side=tk.TOP, pady=(5, 5))

        self.upload_button = ttk.Button(
            self.upload_section, text="Load", command=lambda: self.load_directory(self.upload_entry))
        self.upload_button.pack(side=tk.LEFT, padx=(5, 10))

        self.upload_entry = ttk.Entry(self.upload_section, width=20)
        self.upload_entry.pack(side=tk.BOTTOM, padx=(5, 5))

        # Info section
        self.info_section = ttk.Frame(self.right_frame, padding=(7, 7))
        self.info_section.grid(row=2, column=0, rowspan=3, pady=(7, 7))

        self.info_label1 = ttk.Label(
            self.info_section, text="Image name: ", font=("TkDefaultFont", 11))
        self.info_label1.grid(row=0, column=0, padx=(7, 7), pady=(7, 7))
        # self.info_label1.pack(side = tk.LEFT)
        self.info_value1 = ttk.Label(
            self.info_section, text="", font=("TkDefaultFont", 11))
        # self.info_value1.grid(row=0, column=1, pady=(3, 3), padx=(0, 3))

        self.info_label2 = ttk.Label(
            self.info_section, text="Image size: ", font=("TkDefaultFont", 11))
        self.info_label2.grid(row=1, column=0, padx=(7, 7), pady=(7, 7))
        self.info_value2 = ttk.Label(
            self.info_section, text="", font=("TkDefaultFont", 11))
        # self.info_value2.grid(row=1, column=1, pady=(3, 3), padx=(0, 3))

        self.info_label3 = ttk.Label(
            self.info_section, text="Scale: ", font=("TkDefaultFont", 11))
        self.info_label3.grid(row=2, column=0, padx=(7, 7), pady=(7, 7))
        self.info_value3 = ttk.Label(
            self.info_section, text="", font=("TkDefaultFont", 11))
        # self.info_value3.grid(row=2, column=1, pady=(3, 3))

        # Make the frames expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0), weight=1)
        self.left_frame.grid_rowconfigure((2, 3, 4, 5, 6), weight=1)
        self.left_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.right_frame.grid_columnconfigure((1, 2, 3), weight=1)
        self.right_frame.grid_rowconfigure((2, 3, 4), weight=1)

        self.mainloop()

    def start(self):
        if self._started == 0:
            self.drawfront()
        self._started = 1
