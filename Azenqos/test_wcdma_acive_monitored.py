import sqlite3

import integration_test_helpers
import wcdma_query


def test():
    azmfp = (
        "../example_logs/wcdma_log/357008080503008-02_09_2020-12_25_26 (wcdma log).azm"
    )
    dbfp = integration_test_helpers.unzip_azm_to_tmp_get_dbfp(azmfp)

    with sqlite3.connect(dbfp) as dbcon:
        df = wcdma_query.get_wcdma_acive_monitored_df(dbcon, "2020-09-02 12:15:29.546")
        print("df.head():\n %s" % df.head(20))
        assert df.iloc[1, 3] == 211
        assert len(df) == 14
        assert len(df.columns) == 7


if __name__ == "__main__":
    test()
