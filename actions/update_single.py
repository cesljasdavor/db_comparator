from actions.action import Action
from tkinter import *
from tkinter import messagebox

from error.exceptions import InvalidInputException
from repositories import relational_point_repository as rp_repository
from repositories import spatial_point_repository as sp_repository


class UpdateSingle(Action):

    def __init__(self, window):
        super().__init__(window)

        self.old_x_var = StringVar()
        self.old_y_var = StringVar()
        self.new_x_var = StringVar()
        self.new_y_var = StringVar()
        self.relational_point_count_var = StringVar(value="NaN")
        self.relational_error_count_var = StringVar(value="NaN")
        self.relational_time_spent_var = StringVar(value="NaN")
        self.relational_avg_time_per_point_var = StringVar(value="NaN")
        self.spatial_point_count_var = StringVar(value="NaN")
        self.spatial_error_count_var = StringVar(value="NaN")
        self.spatial_time_spent_var = StringVar(value="NaN")
        self.spatial_avg_time_per_point_var = StringVar(value="NaN")
        self.faster_database_var = StringVar(value="None")
        self.ratio_var = StringVar(value="NaN")

        self.init_gui()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text="Update Single", anchor=CENTER, font=('Courier', 20), bg="#313335",
                             fg="#ffffff")
        action_title.pack(side=TOP, pady=(10, 10))

        input_frame = Frame(self.window, bg="#313335")
        input_frame.pack(side=TOP, pady=(15, 10), padx=(10, 10))

        old_x_label = Label(input_frame, text="Old X", fg="#ffffff", bg="#313335", bd=0, padx=20)
        old_x_label.pack(side=LEFT)
        old_x_entry = Entry(input_frame, textvariable=self.old_x_var, width=15)
        old_x_entry.pack(side=LEFT)

        old_y_label = Label(input_frame, text="Old Y", fg="#ffffff", bg="#313335", bd=0, padx=20)
        old_y_label.pack(side=LEFT)
        old_y_entry = Entry(input_frame, textvariable=self.old_y_var, width=15)
        old_y_entry.pack(side=LEFT)

        new_x_label = Label(input_frame, text="New X", fg="#ffffff", bg="#313335", bd=0, padx=20)
        new_x_label.pack(side=LEFT)
        new_x_entry = Entry(input_frame, textvariable=self.new_x_var, width=15)
        new_x_entry.pack(side=LEFT)

        new_y_label = Label(input_frame, text="New Y", fg="#ffffff", bg="#313335", bd=0, padx=20)
        new_y_label.pack(side=LEFT)
        new_y_entry = Entry(input_frame, textvariable=self.new_y_var, width=15)
        new_y_entry.pack(side=LEFT)

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

        # Statistics
        action_statistics_frame = Frame(self.window, bg="#313335")
        action_statistics_frame.pack(side=TOP, fill="both", expand="yes")

        action_statistics_title = Label(
            action_statistics_frame,
            text="Statistics",
            anchor=CENTER,
            font=('Courier', 20),
            bg="#313335",
            fg="#ffffff"
        )
        action_statistics_title.pack(side=TOP, pady=(10, 10))

        # Relational
        relational_label_frame = LabelFrame(
            action_statistics_frame,
            text="Relational database",
            labelanchor=N,
            bg="#313335",
            fg="#ffffff",
            pady=10
        )
        relational_label_frame.pack(side=LEFT, fill="both", expand="yes", pady=(15, 0))

        relational_point_count_label = Label(
            relational_label_frame,
            text="Point count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_point_count_label.grid(row=0, column=0, sticky=W)
        relational_point_count_value = Label(
            relational_label_frame,
            textvariable=self.relational_point_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_point_count_value.grid(row=0, column=1)

        relational_error_count_label = Label(
            relational_label_frame,
            text="Error count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_error_count_label.grid(row=1, column=0, sticky=W)
        relational_error_count_value = Label(
            relational_label_frame,
            textvariable=self.relational_error_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_error_count_value.grid(row=1, column=1)

        relational_time_spent_label = Label(
            relational_label_frame,
            text="Time spent",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_time_spent_label.grid(row=2, column=0, sticky=W)
        relational_time_spent_value = Label(
            relational_label_frame,
            textvariable=self.relational_time_spent_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_time_spent_value.grid(row=2, column=1)

        relational_avg_time_per_point_label = Label(
            relational_label_frame,
            text="Average time per point",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_avg_time_per_point_label.grid(row=3, column=0, sticky=W)
        relational_avg_time_per_point_value = Label(
            relational_label_frame,
            textvariable=self.relational_avg_time_per_point_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_avg_time_per_point_value.grid(row=3, column=1)

        # Spatial
        spatial_label_frame = LabelFrame(
            action_statistics_frame,
            text="Spatial database",
            labelanchor=N,
            bg="#313335",
            fg="#ffffff",
            pady=10
        )
        spatial_label_frame.pack(side=RIGHT, fill="both", expand="yes", pady=(15, 0))

        spatial_point_count_label = Label(
            spatial_label_frame,
            text="Point count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_point_count_label.grid(row=0, column=0, sticky=W)
        spatial_point_count_value = Label(
            spatial_label_frame,
            textvariable=self.spatial_point_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_point_count_value.grid(row=0, column=1)

        spatial_error_count_label = Label(
            spatial_label_frame,
            text="Error count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_error_count_label.grid(row=1, column=0, sticky=W)
        spatial_error_count_value = Label(
            spatial_label_frame,
            textvariable=self.spatial_error_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_error_count_value.grid(row=1, column=1)

        spatial_time_spent_label = Label(
            spatial_label_frame,
            text="Time spent",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_time_spent_label.grid(row=2, column=0, sticky=W)
        spatial_time_spent_value = Label(
            spatial_label_frame,
            textvariable=self.spatial_time_spent_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_time_spent_value.grid(row=2, column=1)

        spatial_avg_time_per_point_label = Label(
            spatial_label_frame,
            text="Average time per point",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_avg_time_per_point_label.grid(row=3, column=0, sticky=W)
        spatial_avg_time_per_point_value = Label(
            spatial_label_frame,
            textvariable=self.spatial_avg_time_per_point_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_avg_time_per_point_value.grid(row=3, column=1)

        # Overall
        action_overall_frame = Frame(self.window, bg="#313335")
        action_overall_frame.pack(side=TOP, expand="yes", pady=(10, 20))

        action_overall_title = Label(
            action_overall_frame,
            text="Query Overall",
            anchor=CENTER,
            font=('Courier', 13),
            bg="#313335",
            fg="#ffffff"
        )
        action_overall_title.pack(side=TOP, pady=(10, 10))

        action_overall_data_frame = Frame(action_overall_frame, bg="#313335")
        action_overall_data_frame.pack(side=TOP, fill="both", expand="yes")

        faster_database_label = Label(
            action_overall_data_frame,
            text="Faster database",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        faster_database_label.grid(row=0, column=0, sticky=W)
        faster_find_database_value = Label(
            action_overall_data_frame,
            textvariable=self.faster_database_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        faster_find_database_value.grid(row=0, column=1)

        percentage_ration_label = Label(
            action_overall_data_frame,
            text="Ratio",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        percentage_ration_label.grid(row=1, column=0, sticky=W)
        percentage_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        percentage_ratio_value.grid(row=1, column=1)

    def action(self):
        try:
            old_x = float(self.old_x_var.get())
            old_y = float(self.old_y_var.get())
            new_x = float(self.new_y_var.get())
            new_y = float(self.new_y_var.get())
            r_error_count, r_points_count, r_time_elapsed = rp_repository.update_point_by_coordinates(old_x, old_y, new_x, new_y)
            s_error_count, s_points_count, s_time_elapsed = sp_repository.update_point_by_coordinates(old_x, old_y, new_x, new_y)

            if r_points_count == 0 and s_points_count == 0:
                messagebox.showwarning(title="Not found", message="No points with coordinates ({0}, {1})".format(old_x, old_y))
                return
        except InvalidInputException as e:
            messagebox.showerror(title="Invalid input", message=str(e))
            self.reset_inputs()
            return
        except Exception:
            messagebox.showerror(title="Invalid input", message="'old x', 'old y', 'new x' and 'new y' must be floats")
            self.reset_inputs()
            return

        self.relational_error_count_var.set(value=r_error_count)
        self.relational_point_count_var.set(value=r_points_count)
        self.relational_time_spent_var.set(value="{0:.3f} ms".format(r_time_elapsed))
        self.relational_avg_time_per_point_var.set(
            "{0:.3f} ms".format(r_time_elapsed / (r_points_count + r_error_count)))

        self.spatial_error_count_var.set(value=s_error_count)
        self.spatial_point_count_var.set(value=s_points_count)
        self.spatial_time_spent_var.set(value="{0:.3f} ms".format(s_time_elapsed))
        self.spatial_avg_time_per_point_var.set("{0:.3f} ms".format(s_time_elapsed / (s_points_count + s_error_count)))

        if r_time_elapsed < s_time_elapsed:
            faster = "Relational"
            ratio = s_time_elapsed / r_time_elapsed
        else:
            faster = "Spatial"
            ratio = r_time_elapsed / s_time_elapsed

        self.faster_database_var.set(value=faster)
        self.ratio_var.set(value="{0:.3f}".format(ratio))

    def reset_inputs(self):
        self.old_x_var.set(value="")
        self.old_y_var.set(value="")
        self.new_x_var.set(value="")
        self.new_y_var.set(value="")
