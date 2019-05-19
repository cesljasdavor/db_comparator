from models.point import Point


def map_to_point(point_tuple):
    if point_tuple is None:
        return None

    return Point(x=float(point_tuple[0]), y=float(point_tuple[1]))


def map_to_points(point_tuples):
    points = []
    for point_tuple in point_tuples:
        points.append(map_to_point(point_tuple))

    return points
