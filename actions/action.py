from threading import Thread
from tkinter import *


class Action(object):
    def __init__(self, window):
        self.window = window
        self.destroy_all_elements()

        # Statistics
        self.relational_point_count_var = StringVar(value="NaN")
        self.relational_has_errors_var = StringVar(value="None")
        self.relational_time_spent_var = StringVar(value="NaN")
        self.relational_avg_time_per_point_var = StringVar(value="NaN")
        self.spatial_core_point_count_var = StringVar(value="NaN")
        self.spatial_core_has_errors_var = StringVar(value="None")
        self.spatial_core_time_spent_var = StringVar(value="NaN")
        self.spatial_core_avg_time_per_point_var = StringVar(value="NaN")
        self.spatial_postgis_point_count_var = StringVar(value="NaN")
        self.spatial_postgis_has_errors_var = StringVar(value="None")
        self.spatial_postgis_time_spent_var = StringVar(value="NaN")
        self.spatial_postgis_avg_time_per_point_var = StringVar(value="NaN")
        self.best_database_var = StringVar(value="None")
        self.rsp_ratio_var = StringVar(value="NaN")
        self.spsc_ratio_var = StringVar(value="NaN")
        self.rsc_ratio_var = StringVar(value="NaN")

    def destroy_all_elements(self):
        first = True
        for child in self.window.winfo_children():
            if first:
                first = False
                continue

            child.destroy()

    def rename_window(self, title):
        self.window.title(title)

    def create_statistics(self):
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

        relational_has_errors_label = Label(
            relational_label_frame,
            text="Has Errors",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_has_errors_label.grid(row=1, column=0, sticky=W)
        relational_has_errors_value = Label(
            relational_label_frame,
            textvariable=self.relational_has_errors_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        relational_has_errors_value.grid(row=1, column=1)

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

        # Spatial Core
        spatial_core_label_frame = LabelFrame(
            action_statistics_frame,
            text="Spatial Core database",
            labelanchor=N,
            bg="#313335",
            fg="#ffffff",
            pady=10
        )
        spatial_core_label_frame.pack(side=LEFT, fill="both", expand="yes", pady=(15, 0))

        spatial_core_point_count_label = Label(
            spatial_core_label_frame,
            text="Point count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_point_count_label.grid(row=0, column=0, sticky=W)
        spatial_core_point_count_value = Label(
            spatial_core_label_frame,
            textvariable=self.spatial_core_point_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_point_count_value.grid(row=0, column=1)

        spatial_core_has_errors_label = Label(
            spatial_core_label_frame,
            text="Has Errors",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_has_errors_label.grid(row=1, column=0, sticky=W)
        spatial_core_has_errors_value = Label(
            spatial_core_label_frame,
            textvariable=self.spatial_core_has_errors_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_has_errors_value.grid(row=1, column=1)

        spatial_core_time_spent_label = Label(
            spatial_core_label_frame,
            text="Time spent",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_time_spent_label.grid(row=2, column=0, sticky=W)
        spatial_core_time_spent_value = Label(
            spatial_core_label_frame,
            textvariable=self.spatial_core_time_spent_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_time_spent_value.grid(row=2, column=1)

        spatial_core_avg_time_per_point_label = Label(
            spatial_core_label_frame,
            text="Average time per point",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_avg_time_per_point_label.grid(row=3, column=0, sticky=W)
        spatial_core_avg_time_per_point_value = Label(
            spatial_core_label_frame,
            textvariable=self.spatial_core_avg_time_per_point_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_core_avg_time_per_point_value.grid(row=3, column=1)

        # Spatial PostGIS
        spatial_postgis_label_frame = LabelFrame(
            action_statistics_frame,
            text="Spatial PostGIS database",
            labelanchor=N,
            bg="#313335",
            fg="#ffffff",
            pady=10
        )
        spatial_postgis_label_frame.pack(side=LEFT, fill="both", expand="yes", pady=(15, 0))

        spatial_postgis_point_count_label = Label(
            spatial_postgis_label_frame,
            text="Point count",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_point_count_label.grid(row=0, column=0, sticky=W)
        spatial_postgis_point_count_value = Label(
            spatial_postgis_label_frame,
            textvariable=self.spatial_postgis_point_count_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_point_count_value.grid(row=0, column=1)

        spatial_postgis_has_errors_label = Label(
            spatial_postgis_label_frame,
            text="Has Errors",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_has_errors_label.grid(row=1, column=0, sticky=W)
        spatial_postgis_has_errors_value = Label(
            spatial_postgis_label_frame,
            textvariable=self.spatial_postgis_has_errors_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_has_errors_value.grid(row=1, column=1)

        spatial_postgis_time_spent_label = Label(
            spatial_postgis_label_frame,
            text="Time spent",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_time_spent_label.grid(row=2, column=0, sticky=W)
        spatial_postgis_time_spent_value = Label(
            spatial_postgis_label_frame,
            textvariable=self.spatial_postgis_time_spent_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_time_spent_value.grid(row=2, column=1)

        spatial_postgis_avg_time_per_point_label = Label(
            spatial_postgis_label_frame,
            text="Average time per point",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_avg_time_per_point_label.grid(row=3, column=0, sticky=W)
        spatial_postgis_avg_time_per_point_value = Label(
            spatial_postgis_label_frame,
            textvariable=self.spatial_postgis_avg_time_per_point_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spatial_postgis_avg_time_per_point_value.grid(row=3, column=1)

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

        rsc_ratio_label = Label(
            action_overall_data_frame,
            text="Relational / Spatial Core",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        rsc_ratio_label.grid(row=1, column=0, sticky=W)
        rsc_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.rsc_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        rsc_ratio_value.grid(row=1, column=1)

        rsp_ratio_label = Label(
            action_overall_data_frame,
            text="Relational / Spatial PostGIS",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        rsp_ratio_label.grid(row=2, column=0, sticky=W)
        rsp_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.rsp_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        rsp_ratio_value.grid(row=2, column=1)

        spsc_ratio_label = Label(
            action_overall_data_frame,
            text="Spatial PostGIS / Spatial Core",
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spsc_ratio_label.grid(row=3, column=0, sticky=W)
        spsc_ratio_value = Label(
            action_overall_data_frame,
            textvariable=self.spsc_ratio_var,
            bg="#313335",
            fg="#ffffff",
            padx=20
        )
        spsc_ratio_value.grid(row=3, column=1)

    def create_footer(self):
        footer_frame = Frame(self.window, bg="#212325")
        footer_frame.pack(side=TOP, fill="both")

        footer_label = Label(
            footer_frame,
            text="Created by Davor Češljaš ®",
            bg="#212325",
            fg="#ffffff"
        )
        footer_label.pack(side=TOP, pady=(3, 3))

    def perform_action(self):
        thread = Thread(target=self.action)
        thread.start()

    def action(self):
        pass

    def show_statistics(self, relational_data, spatial_core_data, spatial_postgis_data):
        r_has_errors, r_points_count, r_time_elapsed = relational_data
        sc_has_errors, sc_points_count, sc_time_elapsed = spatial_core_data
        sp_has_errors, sp_points_count, sp_time_elapsed = spatial_postgis_data

        self.relational_has_errors_var.set(value=r_has_errors)
        self.relational_point_count_var.set(value=r_points_count)
        self.relational_time_spent_var.set(value="{0:.3f} ms".format(r_time_elapsed))
        self.relational_avg_time_per_point_var.set(
            "{0:.3f} ms".format(
                r_time_elapsed / r_points_count if r_points_count > 0 else 0
            )
        )

        self.spatial_core_has_errors_var.set(value=sc_has_errors)
        self.spatial_core_point_count_var.set(value=sc_points_count)
        self.spatial_core_time_spent_var.set(value="{0:.3f} ms".format(sc_time_elapsed))
        self.spatial_core_avg_time_per_point_var.set(
            "{0:.3f} ms".format(
                sc_time_elapsed / sc_points_count if sc_points_count > 0 else 0
            )
        )

        self.spatial_postgis_has_errors_var.set(value=sp_has_errors)
        self.spatial_postgis_point_count_var.set(value=sp_points_count)
        self.spatial_postgis_time_spent_var.set(value="{0:.3f} ms".format(sp_time_elapsed))
        self.spatial_postgis_avg_time_per_point_var.set(
            "{0:.3f} ms".format(
                sp_time_elapsed / sp_points_count if sp_points_count > 0 else 0
            )
        )

        self.rsc_ratio_var.set(value="{0:.3f}".format(r_time_elapsed / sc_time_elapsed))
        self.rsp_ratio_var.set(value="{0:.3f}".format(r_time_elapsed / sp_time_elapsed))
        self.spsc_ratio_var.set(value="{0:.3f}".format(sp_time_elapsed / sc_time_elapsed))

        if sc_time_elapsed < r_time_elapsed and sc_time_elapsed < sp_time_elapsed:
            best = "Spatial Core"
        elif r_time_elapsed < sc_time_elapsed and r_time_elapsed < sp_time_elapsed:
            best = "Relational"
        else:
            best = "Spatial PostGIS"

        self.best_database_var.set(value=best)