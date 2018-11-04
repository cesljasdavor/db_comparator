import providers
from error.output import print_error


class RelationalCoordinateRepository(object):

    def add_coordinate(self, coordinate):
        if coordinate is None:
            print_error("Coordinate cannot be None")
            return

        connection = providers.db_connection_provider.get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                    INSERT INTO relational_coordinates (x, y) VALUES ({0}, {1})
                """.format(coordinate.x, coordinate.y)
            )
            cursor.close()

            connection.commit()
            print("Coordinate successfully added: " + str(coordinate))
        except Exception as e:
            print_error("Unable to add coordinate: {0}. {1}".format(str(coordinate), str(e)))
            connection.rollback()
        finally:
            connection.close()
