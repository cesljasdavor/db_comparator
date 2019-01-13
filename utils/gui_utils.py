from tkinter import *
from tkinter.ttk import Progressbar


def show_help():
    help_window = Toplevel()
    help_window.title("Database Comparator - Help")
    help_window.geometry("{0}x{1}".format(600, 400))
    help_window.resizable(0, 0)
    help_window.configure(bg="#313335")

    help_title = Label(help_window, text="Help", anchor=CENTER, font=('Courier', 20), bg="#313335",
                       fg="#ffffff")
    help_title.pack(side=TOP, pady=(10, 10))
    help_text = """
Welcome to Database comparator. This small GUI application is created to compare spatial and relational 
database speeds.

Usage

1. Press on "File" -> "Load".
2. Find your .dbc file
3. Wait until all points are inserted in both spatial and relational database
4. Enter your query
5. View results

Created by Davor Češljaš, Faculty of Electrical engineering and Computing. 
All rights reserved ®  
    """
    help_message = Message(help_window, text=help_text, width=500, bg="#313335", fg="#ffffff")
    help_message.pack()


class LoadingScreen(object):
    def __init__(self, title, message=None):
        self.title = title
        self.message_var = StringVar(value=message)
        self.progress_var = DoubleVar(value=0.0)

        self.window = None

        self.init_gui()

    def set_message(self, message):
        self.message_var.set(value=message)

    def set_progress_value(self, value):
        self.progress_var.set(value=value)

    def init_gui(self):
        self.window = Toplevel()
        self.window.title(self.title)
        self.window.resizable(0, 0)
        self.window.configure(bg="#313335")

        progress_bar_message = Label(self.window, textvariable=self.message_var, anchor=W, bg="#313335", fg="#ffffff")
        progress_bar_message.pack(side=TOP, pady=(10, 10))

        progress_bar = Progressbar(
            self.window,
            variable=self.progress_var,
            orient=HORIZONTAL,
            length=200,
            mode="determinate",
            takefocus=True,
            maximum=100
        )
        progress_bar.pack(side=TOP)

    def close(self):
        self.window.destroy()
