from datetime import datetime

import providers
from error.exceptions import InvalidInputException
from utils.program_utils import get_milliseconds


def insert_point(x, y):
    if x is None or y is None or not isinstance(x, float) or not isinstance(y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for point")

    connection = providers.db_connection_provider.get_connection()
    inserted = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO relational_point_object (point) VALUES (point({0}, {1}))
            """.format(x, y)
        )
        inserted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        errors = 1
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, inserted, get_milliseconds(start_time, end_time)


def insert_points(points):
    if points is None or not isinstance(points, list):
        raise InvalidInputException("Please provide points")

    connection = providers.db_connection_provider.get_connection()
    inserted = 0
    errors = 0
    start_time = datetime.now()
    try:
        for x, y in points:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                        INSERT INTO relational_point_object (point) VALUES (point({0}, {1}))
                    """.format(x, y)
                )
                inserted += cursor.rowcount
                cursor.close()
                connection.commit()
            except Exception:
                errors += 1
                connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, inserted, get_milliseconds(start_time, end_time)


def update_point(point_id, new_x, new_y):
    if point_id is None or new_x is None or new_y is None \
            or not isinstance(point_id, int) \
            or not isinstance(new_x, float) \
            or not isinstance(new_y, float):
        print(point_id, new_x, new_y)
        raise InvalidInputException("Please provide 'id' for existing point, and new 'x' and 'y' values")

    connection = providers.db_connection_provider.get_connection()
    updated = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE relational_point_object
                SET point = point({0}, {1})
                WHERE id = {2}
            """.format(new_x, new_y, point_id)
        )
        updated = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        errors = 1
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, updated, get_milliseconds(start_time, end_time)


def update_point_by_coordinates(x, y, new_x, new_y):
    if x is None or y is None or new_x is None or new_y is None \
            or not isinstance(x, float) \
            or not isinstance(y, float) \
            or not isinstance(new_x, float) \
            or not isinstance(new_y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for existing point and new 'x' and 'y' values")

    connection = providers.db_connection_provider.get_connection()
    updated = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE relational_point_object
                SET point = point({0}, {1})
                WHERE point ~= point({2}, {3})
            """.format(new_x, new_y, x, y)
        )
        updated = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        errors = 1
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, updated, get_milliseconds(start_time, end_time)


def delete_point(point_id):
    if point_id is None or not isinstance(point_id, int):
        raise InvalidInputException("Please provide 'id' for point")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM relational_point_object
                WHERE id = {0}
            """.format(point_id)
        )
        deleted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        errors = 1
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, deleted, get_milliseconds(start_time, end_time)


def delete_point_by_coordinates(x, y):
    if x is None or y is None or not isinstance(x, float) or not isinstance(y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for point")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM relational_point_object
                WHERE point ~= point({0}, {1})
            """.format(x, y)
        )
        deleted = cursor.rowcount
        cursor.close()
        connection.commit()
    except Exception:
        errors = 1
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, deleted, get_milliseconds(start_time, end_time)


def delete_points(bottom_left_corner, width, height):
    if bottom_left_corner is None or width is None or height is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float):
        raise InvalidInputException("Please provide bottom left corner point, width and height of bounding box!")

    connection = providers.db_connection_provider.get_connection()
    deleted = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM relational_point_object
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
        errors = 1
        connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, deleted, get_milliseconds(start_time, end_time)


def find_point(point_id):
    if point_id is None or not isinstance(point_id, int):
        raise InvalidInputException("Please provide 'id' for point")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM relational_point_object
                WHERE id = {0}
            """.format(point_id)
        )
        found = cursor.rowcount
        cursor.close()
    except Exception:
        errors = 1
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, found, get_milliseconds(start_time, end_time)


def find_point_by_coordinates(x, y):
    if x is None or y is None or not isinstance(x, float) or not isinstance(y, float):
        raise InvalidInputException("Please provide 'x' and 'y' values for point!")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM relational_point_object
                WHERE point ~= point({0}, {1})
            """.format(x, y)
        )
        found = cursor.rowcount
        cursor.close()
    except Exception:
        errors = 1
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, found, get_milliseconds(start_time, end_time)


def find_points(bottom_left_corner, width, height):
    if bottom_left_corner is None or width is None or height is None \
            or not isinstance(bottom_left_corner, tuple) \
            or not isinstance(width, float) \
            or not isinstance(height, float):
        raise InvalidInputException("Please provide bottom left corner point, width and height of bounding box!")

    connection = providers.db_connection_provider.get_connection()
    found = 0
    errors = 0
    start_time = datetime.now()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM relational_point_object
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
        errors = 1
    finally:
        end_time = datetime.now()
        connection.close()

    return errors, found, get_milliseconds(start_time, end_time)
