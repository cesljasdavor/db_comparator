from tkinter import *


class Action(object):
    def __init__(self, window):
        self.window = window
        self.destroy_all_elements()

    def destroy_all_elements(self):
        first = True
        for child in self.window.winfo_children():
            if first:
                first = False
                continue

            child.destroy()

    def rename_window(self, title):
        self.window.title(title)

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
        pass
