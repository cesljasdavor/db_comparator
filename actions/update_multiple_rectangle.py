from actions.action import Action
from tkinter import *
from tkinter import messagebox

from error.exceptions import InvalidInputException
from repositories import relational_point_repository as rp_repository
from repositories import spatial_core_repository as scp_repository
from repositories import spatial_postgis_point_repository as spp_repository
from utils.gui_utils import LoadingScreen


class UpdateMultipleRectangle(Action):

    def __init__(self, window):
        super().__init__(window)
        self.title = "Update Multiple - Rectangle"
        self.rename_window("Database Comparator - {0}".format(self.title))

        self.x_var = StringVar()
        self.y_var = StringVar()
        self.width_var = StringVar()
        self.height_var = StringVar()
        self.step_var = StringVar()

        self.init_gui()
        self.create_statistics()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text=self.title, anchor=CENTER, font=('Courier', 20),
                             bg="#313335", fg="#ffffff")
        action_title.pack(side=TOP, pady=(10, 10))

        input_frame = Frame(self.window, bg="#313335")
        input_frame.pack(side=TOP, pady=(15, 10), padx=(10, 10))

        x_label = Label(input_frame, text="X", fg="#ffffff", bg="#313335", bd=0, padx=20)
        x_label.pack(side=LEFT)
        x_entry = Entry(input_frame, textvariable=self.x_var, width=15)
        x_entry.pack(side=LEFT)

        y_label = Label(input_frame, text="Y", fg="#ffffff", bg="#313335", bd=0, padx=20)
        y_label.pack(side=LEFT)
        y_entry = Entry(input_frame, textvariable=self.y_var, width=15)
        y_entry.pack(side=LEFT)

        width_label = Label(input_frame, text="Width", fg="#ffffff", bg="#313335", bd=0, padx=20)
        width_label.pack(side=LEFT)
        width_entry = Entry(input_frame, textvariable=self.width_var, width=15)
        width_entry.pack(side=LEFT)

        height_label = Label(input_frame, text="Height", fg="#ffffff", bg="#313335", bd=0, padx=20)
        height_label.pack(side=LEFT)
        height_entry = Entry(input_frame, textvariable=self.height_var, width=15)
        height_entry.pack(side=LEFT)

        step_label = Label(input_frame, text="Step", fg="#ffffff", bg="#313335", bd=0, padx=20)
        step_label.pack(side=LEFT)
        step_entry = Entry(input_frame, textvariable=self.step_var, width=15)
        step_entry.pack(side=LEFT)

        action_button_frame = Frame(self.window, bg="#313335")
        action_button_frame.pack(side=TOP, pady=(10, 15))

        action_button = Button(
            action_button_frame,
            text="Compare databases",
            command=self.perform_action,
            bg="#28a745",
            activebackground="#25a341",
            fg="#ffffff",
            activeforeground="#ffffff",
            bd=0
        )
        action_button.pack(side=BOTTOM, pady=(0, 15))

    def action(self):
        try:
            bottom_left_corner = (float(self.x_var.get()), float(self.y_var.get()))
            width = float(self.width_var.get())
            height = float(self.height_var.get())
            step = float(self.step_var.get())
        except InvalidInputException as e:
            messagebox.showerror(title="Invalid input", message=str(e))
            self.reset_inputs()
            return
        except Exception:
            messagebox.showerror(title="Invalid input", message="'x', 'y', 'width', 'height' and 'step' must be floats")
            self.reset_inputs()
            return

        loading_screen = LoadingScreen(self.window, "Updating database", "Initializing...")
        loading_screen.set_message("Updating points in relational database...")
        relational_data= rp_repository.update_points_in_rectangle(
            bottom_left_corner,
            width,
            height,
            step
        )
        loading_screen.set_message("Points updated in relational database.")
        loading_screen.set_progress_value(33.33)
        loading_screen.set_message("Updating points in spatial Core database...")
        spatial_core_data = scp_repository.update_points_in_rectangle(
            bottom_left_corner,
            width,
            height,
            step
        )
        loading_screen.set_message("Points updated in spatial Core database.")
        loading_screen.set_progress_value(66.66)
        loading_screen.set_message("Updating points in spatial PostGIS database...")
        spatial_postgis_data = spp_repository.update_points_in_rectangle(
            bottom_left_corner,
            width,
            height,
            step
        )
        loading_screen.set_message("Points updated in spatial PostGIS database.")
        loading_screen.set_progress_value(100.0)
        loading_screen.set_message("Done.")
        loading_screen.close()

        self.show_statistics(self.title, relational_data, spatial_core_data, spatial_postgis_data)

    def reset_inputs(self):
        self.x_var.set(value="")
        self.y_var.set(value="")
        self.width_var.set(value="")
        self.height_var.set(value="")
        self.step_var.set(value="")
