import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar

from utils.program_utils import *
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def show_help():
    help_window = Toplevel()
    help_window.title("Database Comparator - Help")
    icon = PhotoImage(file=os.path.join("/usr/share/icons", "database_comparator.png"))
    help_window.tk.call("wm", "iconphoto", help_window._w, icon)
    help_window.geometry("{0}x{1}".format(600, 400))
    help_window.resizable(0, 0)
    help_window.configure(bg="#313335")

    help_title = Label(help_window, text="Help", anchor=CENTER, font=('Courier', 20), bg="#313335",
                       fg="#ffffff")
    help_title.pack(side=TOP, pady=(10, 10))
    help_text = """
Welcome to Database comparator. This small GUI application is created to compare spatial and relational database speeds.

Usage
1. Click on "Actions" menu and pick one of the CRUD operations
2. Enter necessary parameters
3. Click "Compare databases" button
4. View results

You can click on "Show Map" to visualize coordinates on a map of the world.

Created by Davor Češljaš, Faculty of Electrical engineering and Computing. 
All rights reserved ®  
    """
    help_message = Message(help_window, text=help_text, width=500, bg="#313335", fg="#ffffff")
    help_message.pack()


def show_map(table_name=None):
    if table_name == "r":
        points = get_all_relational_points()
        figure_name = "Relational Point Map"
    elif table_name == "sc":
        points = get_all_spatial_core_points()
        figure_name = "Spatial Core Point Map"
    elif table_name == "sp":
        points = get_all_spatial_postgis_points()
        figure_name = "Spatial PostGIS Point Map"
    else:
        raise Exception("No table with name '{0}'".format(table_name))

    x_coordinates = [point.x for point in points]
    y_coordinates = [point.y for point in points]

    plt.figure(num=figure_name, figsize=(12, 8), edgecolor="grey")
    plt.xlabel("Longitude")
    plt.xlim((-180.0, 180.0))
    plt.ylabel("Latitude")
    plt.ylim((-90.0, 90.0))
    m = Basemap(projection='cyl', resolution=None,
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180)
    m.scatter(x=x_coordinates, y=y_coordinates, c="red", s=0.1)
    m.etopo()
    plt.show()


def perform_database_reset():
    reset_database()
    messagebox.showinfo(title="Database reset", message="Database successfully reset.")


class LoadingScreen(object):
    def __init__(self, master, title, message=None):
        self.master = master
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
        self.window = Toplevel(self.master)
        self.window.title(self.title)
        icon = PhotoImage(file=os.path.join("/usr/share/icons", "database_comparator.png"))
        self.window.tk.call("wm", "iconphoto", self.window._w, icon)
        self.window.resizable(0, 0)
        self.window.geometry("{0}x{1}".format(400, 100))
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
