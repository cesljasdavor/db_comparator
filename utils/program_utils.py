import providers
from mappers.point_mapper import map_to_points


def reset_database(has_index=True):
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
                CREATE TABLE relational_point (
                    x double precision,
                    y double precision
                )
            """
        )
        if has_index:
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
        if has_index:
            cursor.execute(
                """
                    CREATE INDEX spatial_core_point_index ON spatial_core_point USING GIST (point);
                """
            )

        # Create spatial PostGIS table
        cursor.execute(
            """
                DROP TABLE IF EXISTS spatial_postgis_point
            """
        )
        cursor.execute(
            """
                CREATE TABLE spatial_postgis_point (
                    point geometry(POINT, 4326)
                )
            """
        )
        if has_index:
            cursor.execute(
                """
                    CREATE INDEX spatial_postgis_point_index ON spatial_postgis_point USING GIST (point);
                """
            )

        # Create Result table
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS result (
                    id bigserial primary key,
                    has_index boolean not null,
                    dataset text null,
                    dataset_size integer null,
                    operation text not null,
                    relational_point_count bigint not null,
                    relational_has_errors boolean not null,
                    relational_time_elapsed decimal(10, 3) not null,
                    relational_avg_time_per_point decimal(10, 3) not null,
                    spatial_core_point_count bigint not null,
                    spatial_core_has_errors boolean not null,
                    spatial_core_time_elapsed decimal(10, 3) not null,
                    spatial_core_avg_time_per_point decimal(10, 3) not null,
                    spatial_postgis_point_count bigint not null,
                    spatial_postgis_has_errors boolean not null,
                    spatial_postgis_time_elapsed decimal(10, 3) not null,
                    spatial_postgis_avg_time_per_point decimal(10, 3) not null,
                    rsc_ratio decimal(10, 3) not null,
                    rsp_ratio decimal(10, 3) not null,
                    spsc_ration decimal(10, 3) not null,
                    best text not null,
                    created_at timestamp(6) with time zone not null
                )
            """
        )

        # Create configuration table
        cursor.execute(
            """
                DROP TABLE IF EXISTS configuration
            """
        )
        cursor.execute(
            """
                CREATE TABLE configuration (
                    key text primary key,
                    value text not null
                )
            """
        )
        cursor.execute(
            """
                INSERT INTO configuration (key, value) VALUES ('active_dataset_key', 'unknown');
                INSERT INTO configuration (key, value) VALUES ('active_dataset_size_key', '0');
            """
        )
        providers.db_state["dataset"] = "unknown"
        providers.db_state["dataset_size"] = 0

        # Create functions
        cursor.execute(
            """
                CREATE OR REPLACE FUNCTION circle_contains(x float, y float, c_x float, c_y float, r float) RETURNS boolean as $contains$
                DECLARE
                    contains boolean;
                BEGIN
                    contains = |/((x - c_x)^2 + (y - c_y)^2) <= r;
                    return contains;
                END;
                $contains$ LANGUAGE plpgsql
            """
        )

        cursor.execute(
            """
                CREATE OR REPLACE FUNCTION rotated_rectangle_contains(x float, y float, s_x float, s_y float, width float, height float, angle float) RETURNS boolean as $contains$
                DECLARE
                    contains boolean;
                    negative_angle_radians float;
                    cos_angle float;
                    sin_angle float;
                    rotated_x float;
                    rotated_y float;
                BEGIN
                    negative_angle_radians = radians(-angle);
                    cos_angle = cos(negative_angle_radians);
                    sin_angle = sin(negative_angle_radians);
                    rotated_x = x * cos_angle - y * sin_angle;
                    rotated_y = y * cos_angle + x * sin_angle;
                    contains = rotated_x >= s_x and rotated_x <= s_x + width and rotated_y >= s_y and rotated_y <= s_y + height;
                    return contains;
                END;
                $contains$ LANGUAGE plpgsql
            """
        )

        cursor.execute(
            """
                CREATE OR REPLACE FUNCTION rotated_rectangle_contains(p point, b box, angle float) RETURNS boolean as $contains$
                DECLARE
                    contains boolean;
                    negative_angle_radians float;
                    rotated_p point;
                BEGIN
                    negative_angle_radians = radians(-angle);
                    rotated_p = p * point(cos(negative_angle_radians), sin(negative_angle_radians));
                    contains = rotated_p <@ b;
                    return contains;
                END;
                $contains$ LANGUAGE plpgsql
            """
        )

        cursor.close()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
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
