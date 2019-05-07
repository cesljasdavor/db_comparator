from actions.action import Action
from tkinter import *
from tkinter import messagebox

from error.exceptions import InvalidInputException
from repositories import relational_point_repository as rp_repository
from repositories import relational_point_object_repository as rpo_repository
from repositories import spatial_point_repository as sp_repository
from utils.gui_utils import LoadingScreen


class FindMultipleRotatedRectangle(Action):
    def __init__(self, window):
        super().__init__(window)

        self.x_var = StringVar()
        self.y_var = StringVar()
        self.width_var = StringVar()
        self.height_var = StringVar()
        self.angle_var = StringVar()
        self.relational_point_count_var = StringVar(value="NaN")
        self.relational_error_count_var = StringVar(value="NaN")
        self.relational_time_spent_var = StringVar(value="NaN")
        self.relational_avg_time_per_point_var = StringVar(value="NaN")
        self.relational_with_point_point_count_var = StringVar(value="NaN")
        self.relational_with_point_error_count_var = StringVar(value="NaN")
        self.relational_with_point_time_spent_var = StringVar(value="NaN")
        self.relational_with_point_avg_time_per_point_var = StringVar(value="NaN")
        self.spatial_point_count_var = StringVar(value="NaN")
        self.spatial_error_count_var = StringVar(value="NaN")
        self.spatial_time_spent_var = StringVar(value="NaN")
        self.spatial_avg_time_per_point_var = StringVar(value="NaN")
        self.best_database_var = StringVar(value="None")
        self.sr_ratio_var = StringVar(value="NaN")
        self.srpo_ratio_var = StringVar(value="NaN")
        self.rrpo_ratio_var = StringVar(value="NaN")

        self.init_gui()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text="Find Multiple - Rotated Rectangle", anchor=CENTER, font=('Courier', 20),
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

        angle_label = Label(input_frame, text="Angle(°)", fg="#ffffff", bg="#313335", bd=0, padx=20)
        angle_label.pack(side=LEFT)
        angle_entry = Entry(input_frame, textvariable=self.angle_var, width=15)
        angle_entry.pack(side=LEFT)

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

        # Relational with point object
        relational_with_point_label_frame = LabelFrame(
            action_statistics_frame,
            text="Relational database with point objects",
            labelanchor=N,
            bg="#313335",
            fg="#ffffff",
            pady=10
        )
        relational_with_point_label_frame.pack(side=LEFT, fill="both", expand="yes", pady=(15, 0))

        relational_with_point_point_count_label = Label(
            relational_with_point_label_frame,
            text="Point count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_point_count_label.grid(row=0, column=0, sticky=W)
        relational_with_point_point_count_value = Label(
            relational_with_point_label_frame,
            textvariable=self.relational_with_point_point_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_point_count_value.grid(row=0, column=1)

        relational_with_point_error_count_label = Label(
            relational_with_point_label_frame,
            text="Error count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_error_count_label.grid(row=1, column=0, sticky=W)
        relational_with_point_error_count_value = Label(
            relational_with_point_label_frame,
            textvariable=self.relational_with_point_error_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_error_count_value.grid(row=1, column=1)

        relational_with_point_time_spent_label = Label(
            relational_with_point_label_frame,
            text="Time spent",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_time_spent_label.grid(row=2, column=0, sticky=W)
        relational_with_point_time_spent_value = Label(
            relational_with_point_label_frame,
            textvariable=self.relational_with_point_time_spent_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_time_spent_value.grid(row=2, column=1)

        relational_with_point_avg_time_per_point_label = Label(
            relational_with_point_label_frame,
            text="Average time per point",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_avg_time_per_point_label.grid(row=3, column=0, sticky=W)
        relational_with_point_avg_time_per_point_value = Label(
            relational_with_point_label_frame,
            textvariable=self.relational_with_point_avg_time_per_point_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_with_point_avg_time_per_point_value.grid(row=3, column=1)

        # Spatial
        spatial_label_frame = LabelFrame(
            action_statistics_frame,
            text="Spatial database",
            labelanchor=N,
            bg="#313335",
            fg="#ffffff",
            pady=10
        )
        spatial_label_frame.pack(side=LEFT, fill="both", expand="yes", pady=(15, 0))

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

        best_database_label = Label(
            action_overall_data_frame,
            text="Best database",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        best_database_label.grid(row=0, column=0, sticky=W)
        best_database_value = Label(
            action_overall_data_frame,
            textvariable=self.best_database_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        best_database_value.grid(row=0, column=1)

        rrpo_ratio_label = Label(
            action_overall_data_frame,
            text="Relational / Relational with point objects",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        rrpo_ratio_label.grid(row=1, column=0, sticky=W)
        rrpo_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.rrpo_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        rrpo_ratio_value.grid(row=1, column=1)

        sr_ratio_label = Label(
            action_overall_data_frame,
            text="Spatial / Relational",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        sr_ratio_label.grid(row=2, column=0, sticky=W)
        sr_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.sr_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        sr_ratio_value.grid(row=2, column=1)

        srpo_ratio_label = Label(
            action_overall_data_frame,
            text="Spatial / Relational with point objects",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        srpo_ratio_label.grid(row=3, column=0, sticky=W)
        srpo_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.srpo_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        srpo_ratio_value.grid(row=3, column=1)

    def action(self):
        try:
            bottom_left_corner = (float(self.x_var.get()), float(self.y_var.get()))
            width = float(self.width_var.get())
            height = float(self.height_var.get())
            angle = float(self.angle_var.get())
        except InvalidInputException as e:
            messagebox.showerror(title="Invalid input", message=str(e))
            self.reset_inputs()
            return
        except Exception as e:
            messagebox.showerror(title="Invalid input",
                                 message="'x', 'y', 'width', 'height' and 'angle' must be floats")
            self.reset_inputs()
            raise e

        loading_screen = LoadingScreen(self.window, "Reading from database", "Initializing...")
        loading_screen.set_message("Reading points from relational database...")
        r_error_count, r_points_count, r_time_elapsed = rp_repository.find_points_in_rotated_rectangle(
            bottom_left_corner,
            width,
            height,
            angle
        )
        loading_screen.set_message("Points read from relational database.")
        loading_screen.set_progress_value(33.33)
        loading_screen.set_message("Reading points from relational database with point objects...")
        rpo_error_count, rpo_points_count, rpo_time_elapsed = rpo_repository.find_points_in_rotated_rectangle(
            bottom_left_corner,
            width,
            height,
            angle
        )
        loading_screen.set_message("Points read from relational database with point objects.")
        loading_screen.set_progress_value(66.66)
        loading_screen.set_message("Reading points from spatial database...")
        s_error_count, s_points_count, s_time_elapsed = sp_repository.find_points_in_rotated_rectangle(
            bottom_left_corner,
            width,
            height,
            angle
        )
        loading_screen.set_message("Points read from spatial database.")
        loading_screen.set_progress_value(100.0)
        loading_screen.set_message("Done.")
        loading_screen.close()

        if r_points_count == 0 and s_points_count == 0 and rpo_points_count == 0:
            messagebox.showwarning(
                title="Not found",
                message="No points inside bounding box bottom left corner " +
                        "= ({0}, {1}) width = {2}, height = {3}, angle = {4} (°)".format(
                            bottom_left_corner[0],
                            bottom_left_corner[1],
                            width,
                            height,
                            angle
                        )
            )

            return

        self.relational_error_count_var.set(value=r_error_count)
        self.relational_point_count_var.set(value=r_points_count)
        self.relational_time_spent_var.set(value="{0:.3f} ms".format(r_time_elapsed))
        self.relational_avg_time_per_point_var.set(
            "{0:.3f} ms".format(r_time_elapsed / (r_points_count + r_error_count)))

        self.relational_with_point_error_count_var.set(value=rpo_error_count)
        self.relational_with_point_point_count_var.set(value=rpo_points_count)
        self.relational_with_point_time_spent_var.set(value="{0:.3f} ms".format(rpo_time_elapsed))
        self.relational_with_point_avg_time_per_point_var.set(
            "{0:.3f} ms".format(rpo_time_elapsed / (rpo_points_count + rpo_error_count)))

        self.spatial_error_count_var.set(value=s_error_count)
        self.spatial_point_count_var.set(value=s_points_count)
        self.spatial_time_spent_var.set(value="{0:.3f} ms".format(s_time_elapsed))
        self.spatial_avg_time_per_point_var.set("{0:.3f} ms".format(s_time_elapsed / (s_points_count + s_error_count)))

        self.rrpo_ratio_var.set(value="{0:.3f}".format(r_time_elapsed / rpo_time_elapsed))
        self.sr_ratio_var.set(value="{0:.3f}".format(s_time_elapsed / r_time_elapsed))
        self.srpo_ratio_var.set(value="{0:.3f}".format(s_time_elapsed / rpo_time_elapsed))

        if rpo_time_elapsed < r_time_elapsed and rpo_time_elapsed < s_time_elapsed:
            best = "Relational with point objects"
        elif r_time_elapsed < rpo_time_elapsed and r_time_elapsed < s_time_elapsed:
            best = "Relational"
        else:
            best = "Spatial"

        self.best_database_var.set(value=best)

    def reset_inputs(self):
        self.x_var.set(value="")
        self.y_var.set(value="")
        self.width_var.set(value="")
        self.height_var.set(value="")
        self.angle_var.set(value="")
