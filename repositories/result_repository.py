import datetime

import providers


def save_result(operation, relational_data, spatial_core_data, spatial_postgis_data, statistics):
    r_has_errors, r_point_count, r_time_elapsed, r_avg_time_per_point = relational_data
    sc_has_errors, sc_point_count, sc_time_elapsed, sc_avg_time_per_point = spatial_core_data
    sp_has_errors, sp_point_count, sp_time_elapsed, sp_avg_time_per_point = spatial_postgis_data
    rsc_ratio, rsp_ratio, spsc_ratio, best = statistics

    connection = providers.db_connection_provider.get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO result (has_index, dataset, dataset_size, operation, relational_point_count, relational_has_errors, relational_time_elapsed, relational_avg_time_per_point, spatial_core_point_count, spatial_core_has_errors, spatial_core_time_elapsed, spatial_core_avg_time_per_point, spatial_postgis_point_count, spatial_postgis_has_errors, spatial_postgis_time_elapsed, spatial_postgis_avg_time_per_point, rsc_ratio, rsp_ratio, spsc_ration, best, created_at)
                VALUES ({}, '{}', {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, '{}', '{}')
            """.format(
                providers.db_state["has_index"],
                providers.db_state["dataset"],
                providers.db_state["dataset_size"],
                operation,
                r_point_count,
                r_has_errors == "Yes",
                r_time_elapsed,
                r_avg_time_per_point,
                sc_point_count,
                sc_has_errors == "Yes",
                sc_time_elapsed,
                sc_avg_time_per_point,
                sp_point_count,
                sp_has_errors == "Yes",
                sp_time_elapsed,
                sp_avg_time_per_point,
                rsc_ratio,
                rsp_ratio,
                spsc_ratio,
                best,
                datetime.datetime.now().isoformat()
            )
        )
        if cursor.rowcount == 0:
            raise Exception("Unable to save result")

        cursor.close()
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
