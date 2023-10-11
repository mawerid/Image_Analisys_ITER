from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import os

from app.graph import GraphFrame, NavigationToolbar
# from comp import *

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk

import matplotlib
import matplotlib.pyplot as plt

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
        self.geometry("1280x720")

        self.files = []

    def load_directory(self, entry):
        self.directory_path = filedialog.askdirectory()
        if self.directory_path:
            self.image_files = [f for f in os.listdir(self.directory_path) if f.lower(
            ).endswith((".jpg", ".png", ".gif", ".bmp", ".jpeg"))]
            print(self.image_files)
            # self.images = []

            # for image_file in self.image_files:
            #     image_path = os.path.join(self.directory_path, image_file)
            #     image = Image.open(image_path)
            #
            #     # Resize images if necessary
            #     max_width = 480
            #     max_height = 480
            #     width, height = image.size
            #     if width > max_width or height > max_height:
            #         ratio = min(max_width / width, max_height / height)
            #         new_width = int(width * ratio)
            #         new_height = int(height * ratio)
            #         image = image.resize((new_width, new_height), Image.LANCZOS)
            #
            #     photo = ImageTk.PhotoImage(image)
            #     self.images.append((image, photo))

            if self.image_files:
                self.current_image_index = 0
                self.show_current_image()

        print(self.current_image_index)
        entry.delete(0, tk.END)
        entry.insert(0, self.directory_path)

        # offset - начиная с какого байта читать файл, dtype - как интерпретировать прочитанные строки.
        # Размер uint16 - 2 байта, поэтому чтение файла происходит 2 байтовыми блоками.

    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            # image_path = os.path.join(self.directory_path, self.image_files[self.current_image_index])
            image_path = self.directory_path + "\\\\" + \
                self.image_files[self.current_image_index]
            print(image_path)
            image = Image.open(image_path)

            # Resize images if necessary
            max_width = 480
            max_height = 480
            width, height = image.size
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.LANCZOS)

            photo = ImageTk.PhotoImage(image)

            # self.images.append((image, photo))
            # image, photo = self.images[self.current_image_index]

            self.image1_label.config(image=photo)
            self.image1_label.image = photo

            self.image2_label.config(image=photo)
            self.image2_label.image = photo

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_current_image()

    def show_next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.show_current_image()

    # Placeholder for your ML algorithm integration
    def run_ml_algorithm(self):
        if self.current_image_index >= 0:
            image, _ = self.images[self.current_image_index]
            # Implement your ML algorithm here using 'image'

    def draw_graph(self):
        x = np.linspace(0, 10, 100)
        y = np.sqrt(x)
        plt.plot(x, y)
        plt.show()

    def drawfront(self):

        # self.header = ttk.Frame(self, padding=(2, 2), relief='solid')
        # self.header.grid(row=0, column=0, columnspan=2, pady=(2, 2), sticky='nsew')
        #
        # self.headtitle = ttk.Label(self.header, text="Название ПО", font=("Helvetica", 16))
        # self.headtitle.pack(pady=(5, 5))

        # Left part of the window
        self.left_frame = ttk.Frame(self, padding=(7, 7), relief="solid")
        self.left_frame.grid(row=0, column=0, rowspan=15,
                             padx=(2, 2), pady=(2, 2), sticky='nsew')

        # Image area
        self.images = []
        self.current_image_index = -1

        # Navigation buttons
        self.nav_frame = ttk.Frame(self.left_frame, padding=(5, 5))
        self.nav_frame.grid(row=0, column=0, rowspan=2,
                            padx=(2, 2), pady=(2, 2), sticky='ew')

        self.nav_label = ttk.Label(
            self.nav_frame, text="Навигация", font=("TkDefaultFont", 11))
        self.nav_label.grid(row=0, column=0, pady=(7, 7), padx=(0, 7))

        self.prev_button = tk.Button(
            self.nav_frame, text="Previous", command=self.show_previous_image)
        self.prev_button.grid(row=1, column=0, padx=(2, 2), pady=(2, 2))
        # self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button = tk.Button(
            self.nav_frame, text="Next", command=self.show_next_image)
        self.next_button.grid(row=1, column=1, padx=(2, 10), pady=(2, 2))
        # self.next_button.pack(side=tk.LEFT)

        # Image section
        self.images_frame = ttk.Frame(
            self.left_frame, padding=(5, 5), relief="solid")
        self.images_frame.grid(
            row=2, column=0, columnspan=5, rowspan=5, sticky="nsew")

        self.image1_frame = ttk.Frame(self.images_frame, padding=(5, 5))
        # self.image1_frame.grid(row=0, column=0)
        self.image1_frame.pack(side=tk.LEFT, padx=(0, 0), pady=(0, 0))
        self.image1_label = ttk.Label(self.image1_frame, text="")
        self.image1_label.grid(row=0, column=0, padx=(0, 5))

        self.image2_frame = ttk.Frame(self.images_frame, padding=(5, 5))
        # self.image2_frame.grid(row=0, column=1)
        self.image2_frame.pack(side=tk.RIGHT, padx=(0, 0), pady=(0, 0))
        self.image2_label = ttk.Label(self.image2_frame, text="")
        self.image2_label.grid(row=0, column=0, padx=(5, 0))

        self.graph_button_frame = ttk.Frame(self.left_frame, padding=(5, 5))
        self.graph_button_frame.grid(row=7, column=0, pady=(
            5, 5), padx=(5, 5), columnspan=2, sticky="ew")
        self.graph_button = ttk.Button(
            self.graph_button_frame, text="Graph", command=lambda: self.draw_graph(), width=10)
        # self.graph_button.grid(row=7, column=0, pady=(5, 5), padx=(0, 5))
        self.graph_button.pack(side=tk.LEFT)
        # Graph areas
        # self.graph1 = GraphFrame(self.left_frame)
        # self.graph1.set_title("Графики опорного и объектного сигналов")
        # self.graph1.grid(row=1, column=0, padx=(2, 2), pady=(2, 2))

        # Right part of the window
        self.right_frame = ttk.Frame(self, padding=(2, 2))
        self.right_frame.grid(row=0, column=1, padx=(
            2, 2), pady=(2, 2), sticky='nsew')

        # Upload section
        self.upload_section = ttk.Frame(self.right_frame, padding=(7, 7))
        self.upload_section.grid(row=0, column=1, columnspan=2, padx=(
            0, 0), pady=(0, 0), sticky='nsew')

        self.upload_label = ttk.Label(
            self.upload_section, text="Загрузка фото/директория", font=("TkDefaultFont", 11))
        # self.upload_label.grid(row=0, column=0, pady=(0, 0), padx=(0, 0))
        self.upload_label.pack(side=tk.TOP, pady=(5, 5))
        self.upload_button = ttk.Button(self.upload_section, text="Загрузить",
                                        command=lambda: self.load_directory(self.upload_entry))
        self.upload_button.pack(side=tk.LEFT, padx=(5, 10))
        # self.upload_button.grid(row=1, column=0, pady=(0, 0), padx=(0, 0))
        self.upload_entry = ttk.Entry(self.upload_section, width=20)
        # self.upload_entry.grid(row=1, column=1, pady=(0, 0), padx=(0, 0))
        self.upload_entry.pack(side=tk.BOTTOM, padx=(5, 5))

        # self.upload_label = ttk.Label(self.upload_section, text="Загрузка фото", font=("TkDefaultFont", 11))
        # self.upload_label.grid(row=2, column=0, pady=(7, 7), padx=(0, 7))
        #
        # self.upload_button2 = ttk.Button(self.upload_section, text="Загрузить",
        #                                  command=lambda: self.upload_file(self.upload_entry2))
        # self.upload_button2.grid(row=3, column=0, pady=(7, 7), padx=(0, 7))
        #
        # self.upload_entry2 = ttk.Entry(self.upload_section)
        # self.upload_entry2.grid(row=3, column=1, pady=(7, 7), padx=(7, 7))

        # Option menus section
        # self.option_menu_section = ttk.Frame(self.right_frame, padding=(7, 7))
        # self.option_menu_section.grid(row=1, column=1, padx=(7, 7), pady=(7, 7), sticky='nsew')
        #
        # self.option_menu1_label = ttk.Label(self.option_menu_section, text="Настройка сигнала", font=("TkDefaultFont", 12, "bold"))
        # self.option_menu1_label.grid(row=0, column=0, pady=(7, 7))

        # self.save_section = ttk.Frame(self.right_frame)
        # self.save_section.grid(row=2, column=0, columnspan=2, pady=(7, 7))
        #
        # self.save_label = ttk.Label(self.save_section, text="Сохранить файл", font=("TkDefaultFont", 11))
        # self.save_label.grid(row=0, column=0, padx=(7, 7), pady=(7, 7))
        #
        # self.save_box = ttk.Combobox(self.save_section, values=["csv"])
        # self.save_box.current(0)
        # self.save_box.grid(row=1, column=0, pady=(7, 7), padx=(7, 7))
        #
        # self.save_button = ttk.Button(self.save_section, text="Save File", command=self.save_file)
        # self.save_button.grid(row=1, column=1, pady=(7, 0))

        # Make the frames expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure((2, 3, 4, 5, 6), weight=1)
        self.left_frame.grid_columnconfigure((2, 3), weight=1)
        # self.right_frame.grid_rowconfigure((2, 3,4), weight=1)

        self.mainloop()

    def start(self):
        if self._started == 0:
            self.drawfront()
        self._started = 1
