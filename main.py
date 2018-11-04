# import psycopg2 as db_client
# connection = db_client.connect(database="db_comparator", user="postgres", password="postgres", host="localhost")
# cursor = connection.cursor()
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS relational_coordinate(
#     id serial primary key,
#     x double precision,
#     y double precision
# )
# """)
# cursor.close()
# connection.commit()
#
# connection = db_client.connect(database="db_comparator", user="postgres", password="postgres", host="localhost")
# cursor = connection.cursor()
# cursor.execute("""
#     INSERT INTO relational_coordinates (x, y) VALUES (1, 0)
# """)
#
# rows = cursor.fetchall()
#
# print(str(rows))
import repositories
from models.relational_coordinate import RelationalCoordinate

repositories.relational_coordinate_repository.add_coordinate(RelationalCoordinate(x=1.25, y=2.75))