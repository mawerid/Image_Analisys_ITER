from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent

matplotlib.use("TkAgg")


class GraphFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.fig = None
        self.axes = None
        self.toolbar = None
        # self.func = None
        self.canvas = None
        # self.range = np.linspace(0, 10, 1000)
        # self.cord_frame = cord_frame
        self.color = 'blue'
        self.linewidth = 1
        self.style_list = ['solid', '-', '--',
                           'dashed', '-.', 'dashdot', ':', 'dotted']
        self.style = '-'
        self.x_axis = 'x'
        self.y_axis = 'y'
        self.title = None
        self.ngraphs = 0
        self._start()

    def _start(self):
        """
        Приватный метод который задает конфигурации графика
        """
        self.fig = Figure(figsize=(5, 2), dpi=100)
        self.axes = self.fig.add_subplot(111)
        # self.a.set_xlim(np.min(self.range), np.max(self.range))

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(padx=(5, 5), pady=(5, 5))
        _Toolbar = tk.Frame(self)
        _Toolbar.pack(side=tk.TOP, fill=tk.BOTH)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.X)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)
        # self.canvas.mpl_connect('motion_notify_event', self._show_cords)
        # self.a.set_xlabel(self.x_axis, fontsize=12)
        # self.a.set_ylabel(self.y_axis, fontsize=12)

        if self.title is not None:
            self.axes.set_title(self.title)
            print()

    def draw_graph(self, files):
        """
        Метод который рисует графики
        """
        self.canvas.get_tk_widget().pack_forget()
        self.toolbar.pack_forget()
        self._start()
        # if(self.ngraphs > 2):
        #     self.canvas.get_tk_widget().pack_forget()
        #     self.toolbar.pack_forget()
        #     self._start()
        # print(files.shape)
        # print(files)
        for i in range(files.shape[0]):
            self.axes.plot(
                files[i], linewidth=self.linewidth, linestyle=self.style)
            # self.ngraphs += 1
            self.axes.set_title(self.title)
            self.canvas.draw()

    def set_title(self, value):
        self.title = value
        self.axes.set_title(self.title)

    # def _show_cords(self, event):
    #     """
    #     Приватный метод для координат мышки
    #     :param event: Параметры мышки
    #     """
    #     if event.inaxes and event.inaxes.get_navigate():
    #         try:
    #             s = event.inaxes.format_coord(event.xdata, event.ydata)
    #         except (ValueError, OverflowError):
    #             pass
    #         else:
    #             s = s.rstrip()
    #             artists = [a for a in event.inaxes._mouseover_set
    #                        if a.contains(event)[0] and a.get_visible()]
    #             if artists:
    #                 a = matplotlib.cbook._topmost_artist(artists)
    #                 if a is not event.inaxes.patch:
    #                     data = a.get_cursor_data(event)
    #                     if data is not None:
    #                         data_str = a.format_cursor_data(data).rstrip()
    #                         if data_str:
    #                             s = s + '\n' + data_str
    #


class NavigationToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, window):
        super().__init__(canvas, window, pack_toolbar=False)

    # override _Button() to re-pack the toolbar button in vertical direction
    def _Button(self, text, image_file, toggle, command):
        b = super()._Button(text, image_file, toggle, command)
        b.pack(side=tk.TOP)  # re-pack button in vertical direction
        return b

    # override _Spacer() to create vertical separator
    def _Spacer(self):
        s = tk.Frame(self, width=26, relief=tk.RIDGE, bg="DarkGray", padx=2)
        s.pack(side=tk.TOP, pady=5)  # pack in vertical direction
        return s

    # disable showing mouse position in toolbar
    def set_message(self, s):
        pass

    toolitems = (
        ('Home', 'Вернутся в начальный вид', 'home', 'home'),
        ('Back', 'Обратно в предыдущий вид', 'back', 'back'),
        ('Forward', 'Вперед к следующему виду', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan',
         'Левый клик для движения, Правый клик для увеличения\n'
         'x/y фиксирует оси, CTRL фиксирует стороны',
         'move', 'pan'),
        ('Save', 'Сохранить', 'filesave', 'save_figure'),
        (None, None, None, None))
