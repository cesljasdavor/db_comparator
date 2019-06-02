from threading import Thread

from actions.action import Action
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox

from providers import db_state
from repositories import relational_point_repository as rp_repository, configuration_repository
from repositories import spatial_core_repository as scp_repository
from repositories import spatial_postgis_point_repository as spp_repository
from parsers.dbcom_parser import DbcomParser
from utils.gui_utils import LoadingScreen


class InsertMultiple(Action):

    def __init__(self, window):
        super().__init__(window)
        self.title = "Insert Multiple"
        self.rename_window("Database Comparator - {0}".format(self.title))

        self.file_name = None
        self.points = None

        self.init_gui()
        self.create_statistics()
        self.create_footer()

    def init_gui(self):
        action_title = Label(self.window, text=self.title, anchor=CENTER, font=('Courier', 20), bg="#313335",
                             fg="#ffffff")
        action_title.pack(side=TOP, pady=(10, 10))

        input_frame = Frame(self.window, bg="#313335")
        input_frame.pack(side=TOP, pady=(15, 10), padx=(10, 10))

        action_button_frame = Frame(self.window, bg="#313335")
        action_button_frame.pack(side=TOP, pady=(10, 15), padx=(10, 10))

        load_button = Button(
            action_button_frame,
            text="Load points",
            command=self.perform_load_points,
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

    def perform_load_points(self):
        thread = Thread(target=self.load_points)
        thread.start()

    def load_points(self):
        self.file_name = filedialog.askopenfilename(
            initialdir=".",
            title="Select file",
            filetypes=[("Database comparator file", "*.dbcom")]
        )
        if self.file_name is None or len(self.file_name) == 0:
            return

        try:
            parser = DbcomParser(self.file_name)
            parser.parse()
            self.points = parser.points
        except Exception:
            messagebox.showerror(title="Parse error", message="Unable to parse points from file {0}".format(file_name))

    def action(self):
        if self.points is None:
            messagebox.showerror(title="No points", message="No points loaded! Please load points first.")
            return

        loading_screen = LoadingScreen(self.window, "Inserting to database", "Initializing...")
        loading_screen.set_message("Inserting points to relational database...")
        relational_data = rp_repository.insert_points(self.points)
        loading_screen.set_message("Points inserted to relational database.")
        loading_screen.set_progress_value(33.33)
        loading_screen.set_message("Inserting points to spatial Core database...")
        spatial_core_data = scp_repository.insert_points(self.points)
        loading_screen.set_message("Points inserted to spatial Core database.")
        loading_screen.set_progress_value(66.66)
        loading_screen.set_message("Inserting points to spatial PostGIS database...")
        spatial_postgis_data = spp_repository.insert_points(self.points)
        loading_screen.set_message("Points inserted to spatial PostGIS database.")
        loading_screen.set_progress_value(100.0)
        loading_screen.set_message("Done.")
        loading_screen.close()

        self.change_active_dataset()
        self.show_statistics(self.title, relational_data, spatial_core_data, spatial_postgis_data)

    def change_active_dataset(self):
        dataset_file_name = self.file_name.split("/")[-1]
        dataset = dataset_file_name.split(".")[0]
        dataset_size = len(self.points)

        configuration_repository.set_active_dataset(dataset)
        configuration_repository.set_active_dataset_size(dataset_size)

        db_state["dataset"] = dataset
        db_state["dataset_size"] = dataset_size
