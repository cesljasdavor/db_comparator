import psycopg2 as db_client


class DatabaseConnectionProvider(object):
    def __init__(self, db, host, port, user, password):
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
