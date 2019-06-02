from providers.db_providers import DatabaseConnectionProvider
import sys
import getopt

from repositories import configuration_repository
from utils.program_utils import reset_database

default_database = "db_comparator"
default_host = "localhost"
default_port = 5432
default_username = "postgres"
default_password = "postgres"
table_names = ['relational_point', 'spatial_core_point', 'spatial_postgis_point']
index_names = ['relational_point_index', 'spatial_core_point_index', 'spatial_postgis_point_index']

connection_options = None
db_connection_provider = None
db_state = None


def create_connection_options():
    global connection_options

    optlist, args = getopt.getopt(sys.argv[1:], "db:host:port:user:pass")
    custom_options = dict(optlist)
    connection_options = {
        "db": custom_options["db"] if "db" in custom_options is not None else default_database,
        "host": custom_options["host"] if "host" in custom_options is not None else default_host,
        "port": custom_options["port"] if "port" in custom_options is not None else default_port,
        "user": custom_options["user"] if "user" in custom_options is not None else default_username,
        "pass": custom_options["pass"] if "pass" in custom_options is not None else default_password
    }


def create_db_connection_provider():
    global db_connection_provider

    db_connection_provider = DatabaseConnectionProvider(
        db=connection_options["db"],
        host=connection_options["host"],
        port=int(connection_options["port"]),
        user=connection_options["user"],
        password=connection_options["pass"]
    )


def initialize_database():
    print("Initializing database...")

    try:
        connection = db_connection_provider.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT table_name FROM information_schema.tables
                WHERE table_name IN ({0})
            """.format(str(table_names)[1:-1])
        )
        initialized = cursor.rowcount == len(table_names)
        if not initialized:
            reset_database()

        cursor.close()
    finally:
        connection.close()

    print("Database initialized!")


def get_db_state():
    global db_state

    print("Initializing application...")

    connection = db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT indexname FROM pg_indexes 
                WHERE indexname IN ({0});
            """.format(str(index_names)[1:-1])
        )
        db_state = {
            "has_index": cursor.rowcount == len(index_names),
            "dataset": configuration_repository.get_active_dataset(),
            "dataset_size": configuration_repository.get_active_dataset_size()
        }

        cursor.close()
    finally:
        connection.close()

    print("Application Initialized!")


try:
    create_connection_options()
    create_db_connection_provider()
    initialize_database()
    get_db_state()
except Exception as e:
    sys.exit(str(e))
