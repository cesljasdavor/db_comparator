from actions.action import Action
from tkinter import filedialog
from tkinter import *

from repositories import relational_point_repository as rp_repository
from repositories import spatial_point_repository as sp_repository
from parsers.dbcom_parser import DbcomParser
from utils.gui_utils import LoadingScreen


class InsertMultiple(Action):

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
        self.points = None

        self.init_gui()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text="Insert Multiple", anchor=CENTER, font=('Courier', 20), bg="#313335",
                             fg="#ffffff")
        action_title.pack(side=TOP, pady=(10, 10))

        input_frame = Frame(self.window, bg="#313335")
        input_frame.pack(side=TOP, pady=(15, 10), padx=(10, 10))

        action_button_frame = Frame(self.window, bg="#313335")
        action_button_frame.pack(side=TOP, pady=(10, 15), padx=(10, 10))

        load_button = Button(
            action_button_frame,
            text="Load points",
            command=self.load_points,
            bg="#0069d9",
            activebackground="#036cdc",
            fg="#ffffff",
            activeforeground="#ffffff",
            bd=0
        )
        load_button.pack(side=LEFT, pady=(0, 15), padx=(10, 10))
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
        action_button.pack(side=LEFT, pady=(0, 15))

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
            text="Ratio percentage",
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
        loading_screen = LoadingScreen("Inserting to database", "Initializing...")
        r_error_count, r_points_count, r_time_elapsed = rp_repository.insert_points(self.points)
        loading_screen.set_message("Points inserted to relational database.")
        loading_screen.set_progress_value(50.0)
        s_error_count, s_points_count, s_time_elapsed = sp_repository.insert_points(self.points)
        loading_screen.set_message("Points inserted to spatial database.")
        loading_screen.set_progress_value(100.0)
        loading_screen.close()

        print(r_error_count, r_points_count, r_time_elapsed)
        print(s_error_count, s_points_count, s_time_elapsed)

    def load_points(self):
        file_name = filedialog.askopenfilename(
            initialdir=".",
            title="Select file",
            filetypes=[("Database comparator file", "*.dbcom")]
        )

        parser = DbcomParser(file_name)
        parser.parse()
        self.points = parser.points
