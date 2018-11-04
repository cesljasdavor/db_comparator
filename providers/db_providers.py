import psycopg2 as db_client


class DatabaseConnectionProvider(object):
    def __init__(self, db="db_comparator", host="localhost", port=5432, user="postgres", password="postgres"):
        """
        Creates a new database connection provider with given params
        :param db: Database to connect to
        :param host:
        :param port:
        :param user:
        :param password:
        """
        self.db = db
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def get_connection(self):
        return db_client.connect(
            database=self.db,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )
