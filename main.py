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
from program import Program


def main():
    program = Program()
    program.start()


if __name__ == "__main__":
    main()
