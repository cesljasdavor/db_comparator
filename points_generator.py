from random import uniform
from random import shuffle

import sys


def generate_uniform(file_name, number_of_points):
    with open(file_name, "w") as file:
        print("Created file:", file_name)
        for i in range(number_of_points):
            x, y = uniform(-180, 180), uniform(-90, 90)
            file.write("{0},{1}".format(x, y))
            if i < number_of_points - 1:
                file.write("\n")

    print("{0} points generated".format(number_of_points))


def generate_routers(file_name, step):
    with open(file_name, "w") as write_file, open("routers_init.dbcom", "r") as routers_file:
        print("Created file:", file_name)
        lines = routers_file.readlines()
        shuffle(lines)
        number_of_points = int(len(lines) / step)
        for i in range(number_of_points):
            point_line = lines[i * step].strip()
            write_file.write(point_line)
            if i < number_of_points - 1:
                write_file.write("\n")

    print("{0} points generated".format(number_of_points))


def main():
    try:
        program_type = sys.argv[1]
        if program_type != 'routers' and program_type != 'uniform':
            sys.exit("Please provide 'routers' or 'uniform' param.")

        if program_type == 'routers':
            generate_routers(sys.argv[2], int(sys.argv[3]))
        elif program_type == 'uniform':
            generate_uniform(sys.argv[2], int(sys.argv[3]))

    except Exception as e:
        sys.exit("You must provide program type, file name and number of points / step params")


if __name__ == "__main__":
    main()
