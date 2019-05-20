from random import uniform
from random import normalvariate
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


def generate_routers(file_name, step, extra_points, sigma):
    with open(file_name, "w") as write_file, open("routers_init.dbcom", "r") as routers_file:
        print("Created file:", file_name)
        lines = routers_file.readlines()
        shuffle(lines)
        number_of_points = int(len(lines) / step)
        for i in range(number_of_points):
            point_line = lines[i * step].strip()
            if extra_points is not None and sigma is not None:
                mu_x_str, mu_y_str = point_line.split(",")
                mu_x, mu_y = float(mu_x_str), float(mu_y_str)
                for j in range(extra_points):
                    x, y = normalvariate(mu_x, sigma), normalvariate(mu_y, sigma)
                    write_file.write("{0},{1}".format(str(x), str(y)))
                    write_file.write("\n")

            write_file.write(point_line)
            if i < number_of_points - 1:
                write_file.write("\n")

    total_points = number_of_points * (extra_points if extra_points is not None else 1)
    print("{0} points generated".format(total_points))


def main():
    try:
        program_type = sys.argv[1]
        if program_type != 'routers' and program_type != 'uniform':
            sys.exit("Please provide 'routers' or 'uniform' param.")

        if program_type == 'routers':
            file_name = sys.argv[2]
            step = int(sys.argv[3])
            extra_points = None
            sigma = None
            if len(sys.argv) == 6:
                extra_points = int(sys.argv[4])
                sigma = float(sys.argv[5])

            generate_routers(file_name, step, extra_points, sigma)
        elif program_type == 'uniform':
            file_name = sys.argv[2]
            number_of_points = int(sys.argv[3])

            generate_uniform(file_name, number_of_points)

    except Exception as e:
        sys.exit("You must provide program type, file name and number of points / step params")


if __name__ == "__main__":
    main()
