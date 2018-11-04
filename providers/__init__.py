from providers.db_providers import DatabaseConnectionProvider
import sys
import getopt
from error.output import print_error

db_connection_provider = None


def create_db_connection_provider():
    global db_connection_provider

    if len(sys.argv[1:]) != 5:
        db_connection_provider = DatabaseConnectionProvider()
        return

    optlist, args = getopt.getopt(sys.argv[1:], "db:host:port:user:pass")
    if len(optlist) != 5:
        db_connection_provider = DatabaseConnectionProvider()
        return

    connection_options = dict(optlist)
    db_connection_provider = DatabaseConnectionProvider(
        db=connection_options["db"],
        host=connection_options["host"],
        port=int(connection_options["port"]),
        user=connection_options["user"],
        password=connection_options["pass"]
    )


def test_connection():
    connection = db_connection_provider.get_connection()
    connection.close()


try:
    create_db_connection_provider()
    test_connection()
except Exception as e:
    print_error("Unable to create database connection provider: " + str(e))
