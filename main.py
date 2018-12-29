from tkinter import *
from actions.delete_multiple import DeleteMultiple
from actions.delete_single import DeleteSingle
from actions.find_multiple import FindMultiple
from actions.find_single import FindSingle
from actions.insert_multiple import InsertMultiple
from actions.insert_single import InsertSingle
from actions.update_single import UpdateSingle

# Relational
# Insert
# rp_repository.insert_point(x=5.0, y=15.65)

# Update
# rp_repository.update_point(1, 2, 3)
# rp_repository.update_point_by_coordinates(2, 3, 5.0, 15.65)

# Delete
# rp_repository.delete_point(2)
# rp_repository.delete_point_by_coordinates(x=5.0, y=15.65)
# rp_repository.delete_points((0, 0), 10, 20)

# Find
# print(sp_repository.find_point(2))
# print(sp_repository.find_point_by_coordinates(x=20.75, y=36.265))
# results = sp_repository.find_points((0, 0), 100, 100)
# for result in results:
#     print(str(result))


# Spatial
# Insert
# sp_repository.insert_point(x=5.0, y=15.65)

# Update
# sp_repository.update_point(1, 2, 3)
# sp_repository.update_point_by_coordinates(2, 3, 5.0, 15.65)

# Delete
# sp_repository.delete_point(1)
# sp_repository.delete_point_by_coordinates(x=20.75, y=36.265)
# sp_repository.delete_points((0, 0), 100, 100)

# Find
# results = rp_repository.find_points((0, 0), 10, 20)
# for result in results:
#     print(str(result))
# print(rp_repository.find_point(3))
# print(rp_repository.find_point_by_coordinates(x=5, y=15.65))


def setup_menubar():
    menubar = Menu(
        window,
        bg="#212325",
        activebackground="#313335",
        fg="#ffffff",
        activeforeground="#ffffff",
        bd=0
    )
    window.config(menu=menubar)

    action_menu = Menu(
        menubar,
        tearoff=0,
        bg="#212325",
        activebackground="#313335",
        fg="#ffffff",
        activeforeground="#ffffff",
        bd=5
    )
    action_menu.add_command(label="Insert multiple", command=insert_multiple)
    action_menu.add_command(label="Insert single", command=insert_single)
    action_menu.add_command(label="Update single", command=update_single)
    action_menu.add_command(label="Delete multiple", command=delete_multiple)
    action_menu.add_command(label="Delete single", command=delete_single)
    action_menu.add_command(label="Find multiple", command=find_multiple)
    action_menu.add_command(label="Find single", command=find_single)

    menubar.add_cascade(label="Actions", menu=action_menu)
    menubar.add_command(label="Help", command=show_help)
    menubar.add_command(label="Exit", command=exit_app)


def insert_multiple():
    InsertMultiple(window)


def insert_single():
    InsertSingle(window)


def update_single():
    UpdateSingle(window)


def delete_multiple():
    DeleteMultiple(window)


def delete_single():
    DeleteSingle(window)


def find_multiple():
    FindMultiple(window)


def find_single():
    FindSingle(window)


def exit_app():
    window.destroy()


def show_help():
    help_window = Toplevel()
    help_window.title("Database Comparator - Help")
    help_window.geometry("{0}x{1}".format(600, 400))
    help_window.resizable(0, 0)
    help_window.configure(bg="#313335")

    help_title = Label(help_window, text="Help", anchor=CENTER, font=('Courier', 20), bg="#313335",
                       fg="#ffffff")
    help_title.pack(side=TOP, pady=(10, 10))
    help_text = """
Welcome to Database comparator. This small GUI application is created to compare spatial and relational 
database speeds.

Usage

1. Press on "File" -> "Load".
2. Find your .dbc file
3. Wait until all points are inserted in both spatial and relational database
4. Enter your query
5. View results

Created by Davor Češljaš, Faculty of Electrical engineering and Computing. 
All rights reserved ®  
    """
    help_message = Message(help_window, text=help_text, width=500, bg="#313335", fg="#ffffff")
    help_message.pack()


window = Tk()
window.title("Database Comparator")
window.resizable(0, 0)
window.configure(bg="#313335")
window.wm_iconname("database_comparator.png")
setup_menubar()

# Initialize window
FindMultiple(window)

window.mainloop()
