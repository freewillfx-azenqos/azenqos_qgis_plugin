import sqlite3
import contextlib
import integration_test_helpers
import lte_query


def test():
    azmfp = "../example_logs/lte_benchmark/357008080503008-26_08_2020-16_18_08.azm"
    dbfp = integration_test_helpers.unzip_azm_to_tmp_get_dbfp(azmfp)

    with contextlib.closing(sqlite3.connect(dbfp)) as dbcon:
        df = lte_query.get_lte_data_disp_df(dbcon, "2020-08-26 15:42:26.226")
        print(df)
        assert df.iloc[1, 1] == "DL"
        assert len(df) == 46
        assert len(df.columns) == 5


if __name__ == "__main__":
    test()
