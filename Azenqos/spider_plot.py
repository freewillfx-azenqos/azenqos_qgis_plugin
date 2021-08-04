import sys
import traceback

import sqlite3
import pandas as pd

import azq_utils
import azq_cell_file


rat_to_spider_param_dict = dict()
rat_to_spider_param_dict['nr'] = ["nr_servingbeam_pci_1"]
rat_to_spider_param_dict['lte'] = ["lte_physical_cell_id_1", "lte_neigh_physical_cell_id_1",
                                      "lte_neigh_physical_cell_id_2", "lte_neigh_physical_cell_id_3"]
rat_to_spider_param_dict['wcdma'] = ["wcdma_aset_sc_1", "wcdma_aset_sc_2", "wcdma_aset_sc_3"]
rat_to_spider_param_dict['2G'] = ["gsm_arfcn_bcch"]

cellfile_att_param = dict()
cellfile_att_param['nr'] = 'pci'
cellfile_att_param['lte'] = 'pci'
cellfile_att_param['wcdma'] = 'psc'
cellfile_att_param['gsm'] = 'bcch'


def plot_rat_spider(cell_files, dbfp, rat, single_point_layer_time=None, plot_spider_param=None):
    print("plot_spider_param - START")
    try:
        from qgis._core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsProject

        if plot_spider_param is None:
            plot_spider_param = rat_to_spider_param_dict[rat][0]
        new_layer_name = get_spider_or_line_to_site_layer_name(rat, plot_spider_param, single_point_layer_time)

        # remove currently selected layer first, in case we dont have a match when we do single point plot so prev layer must be removed first
        cur_layers_dict = azq_utils.get_qgis_layers_dict()
        if new_layer_name in cur_layers_dict:
            print("remove existing layername pre add: " + new_layer_name)
            old_layer = cur_layers_dict[new_layer_name]
            QgsProject.instance().removeMapLayer(old_layer)

        wkt_multiline_string = gen_wkt_lines_plot_rat_spider(cell_files, dbfp, rat, plot_spider_param, single_point_layer_time=single_point_layer_time)
        print("single_point_layer_time: {} wkt_multiline_string: {}".format(single_point_layer_time, wkt_multiline_string))

        new_layer = QgsVectorLayer('LineString?crs=epsg:4326', new_layer_name, 'memory')
        prov = new_layer.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromWkt(wkt_multiline_string))
        prov.addFeatures([feat])
        new_layer.updateExtents()
        print("new_layer_name:", new_layer_name)
        cur_layers_dict = azq_utils.get_qgis_layers_dict()
        if new_layer_name in cur_layers_dict:
            print("remove existing layername pre add: " + new_layer_name)
            old_layer = cur_layers_dict[new_layer_name]
            QgsProject.instance().removeMapLayer(old_layer)
        QgsProject.instance().addMapLayer(new_layer)
        print("plot_spider_param - addMapLayers success")
    except:
        type_, value_, traceback_ = sys.exc_info()
        exstr = str(traceback.format_exception(type_, value_, traceback_))
        print("WARNING: plot_rat_spider rat {} exception: {}".format(rat, exstr))
    print("plot_spider_param - DONE")


def gen_wkt_multiline_string(wkt_lines):
    assert wkt_lines is not None
    assert len(wkt_lines)
    wkt_str = ",".join(wkt_lines)
    wkt_str = "MULTILINESTRING({})".format(wkt_str)
    return wkt_str


def get_spider_or_line_to_site_layer_name(rat, plot_spider_param, single_point_layer_time=None):
    name_suffix = rat.upper() + "_" + plot_spider_param
    spider_layer_name = get_spider_layer_name(name_suffix)
    if single_point_layer_time is not None:
        spider_layer_name = get_line_to_site_layer_name(name_suffix)
    return spider_layer_name


def gen_wkt_lines_plot_rat_spider(cell_files, dbfp, rat, plot_spider_param, single_point_layer_time=None):
    assert cell_files is not None
    assert cell_files
    print("rat {} handle plot_spider_param: {}".format(rat, plot_spider_param))
    wkt_lines = gen_spider_wkt_lines(cell_files, dbfp, rat, plot_spider_param, single_point_layer_time)
    assert wkt_lines is not None
    assert len(wkt_lines)
    wkt_multiline_string = gen_wkt_multiline_string(wkt_lines)
    assert wkt_multiline_string.startswith("MULTILINESTRING((")
    return wkt_multiline_string


def gen_spider_wkt_lines(cell_files, dbfp, rat, plot_spider_param, single_point_layer_time):
    df = gen_spider_df(cell_files, dbfp, rat, plot_spider_param, single_point_layer_time)
    df = df.dropna(subset=["param_lat", "param_lon", "cell_lat", "cell_lon"])
    wkt_sr = "(" + df.param_lon.astype(str) + " " + df.param_lat.astype(str) + "," + df.cell_lon.astype(str) + " " + df.cell_lat.astype(str) + " )"
    return wkt_sr


def gen_spider_df(cell_files, dbfp, rat, plot_spider_param, single_point_layer_time, sector_distance=0.0007):
    cells_df = azq_cell_file.read_cellfiles(cell_files, rat=rat, add_cell_lat_lon_sector_distance=sector_distance)
    if len(cells_df) == 0:
        raise Exception("len(cells_df) == 0")
    with sqlite3.connect(dbfp) as dbcon:
        cgi_df = None
        param_df = None
        cgi_df, param_df = get_cgi_df_and_param_df(dbcon, rat, plot_spider_param, single_point_layer_time=single_point_layer_time)
        assert cgi_df is not None
        assert param_df is not None
        assert len(cgi_df)
        assert len(param_df)

        df = cgi_df
        df['time'] = pd.to_datetime(df['time'])
        df = df[['log_hash', 'time', 'cgi']]
        df = df.set_index('time', drop=True)
        df = df.groupby('log_hash').resample('1000ms').ffill()
        df = df[['cgi']]
        df = df.reset_index()
        df = df[df.log_hash.notnull()]
        df['log_hash'] = df.log_hash.astype(int)

        param_df['time'] = pd.to_datetime(param_df['time'])
        param_df['log_hash'] = param_df.log_hash.astype(int)

        location_sql = "select log_hash, time, positioning_lat as param_lat, positioning_lon as param_lon from location order by time"
        location_df = pd.read_sql_query(location_sql, dbcon)
        location_df['time'] = pd.to_datetime(location_df['time'])
        location_df['log_hash'] = location_df.log_hash.astype(int)

        df = pd.merge_asof(param_df, df, on='time', by='log_hash', direction='nearest',
                           tolerance=pd.Timedelta('1000ms'))
        df = pd.merge_asof(df, location_df, on='time', by='log_hash', direction='nearest',
                           tolerance=pd.Timedelta('2000ms'))
        df = df[(df.param_lat.notnull()) & (df.param_lon.notnull())]
        df = df[df.cgi.notnull()]
        df = df.drop_duplicates(["param_lat", "param_lon"])
        print("df matched cgi len:", len(df))
        print("start gen wkt_line_list df.head()", df[["param_lat", "param_lon", "cgi"]].head(), "\ncells_df.head()", cells_df.head())
        cells_df = cells_df[["cgi", "cell_lat", "cell_lon"]].copy()
        merged_df = df.merge(cells_df, on="cgi", how="left")
        merged_df = merged_df[["param_lat", "cell_lat", "param_lon", "cell_lon"]]
        print("merged_df head:", merged_df.head(10))
        return merged_df

    raise Exception("invalid state")


def get_spider_layer_name(rat):
    return "Spider_"+rat


def get_line_to_site_layer_name(rat):
    return "Line_to_site_"+rat


def get_cgi_df_and_param_df(dbcon, rat, plot_spider_param, single_point_layer_time=None):
    cgi_df = None
    param_df = None

    if rat == "lte":
        sqlstr = "select log_hash, time, lte_sib1_mcc as mcc, lte_sib1_mnc as mnc, lte_sib1_tac as lac, lte_sib1_eci as cell_id from lte_sib1_info order by time"
        df = pd.read_sql_query(sqlstr, dbcon)
        df["cgi"] = df.mcc.astype(int).astype(str) + " " + df.mnc.astype(int).astype(
            str) + " " + df.lac.astype(int).astype(str) + " " + df.cell_id.astype(int).astype(str)
        cgi_df = df

        if single_point_layer_time is not None:
            param_sql = "select log_hash, time, {} from lte_cell_meas where time = '{}' order by time".format(
                plot_spider_param,
                single_point_layer_time)
        else:
            param_sql = "select log_hash, time, {} from lte_cell_meas order by time".format(plot_spider_param)
        print("lte param_sql:", param_sql)
        param_df = pd.read_sql_query(param_sql, dbcon)
        print("lte param df len:", len(param_df))
    elif rat == "wcdma":
        asql = "select log_hash, time, mm_characteristics_mcc as mcc, mm_characteristics_mnc as mnc, mm_characteristics_lac as lac from mm_state where mm_characteristics_mcc is not null and mm_characteristics_mnc is not null and mm_characteristics_lac is not null order by time"
        bsql = "select log_hash, time, wcdma_cellid as cell_id from wcdma_idle_cell_info where wcdma_cellid is not null"

        df_a = pd.read_sql_query(asql, dbcon)
        df_b = pd.read_sql_query(bsql, dbcon)

        df_a['time'] = pd.to_datetime(df_a['time'])
        df_a['log_hash'] = df_a.log_hash.astype(int)
        df_b['time'] = pd.to_datetime(df_b['time'])
        df_b['log_hash'] = df_b.log_hash.astype(int)
        df = pd.merge_asof(df_a, df_b, on='time', by='log_hash', direction='nearest',
                           tolerance=pd.Timedelta('3600000ms'))

        df["cgi"] = df.mcc.astype(int).astype(str) + " " + df.mnc.astype(int).astype(
            str) + " " + df.lac.astype(int).astype(str) + " " + df.cell_id.astype(int).astype(str)
        cgi_df = df
        param_sql = "select log_hash, time, wcdma_aset_sc_1 from wcdma_cell_meas order by time"
        param_df = pd.read_sql_query(param_sql, dbcon)

    elif rat == "gsm":
        sqlstr = "select log_hash, time, gsm_cgi as cgi, gsm_arfcn_bcch from gsm_cell_meas order by time"
        df = pd.read_sql_query(sqlstr, dbcon)
        cgi_df = df
        param_df = df[['log_hash', 'time', 'gsm_arfcn_bcch']]
    else:
        raise Exception("unhandled rat: {}".format(rat))

    assert cgi_df is not None
    assert param_df is not None
    return cgi_df, param_df