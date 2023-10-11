import os
import pathlib
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk


def show_image(label):
    path = pathlib.Path("C:/", "Фото_пыли_1", "ACD-1_k0.4_after.png")
    print(path)
    image = Image.open("ACD-1_k04_after.jpg")
    image = image.resize((100, 100), Image.LANCZOS)
    img = ImageTk.PhotoImage(image)

    label.config(image=img)
    label.image = img


def test():
    root = tk.Tk()
    frame = ttk.Frame(root, width=600, height=400)
    frame.pack()
    frame.place(anchor='center', relx=0.5, rely=0.5)

    # Create an object of tkinter ImageTk

    # Create a Label Widget to display the text or Image
    label = ttk.Label(frame)
    label.pack()
    show_image(label)
    root.mainloop()
