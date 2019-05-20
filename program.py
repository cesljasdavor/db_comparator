import os
from tkinter import *
from tkinter import PhotoImage

from actions.delete_multiple_circle import DeleteMultipleCircle
from actions.delete_multiple_rectangle import DeleteMultipleRectangle
from actions.delete_multiple_rotated_rectangle import DeleteMultipleRotatedRectangle
from actions.delete_single import DeleteSingle
from actions.find_multiple_circle import FindMultipleCircle
from actions.find_multiple_rectangle import FindMultipleRectangle
from actions.find_multiple_rotated_rectangle import FindMultipleRotatedRectangle
from actions.find_single import FindSingle
from actions.insert_multiple import InsertMultiple
from actions.insert_single import InsertSingle
from actions.update_multiple_circle import UpdateMultipleCircle
from actions.update_multiple_rectangle import UpdateMultipleRectangle
from actions.update_multiple_rotated_rectangle import UpdateMultipleRotatedRectangle
from actions.update_single import UpdateSingle
from utils.gui_utils import perform_database_reset, show_map
from utils.gui_utils import show_help


class Program(object):
    def __init__(self):
        self.window = Tk(className="Database Comparator")
        icon = PhotoImage(file=os.path.join("/usr/share/icons", "database_comparator.png"))
        self.window.tk.call("wm", "iconphoto", self.window._w, icon)
        self.window.title("Database Comparator")
        self.window.resizable(0, 0)
        self.window.configure(bg="#313335")
        self.window.wm_iconname("database_comparator.png")
        self.setup_menubar()

        # Initialize window
        FindMultipleRectangle(self.window)

    def start(self):
        self.window.mainloop()

    def setup_menubar(self):
        menubar = Menu(
            self.window,
            bg="#212325",
            activebackground="#313335",
            fg="#ffffff",
            activeforeground="#ffffff",
            bd=0
        )
        self.window.config(menu=menubar)

        # Actions
        action_menu = Menu(
            menubar,
            tearoff=0,
            bg="#212325",
            activebackground="#313335",
            fg="#ffffff",
            activeforeground="#ffffff",
            bd=5
        )
        action_menu.add_command(label="Insert single", command=self.insert_single)
        action_menu.add_command(label="Insert multiple", command=self.insert_multiple)
        action_menu.add_separator()
        action_menu.add_command(label="Find single", command=self.find_single)
        action_menu.add_command(label="Find multiple - Rectangle", command=self.find_multiple_rectangle)
        action_menu.add_command(label="Find multiple - Rotated Rectangle", command=self.find_multiple_rotated_rectangle)
        action_menu.add_command(label="Find multiple - Circle", command=self.find_multiple_circle)
        action_menu.add_separator()
        action_menu.add_command(label="Update single", command=self.update_single)
        action_menu.add_command(label="Update multiple - Rectangle", command=self.update_multiple_rectangle)
        action_menu.add_command(label="Update multiple - Rotated Rectangle", command=self.update_multiple_rotated_rectangle)
        action_menu.add_command(label="Update multiple - Circle", command=self.update_multiple_circle)
        action_menu.add_separator()
        action_menu.add_command(label="Delete single", command=self.delete_single)
        action_menu.add_command(label="Delete multiple - Rectangle", command=self.delete_multiple_rectangle)
        action_menu.add_command(label="Delete multiple - Rotated Rectangle", command=self.delete_multiple_rotated_rectangle)
        action_menu.add_command(label="Delete multiple - Circle", command=self.delete_multiple_circle)
        action_menu.add_separator()
        action_menu.add_command(label="Reset database", command=perform_database_reset)

        # Maps
        map_menu = Menu(
            menubar,
            tearoff=0,
            bg="#212325",
            activebackground="#313335",
            fg="#ffffff",
            activeforeground="#ffffff",
            bd=5
        )
        map_menu.add_command(label="Relational", command=lambda: show_map("r"))
        map_menu.add_command(label="Spatial Core", command=lambda: show_map("sc"))
        map_menu.add_command(label="Spatial PostGIS", command=lambda: show_map("sp"))

        menubar.add_cascade(label="Actions", menu=action_menu)
        menubar.add_cascade(label="Maps", menu=map_menu)
        menubar.add_command(label="Help", command=show_help)
        menubar.add_command(label="Exit", command=self.exit_app)

    def insert_multiple(self):
        InsertMultiple(self.window)

    def insert_single(self):
        InsertSingle(self.window)

    def update_single(self):
        UpdateSingle(self.window)

    def update_multiple_rectangle(self):
        UpdateMultipleRectangle(self.window)

    def update_multiple_rotated_rectangle(self):
        UpdateMultipleRotatedRectangle(self.window)

    def update_multiple_circle(self):
        UpdateMultipleCircle(self.window)

    def delete_multiple_rectangle(self):
        DeleteMultipleRectangle(self.window)

    def delete_multiple_rotated_rectangle(self):
        DeleteMultipleRotatedRectangle(self.window)

    def delete_multiple_circle(self):
        DeleteMultipleCircle(self.window)

    def delete_single(self):
        DeleteSingle(self.window)

    def find_multiple_rectangle(self):
        FindMultipleRectangle(self.window)

    def find_multiple_rotated_rectangle(self):
        FindMultipleRotatedRectangle(self.window)

    def find_multiple_circle(self):
        FindMultipleCircle(self.window)

    def find_single(self):
        FindSingle(self.window)

    def exit_app(self):
        self.window.destroy()
