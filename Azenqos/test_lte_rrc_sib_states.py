import sqlite3

import integration_test_helpers
import lte_query


def test():
    azmfp = "../example_logs/lte_benchmark/357008080503008-26_08_2020-16_18_08.azm"
    dbfp = integration_test_helpers.unzip_azm_to_tmp_get_dbfp(azmfp)

    with sqlite3.connect(dbfp) as dbcon:
        df = lte_query.get_lte_rrc_sib_states_df(dbcon, "2020-08-26 15:45:49.353")
        print("df.head():\n %s" % df.head(20))
        print("len(df)", len(df))
        assert df.iloc[1, 1] == 520
        assert len(df) >= 9
        assert len(df.columns) == 2


if __name__ == "__main__":
    test()
