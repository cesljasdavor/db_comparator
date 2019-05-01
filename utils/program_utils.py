import providers
from mappers.point_mapper import map_to_points


def reset_database():
    connection = providers.db_connection_provider.get_connection()
    try:
        # Create relational table
        cursor = connection.cursor()
        cursor.execute(
            """
                DROP TABLE IF EXISTS relational_point
            """
        )
        cursor.execute(
            """
                CREATE TABLE relational_point(
                    id serial primary key,
                    x double precision,
                    y double precision
                )
            """
        )
        cursor.execute(
            """
                CREATE INDEX relational_point_x_y_index ON relational_point (x, y)
            """
        )

        # Create relational table with point object
        cursor.execute(
            """
                DROP TABLE IF EXISTS relational_point_object
            """
        )
        cursor.execute(
            """
                CREATE TABLE relational_point_object(
                    id serial primary key,
                    point point
                )
            """
        )
        cursor.execute(
            """
                CREATE INDEX relational_point_object_index ON relational_point_object USING GIST (point);
            """
        )
        #

        # Create spatial table
        cursor.execute(
            """
                DROP TABLE IF EXISTS spatial_point
            """
        )
        cursor.execute(
            """
                CREATE TABLE spatial_point(
                    id serial primary key,
                    point geometry(POINT, 4326)
                )
            """
        )
        cursor.execute(
            """
                CREATE INDEX spatial_point_geometry_index ON spatial_point USING GIST (point);
            """
        )

        # Create functions
        cursor.execute(
            """
                create or replace function circle_contains(x float, y float, c_x float, c_y float, r float) returns boolean as $contains$
                declare
                    contains boolean;
                begin
                    contains = |/((x - c_x)^2 + (y - c_y)^2) <= r;
                    return contains;
                end;
                $contains$ LANGUAGE plpgsql;
            """
        )

        cursor.close()
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        connection.close()


def get_all_points():
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM relational_point
        """)
        return map_to_points(cursor.fetchall())
    except Exception:
        connection.rollback()
    finally:
        connection.close()


def get_milliseconds(start_time, end_time):
    return (end_time - start_time).total_seconds() * 1000
