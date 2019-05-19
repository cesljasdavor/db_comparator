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
                    x double precision,
                    y double precision
                )
            """
        )
        cursor.execute(
            """
                CREATE INDEX relational_point_index ON relational_point (x, y)
            """
        )

        # Create spatial core table
        cursor.execute(
            """
                DROP TABLE IF EXISTS spatial_core_point
            """
        )
        cursor.execute(
            """
                CREATE TABLE spatial_core_point(
                    point point
                )
            """
        )
        cursor.execute(
            """
                CREATE INDEX spatial_core_point_index ON spatial_core_point USING GIST (point);
            """
        )
        #

        # Create spatial PostGIS table
        cursor.execute(
            """
                DROP TABLE IF EXISTS spatial_postgis_point
            """
        )
        cursor.execute(
            """
                CREATE TABLE spatial_postgis_point(
                    point geometry(POINT, 4326)
                )
            """
        )
        cursor.execute(
            """
                CREATE INDEX spatial_postgis_point_index ON spatial_postgis_point USING GIST (point);
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
                $contains$ LANGUAGE plpgsql
            """
        )

        cursor.execute(
            """
                create or replace function rotated_rectangle_contains(x float, y float, s_x float, s_y float, width float, height float, angle float) returns boolean as $contains$
                declare
                    contains boolean;
                    negative_angle_radians float;
                    cos_angle float;
                    sin_angle float;
                    rotated_x float;
                    rotated_y float;
                begin
                    negative_angle_radians = radians(-angle);
                    cos_angle = cos(negative_angle_radians);
                    sin_angle = sin(negative_angle_radians);
                    rotated_x = x * cos_angle - y * sin_angle;
                    rotated_y = y * cos_angle + x * sin_angle;
                    contains = rotated_x >= s_x and rotated_x <= s_x + width and rotated_y >= s_y and rotated_y <= s_y + height;
                    return contains;
                end;
                $contains$ LANGUAGE plpgsql
            """
        )

        cursor.execute(
            """
                create or replace function rotated_rectangle_contains(p point, b box, angle float) returns boolean as $contains$
                declare
                    contains boolean;
                    negative_angle_radians float;
                    rotated_p point;
                begin
                    negative_angle_radians = radians(-angle);
                    rotated_p = p * point(cos(negative_angle_radians), sin(negative_angle_radians));
                    contains = rotated_p <@ b;
                    return contains;
                end;
                $contains$ LANGUAGE plpgsql
            """
        )

        cursor.close()
        connection.commit()
    except Exception as e:
        connection.rollback()
    finally:
        connection.close()


def get_all_relational_points():
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


def get_all_spatial_core_points():
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.point[0] x, p.point[1] y FROM spatial_core_point p
        """)
        return map_to_points(cursor.fetchall())
    except Exception:
        connection.rollback()
    finally:
        connection.close()


def get_all_spatial_postgis_points():
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT st_x(p.point) x, st_y(p.point) y FROM spatial_postgis_point p
        """)
        return map_to_points(cursor.fetchall())
    except Exception:
        connection.rollback()
    finally:
        connection.close()


def get_milliseconds(start_time, end_time):
    return (end_time - start_time).total_seconds() * 1000
