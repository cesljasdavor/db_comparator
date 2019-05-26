from datetime import datetime

import providers
from error.exceptions import InvalidInputException
from utils.program_utils import get_milliseconds


def insert_point(x, y):
    if x is None or y is None or not isinstance(x, float) or not isinstance(y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for point")

    connection = providers.db_connection_provider.get_connection()
    inserted = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO spatial_core_point (point) VALUES (point({0}, {1}))
            """.format(x, y)
        )
        inserted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, inserted, get_milliseconds(start_time, end_time)


def insert_points(points):
    if points is None or not isinstance(points, list):
        raise InvalidInputException("Please provide points")

    connection = providers.db_connection_provider.get_connection()
    inserted = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.executemany("INSERT INTO spatial_core_point (point) VALUES (point(%s, %s))", points)
        inserted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, inserted, get_milliseconds(start_time, end_time)


def update_point_by_coordinates(x, y, step):
    if x is None or y is None or step is None \
            or not isinstance(x, float) \
            or not isinstance(y, float) \
            or not isinstance(step, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for existing point and update step.")

    connection = providers.db_connection_provider.get_connection()
    updated = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE spatial_core_point
                SET point = point(point[0] + {0}, point[1] + {0})
                WHERE point ~= point({1}, {2})
            """.format(step, x, y)
        )
        updated = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, updated, get_milliseconds(start_time, end_time)


def update_points_in_rectangle(bottom_left_corner, width, height, step):
    if bottom_left_corner is None or width is None or height is None or step is None\
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float) \
            or not isinstance(step, float):
        raise InvalidInputException("Please provide bottom left corner point, width and height of rectangle and update step.")

    connection = providers.db_connection_provider.get_connection()
    updated = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE spatial_core_point
                SET point = point(point[0] + {0}, point[1] + {0})
                WHERE point <@ box(point({1}, {2}), point({3}, {4}))
            """.format(
                step,
                bottom_left_corner[0],
                bottom_left_corner[1],
                bottom_left_corner[0] + width,
                bottom_left_corner[1] + height
            )
        )
        updated = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, updated, get_milliseconds(start_time, end_time)


def update_points_in_rotated_rectangle(bottom_left_corner, width, height, angle, step):
    if bottom_left_corner is None or width is None or height is None or angle is None or step is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float)\
            or not isinstance(angle, float) \
            or not isinstance(step, float):
        raise InvalidInputException("Please provide bottom left corner point, width, height and angle of rectangle and update step.")

    connection = providers.db_connection_provider.get_connection()
    updated = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE spatial_core_point
                SET point = point(point[0] + {0}, point[1] + {0})
                WHERE rotated_rectangle_contains(point, box(point({1}, {2}), point({3}, {4})), {5})
            """.format(
                step,
                bottom_left_corner[0],
                bottom_left_corner[1],
                bottom_left_corner[0] + width,
                bottom_left_corner[1] + height,
                angle
            )
        )
        updated = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, updated, get_milliseconds(start_time, end_time)


def update_points_in_circle(center, radius, step):
    if center is None or radius is None or step is None \
            or not isinstance(center, tuple) \
            or not isinstance(radius, float) \
            or not isinstance(step, float):
        raise InvalidInputException("Please provide circle center and radius and update step.")

    connection = providers.db_connection_provider.get_connection()
    updated = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE spatial_core_point
                SET point = point(point[0] + {0}, point[1] + {0})
                WHERE circle '(({1}, {2}), {3})' @> point;
            """. format(
                step,
                center[0],
                center[1],
                radius
            )
        )
        updated = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, updated, get_milliseconds(start_time, end_time)


def delete_point_by_coordinates(x, y):
    if x is None or y is None or not isinstance(x, float) or not isinstance(y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for point")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM spatial_core_point
                WHERE point ~= point({0}, {1})
            """.format(x, y)
        )
        deleted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, deleted, get_milliseconds(start_time, end_time)


def delete_points_in_rectangle(bottom_left_corner, width, height):
    if bottom_left_corner is None or width is None or height is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float):
        raise InvalidInputException("Please provide bottom left corner point, width and height of bounding box!")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM spatial_core_point
                WHERE point <@ box(point({0}, {1}), point({2}, {3}))
            """.format(
                bottom_left_corner[0],
                bottom_left_corner[1],
                bottom_left_corner[0] + width,
                bottom_left_corner[1] + height
            )
        )
        deleted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, deleted, get_milliseconds(start_time, end_time)


def delete_points_in_rotated_rectangle(bottom_left_corner, width, height, angle):
    if bottom_left_corner is None or width is None or height is None or angle is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float)\
            or not isinstance(angle, float):
        raise InvalidInputException("Please provide bottom left corner point, width, height and angle of rectangle!")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM spatial_core_point
                WHERE rotated_rectangle_contains(point, box(point({0}, {1}), point({2}, {3})), {4})
            """.format(
                bottom_left_corner[0],
                bottom_left_corner[1],
                bottom_left_corner[0] + width,
                bottom_left_corner[1] + height,
                angle
            )
        )
        deleted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, deleted, get_milliseconds(start_time, end_time)


def delete_points_in_circle(center, radius):
    if center is None or radius is None or not isinstance(center, tuple) or not isinstance(radius, float):
        raise InvalidInputException("Please provide circle center and radius!")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM spatial_core_point 
                WHERE circle '(({0}, {1}), {2})' @> point;
            """. format(
                center[0],
                center[1],
                radius
            )
        )
        deleted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        has_errors = "Yes"
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, deleted, get_milliseconds(start_time, end_time)


def find_point_by_coordinates(x, y):
    if x is None or y is None or not isinstance(x, float) or not isinstance(y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for point!")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM spatial_core_point
                WHERE point ~= point({0}, {1})
            """.format(x, y)
        )
        found = cursor.rowcount
        cursor.close()
    except Exception:
        has_errors = "Yes"
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, found, get_milliseconds(start_time, end_time)


def find_points_in_rectangle(bottom_left_corner, width, height):
    if bottom_left_corner is None or width is None or height is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float):
        raise InvalidInputException("Please provide bottom left corner point, width and height of bounding box!")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM spatial_core_point
                WHERE point <@ box(point({0}, {1}), point({2}, {3}))
            """.format(
                bottom_left_corner[0],
                bottom_left_corner[1],
                bottom_left_corner[0] + width,
                bottom_left_corner[1] + height
            )
        )
        found = cursor.rowcount
        cursor.close()
    except Exception:
        has_errors = "Yes"
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, found, get_milliseconds(start_time, end_time)


def find_points_in_rotated_rectangle(bottom_left_corner, width, height, angle):
    if bottom_left_corner is None or width is None or height is None or angle is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float)\
            or not isinstance(angle, float):
        raise InvalidInputException("Please provide bottom left corner point, width, height and angle of rectangle!")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM spatial_core_point
                WHERE rotated_rectangle_contains(point, box(point({0}, {1}), point({2}, {3})), {4})
            """.format(
                bottom_left_corner[0],
                bottom_left_corner[1],
                bottom_left_corner[0] + width,
                bottom_left_corner[1] + height,
                angle
            )
        )
        found = cursor.rowcount
        cursor.close()
    except Exception:
        has_errors = "Yes"
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, found, get_milliseconds(start_time, end_time)


def find_points_in_circle(center, radius):
    if center is None or radius is None or not isinstance(center, tuple) or not isinstance(radius, float):
        raise InvalidInputException("Please provide circle center and radius!")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    has_errors = "No"
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM spatial_core_point WHERE circle '(({0}, {1}), {2})' @> point;
            """. format(
                center[0],
                center[1],
                radius
            )
        )
        found = cursor.rowcount
        cursor.close()
    except Exception:
        has_errors = "Yes"
    finally:
        end_time = datetime.now()
        connection.close()

    return has_errors, found, get_milliseconds(start_time, end_time)

