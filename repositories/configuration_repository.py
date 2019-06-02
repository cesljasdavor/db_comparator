import providers

active_dataset_key = "active_dataset_key"
active_dataset_size_key = "active_dataset_size_key"


def get_active_dataset():
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT value FROM configuration where key = '{0}'
            """.format(active_dataset_key)
        )
        dataset = cursor.fetchone()[0]
        cursor.close()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

    return dataset


def get_active_dataset_size():
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                SELECT value FROM configuration where key = '{0}'
            """.format(active_dataset_size_key)
        )
        dataset_size = int(cursor.fetchone()[0])
        cursor.close()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()

    return dataset_size


def set_active_dataset(dataset):
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO configuration (key, value) VALUES ('{0}', '{1}')
                ON CONFLICT (key)
                DO UPDATE SET value = '{1}'
            """.format(active_dataset_key, dataset)
        )
        cursor.close()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()


def set_active_dataset_size(dataset_size):
    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO configuration (key, value) VALUES ('{0}', '{1}')
                ON CONFLICT (key)
                DO UPDATE SET value = '{1}'
            """.format(active_dataset_size_key, dataset_size)
        )
        cursor.close()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
