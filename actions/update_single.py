from actions.action import Action
from tkinter import *
from tkinter import messagebox

from error.exceptions import InvalidInputException
from repositories import relational_point_repository as rp_repository
from repositories import spatial_core_repository as scp_repository
from repositories import spatial_postgis_point_repository as spp_repository


class UpdateSingle(Action):

    def __init__(self, window):
        super().__init__(window)
        self.title = "Update Single"
        self.rename_window("Database Comparator - {0}".format(self.title))

        self.x_var = StringVar()
        self.y_var = StringVar()
        self.step_var = StringVar()

        self.init_gui()
        self.create_statistics()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text=self.title, anchor=CENTER, font=('Courier', 20), bg="#313335",
                             fg="#ffffff")
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
            x = float(self.x_var.get())
            y = float(self.y_var.get())
            step = float(self.step_var.get())
        except InvalidInputException as e:
            messagebox.showerror(title="Invalid input", message=str(e))
            self.reset_inputs()
            return
        except Exception:
            messagebox.showerror(title="Invalid input", message="'x', 'y' and 'step' must be floats")
            self.reset_inputs()
            return

        relational_data = rp_repository.update_point_by_coordinates(x, y, step)
        spatial_core_data = scp_repository.update_point_by_coordinates(x, y, step)
        spatial_postgis_data = spp_repository.update_point_by_coordinates(x, y, step)

        self.show_statistics(self.title, relational_data, spatial_core_data, spatial_postgis_data)

    def reset_inputs(self):
        self.x_var.set(value="")
        self.y_var.set(value="")
        self.step_var.set(value="")
