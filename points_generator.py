from random import uniform

import sys


def main():
    try:
        file_name = sys.argv[1]
        number_of_points = int(sys.argv[2])
    except Exception as e:
        sys.exit("You must provide file name and number of points")

    with open(file_name, "w") as file:
        print("Created file:", file_name)
        for i in range(number_of_points):
            x, y = uniform(-180, 180), uniform(-90, 90)
            file.write("{0},{1}".format(x, y))
            if i < number_of_points - 1:
                file.write("\n")

    print("{0} points generated".format(number_of_points))


if __name__ == "__main__":
    main()
