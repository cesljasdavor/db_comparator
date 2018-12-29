import repositories.relational_point_repository as rp_repository
import repositories.spatial_point_repository as sp_repository
from tkinter import *

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
# results = rp_repository.find_points((0, 0), 10, 20)
# for result in results:
#     print(str(result))
# print(rp_repository.find_point(3))
# print(rp_repository.find_point_by_coordinates(x=5, y=15.65))


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
# print(sp_repository.find_point(2))
# print(sp_repository.find_point_by_coordinates(x=20.75, y=36.265))
# results = sp_repository.find_points((0, 0), 100, 100)
# for result in results:
#     print(str(result))
def compare_databases():
    print("console")


window = Tk()
window.title("Database Comparator")
# Center screen
# window.eval('tk::PlaceWindow %s center' % window.winfo_pathname(window.winfo_id()))
window.geometry("{0}x{1}".format(800, 650))
window.resizable(0, 0)
window.configure(bg="#313335")

input_frame = Frame(window, pady=50, bg="#313335")
input_frame.pack(side=TOP)

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


compare_button_frame = Frame(window, pady=10, bg="#313335")
compare_button_frame.pack(side=TOP)

compare_button = Button(
    compare_button_frame,
    text="Compare databases",
    command=compare_databases,
    bg="#28a745",
    activebackground="#25a341",
    fg="#ffffff",
    activeforeground="#ffffff",
    bd=0)
compare_button.pack(side=BOTTOM)
window.mainloop()
