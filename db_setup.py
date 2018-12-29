import providers

connection = providers.db_connection_provider.get_connection()

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

cursor.close()
connection.commit()
