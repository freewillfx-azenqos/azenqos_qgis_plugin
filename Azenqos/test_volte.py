import sqlite3
import contextlib
import integration_test_helpers
import lte_query


def test():
    azmfp = "../example_logs/lte_benchmark/357008080503008-26_08_2020-16_18_08.azm"
    dbfp = integration_test_helpers.unzip_azm_to_tmp_get_dbfp(azmfp)

    with contextlib.closing(sqlite3.connect(dbfp)) as dbcon:
        df = lte_query.get_volte_disp_df(dbcon, "2020-08-26 15:53:44.237")
        print("df.head():\n %s" % df.head(20))
        assert df.iloc[8, 1] == 39
        assert len(df) == 18
        assert len(df.columns) == 2


if __name__ == "__main__":
    test()
