from actions.action import Action
from tkinter import *


class FindMultiple(Action):
    def __init__(self, window):
        super().__init__(window)

        self.relational_point_count_var = StringVar(value="NaN")
        self.relational_error_count_var = StringVar(value="NaN")
        self.relational_time_spent_var = StringVar(value="NaN")
        self.relational_avg_time_per_point_var = StringVar(value="NaN")
        self.spatial_point_count_var = StringVar(value="NaN")
        self.spatial_error_count_var = StringVar(value="NaN")
        self.spatial_time_spent_var = StringVar(value="NaN")
        self.spatial_avg_time_per_point_var = StringVar(value="NaN")
        self.faster_database_var = StringVar(value="None")
        self.percentage_ratio_var = StringVar(value="NaN")

        self.init_gui()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text="Find Multiple", anchor=CENTER, font=('Courier', 20), bg="#313335",
                             fg="#ffffff")
        action_title.pack(side=TOP, pady=(10, 10))

        input_frame = Frame(self.window, bg="#313335")
        input_frame.pack(side=TOP, pady=(15, 10), padx=(10, 10))

        x_label = Label(input_frame, text="X", fg="#ffffff", bg="#313335", bd=0, padx=20)
        x_label.pack(side=LEFT)
        x_entry = Entry(input_frame, width=15)
        x_entry.pack(side=LEFT)

        y_label = Label(input_frame, text="Y", fg="#ffffff", bg="#313335", bd=0, padx=20)
        y_label.pack(side=LEFT)
        y_entry = Entry(input_frame, width=15)
        y_entry.pack(side=LEFT)

        width_label = Label(input_frame, text="Width", fg="#ffffff", bg="#313335", bd=0, padx=20)
        width_label.pack(side=LEFT)
        width_entry = Entry(input_frame, width=15)
        width_entry.pack(side=LEFT)

        height_label = Label(input_frame, text="Height", fg="#ffffff", bg="#313335", bd=0, padx=20)
        height_label.pack(side=LEFT)
        height_entry = Entry(input_frame, width=15)
        height_entry.pack(side=LEFT)

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
            text="Faster query percentage",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        percentage_ration_label.grid(row=1, column=0, sticky=W)
        percentage_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.percentage_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        percentage_ratio_value.grid(row=1, column=1)

    def perform_action(self):
        print("Action performed")
