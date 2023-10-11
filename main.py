from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from app.app import App
import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")


def main():
    app = App()
    app.start()


if __name__ == '__main__':
    main()
