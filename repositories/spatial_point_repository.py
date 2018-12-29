import providers
from error.output import print_error
from mappers.point_mapper import map_to_point, map_to_points


def insert_point(x, y):
    if x is None or y is None:
        print_error("Please provide 'x' and 'y ' values for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO spatial_point (point) VALUES (st_geomfromtext('POINT({0} {1})', 4326))
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


def update_point(id, new_x, new_y):
    if id is None or new_x is None or new_y is None:
        print_error("Please provide 'id' for existing point, and new 'x' and 'y' values")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                UPDATE spatial_point
                SET point = st_geomfromtext('POINT({0} {1})', 4326)
                WHERE id = {2}
            """.format(new_x, new_y, id)
        )
        cursor.close()
        connection.commit()

        print("Point successfully updated!")
    except Exception as e:
        print_error("Unable to update point with id: {0}. {1}".format(id, str(e)))
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
                UPDATE spatial_point
                SET point = st_geomfromtext('POINT({0} {1})', 4326)
                WHERE st_intersects(point, st_geomfromtext('POINT({2} {3})', 4326))
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


def delete_point(id):
    if id is None:
        print_error("Please provide 'id' for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                DELETE FROM spatial_point
                WHERE id = {0}
            """.format(id)
        )
        cursor.close()
        connection.commit()

        print("Point successfully deleted!")
    except Exception as e:
        print_error("Unable to delete point with id: {0}. {1}".format(id, str(e)))
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
                DELETE FROM spatial_point 
                WHERE st_intersects(point, st_geomfromtext('POINT({0} {1})', 4326))
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
                DELETE FROM spatial_point
                WHERE st_contains(st_makeenvelope({0}, {2}, {1}, {3}, 4326), point)
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


def find_point(id):
    if id is None:
        print_error("Please provide 'id' for point")
        return

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT id, st_x(point), st_y(point) FROM spatial_point
                WHERE id = {0}
            """.format(id)
        )

        return map_to_point(cursor.fetchone())
    except Exception as e:
        print_error("Unable to find point with id: {0}! {1}".format(id, e))
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
                SELECT id, st_x(point), st_y(point) FROM spatial_point 
                WHERE st_intersects(point, st_geomfromtext('POINT({0} {1})', 4326))
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
                SELECT id, st_x(point), st_y(point) FROM spatial_point
                WHERE st_contains(st_makeenvelope({0}, {2}, {1}, {3}, 4326), point)
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
