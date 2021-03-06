import contextlib
import os
import sqlite3

import server_overview_widget


def test():
    dbfp = "../example_logs/overview_adbdd4d4-0322-4aa5-a642-5dabe735b898.db"
    if os.path.isfile(dbfp):        
        with contextlib.closing(sqlite3.connect(dbfp)) as dbcon:
            df_dict = server_overview_widget.gen_site_kpi_dfs(dbcon, raise_if_failed=True)
            for key, val in df_dict.items():
                print("df_dict table: {} df:\n{}".format(key, val))
    

if __name__ == "__main__":
    test()
