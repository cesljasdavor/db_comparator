import providers
from datetime import datetime
from utils.program_utils import get_milliseconds
from error.output import print_error
from mappers.point_mapper import map_to_point, map_to_points


def insert_point(x, y):
    if x is None or y is None:
        print_error("Please provide 'x' and 'y' values for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO relational_point (x, y) VALUES ({0}, {1})
            """.format(x, y)
        )
        cursor.close()
        connection.commit()

        print("Point (x={0}, y={1}) successfully inserted!".format(str(x), str(y)))
    except Exception as e:
        print_error("Unable to insert point (x={0}, y={1})! {2}".format(str(x), str(y), str(e)))
        connection.rollback()
    finally:
        connection.close()


def insert_points(points):
    if points is None:
        print_error("Please provide points")
        return

    connection = providers.db_connection_provider.get_connection()
    errors = []
    try:
        start_time = datetime.now()
        for x, y in points:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                        INSERT INTO relational_point (x, y) VALUES ({0}, {1})
                    """.format(x, y)
                )
                cursor.close()
                connection.commit()
            except Exception as e:
                errors.append(e)
                connection.rollback()
    finally:
        end_time = datetime.now()
        connection.close()

    return len(errors), len(points), get_milliseconds(start_time, end_time)


def update_point(point_id, new_x, new_y):
    if point_id is None or new_x is None or new_y is None:
        print_error("Please provide 'id' for existing point, and new 'x' and 'y' values")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE relational_point
                SET x = {0}, y = {1}
                WHERE id = {2}
            """.format(new_x, new_y, point_id)
        )
        cursor.close()
        connection.commit()

        print("Point successfully updated!")
    except Exception as e:
        print_error("Unable to update point with id: {0}. {1}".format(point_id, str(e)))
        connection.rollback()
    finally:
        connection.close()


def update_point_by_coordinates(x, y, new_x, new_y):
    if x is None or y is None or new_x is None or new_y is None:
        print_error("Please provide 'x' and 'y' values for existing point and new 'x' and 'y' values")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE relational_point
                SET x = {0}, y = {1}
                WHERE x = {2} AND y = {3}
            """.format(new_x, new_y, x, y)
        )
        cursor.close()
        connection.commit()

        print("Point successfully updated!")
    except Exception as e:
        print_error("Unable to update point (x={0}, y={1})! {2}".format(str(x), str(y), str(e)))
        connection.rollback()
    finally:
        connection.close()


def delete_point(point_id):
    if point_id is None:
        print_error("Please provide 'id' for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM relational_point
                WHERE id = {0}
            """.format(point_id)
        )
        cursor.close()
        connection.commit()

        print("Point successfully deleted!")
    except Exception as e:
        print_error("Unable to delete point with id: {0}. {1}".format(point_id, str(e)))
        connection.rollback()
    finally:
        connection.close()


def delete_point_by_coordinates(x, y):
    if x is None or y is None:
        print_error("Please provide 'x' and 'y' values for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM relational_point 
                WHERE x = {0} AND y = {1}
            """.format(x, y)
        )
        cursor.close()
        connection.commit()

        print("Point successfully deleted!")
    except Exception as e:
        print_error("Unable to delete point (x={0}, y={1})! {2}".format(str(x), str(y), str(e)))
        connection.rollback()
    finally:
        connection.close()


def delete_points(bottom_left_corner, width, height):
    if bottom_left_corner is None or width is None or height is None:
        print_error("Please provide bottom left corner point, width and height of bounding box!")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM relational_point
                WHERE x >= {0} AND x <= {1} AND y >= {2} AND y <= {3}
            """.format(
                bottom_left_corner[0],
                bottom_left_corner[0] + width,
                bottom_left_corner[1],
                bottom_left_corner[1] + height
            )
        )
        cursor.close()
        connection.commit()

        print("Points successfully deleted!")
    except Exception as e:
        print_error("Unable to delete points! {0}".format(str(e)))
        connection.rollback()
    finally:
        connection.close()


def find_point(point_id):
    if point_id is None:
        print_error("Please provide 'id' for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM relational_point 
                WHERE id = {0}
            """.format(point_id)
        )

        return map_to_point(cursor.fetchone())
    except Exception as e:
        print_error("Unable to find point! {0}".format(str(e)))
    finally:
        connection.close()


def find_point_by_coordinates(x, y):
    if x is None or y is None:
        print_error("Please provide 'x' and 'y' values for point!")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM relational_point 
                WHERE x = {0} AND y = {1}
            """.format(x, y)
        )

        return map_to_point(cursor.fetchone())
    except Exception as e:
        print_error("Unable to find point  (x={0}, y={1})! {2}".format(str(x), str(y), str(e)))
    finally:
        connection.close()


def find_points(bottom_left_corner, width, height):
    if bottom_left_corner is None or width is None or height is None:
        print_error("Please provide bottom left corner point, width and height of bounding box!")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT * FROM relational_point
                WHERE x >= {0} AND x <= {1} AND y >= {2} AND y <= {3}
            """.format(
                bottom_left_corner[0],
                bottom_left_corner[0] + width,
                bottom_left_corner[1],
                bottom_left_corner[1] + height
            )
        )

        return map_to_points(cursor.fetchall())
    except Exception as e:
        print_error("Unable to find points! {0}".format(str(e)))
    finally:
        connection.close()
