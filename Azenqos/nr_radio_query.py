import params_disp_df

NR_RADIO_PARAMS_SQL_LIST = [
    '''
    select log_hash, time,
    '--- PCell ---'
    from nr_cell_meas
    ''' ,
    '''
    select nr_dl_frequency_1 as 'NR DL FREQ',
    nr_dl_arfcn_1 as 'NR ARFCN', 
    nr_band_1 as 'NR Band', 
    nr_servingbeam_pci_1 as 'NR PCI', 
    nr_servingbeam_ssb_index_1 as 'NR SSB Index', 
    nr_servingbeam_ss_rsrp_1 as 'NR SS RSRP', 
    nr_servingbeam_ss_rsrq_1 as 'NR SS RSRQ', 
    nr_servingbeam_ss_sinr_1 as 'NR SS SINR', 
    nr_numerology_scs_1 as 'NR SubCarrier Size', 
    nr_num_rx_ant_1 as 'NR N Rx Ant'
    from nr_cell_meas
    ''' ,
    '''
    select nr_cri_1 as 'NR CRI'
    from nr_csi_report
    ''' ,
    '''
    select nr_ri_1 as 'NR RI'
    from nr_deb_stat
    ''' ,
    '''
    select nr_numlayers_1 as 'NR NumLayers'
    from nr_deb_stat
    ''' ,
    '''
    select nr_endc_total_tx_power as 'NR ENDC Total Tx Power',
    nr_pusch_tx_power_1 as 'NR PUSCH Tx Power',
    nr_pucch_tx_power_1 as 'NR PUCCH Tx Power'
    from nr_deb_stat
    ''' ,
    '''
    select nr_srs_tx_power_1 as 'NR SRX Tx Power'
    from nr_tx_srs_status
    ''' ,
    ]

def get_nr_radio_params_disp_df(dbcon, time_before):
    parameter_to_columns_list = [
        (
            [
                "---- PCell ----",
                "NR DL FREQ",
                "NR ARFCN",
            ],
            [
                '"" as unused1',
                "nr_dl_frequency_1",
                "nr_dl_arfcn_1",
            ],
            "nr_cell_meas",
        ),
        (
            [
                "NR Band",
                "NR PCI",
                "NR SSB Index",
            ],
            [
                "nr_band_1",
                "nr_servingbeam_pci_1",
                "nr_servingbeam_ssb_index_1",
            ],
            "nr_cell_meas",
        ),
        (
            [
                "NR SS RSRP",
                "NR SS RSRQ",
                "NR SS SINR",
            ],
            [
                "nr_servingbeam_ss_rsrp_1",
                "nr_servingbeam_ss_rsrq_1",
                "nr_servingbeam_ss_sinr_1",
            ],
            "nr_cell_meas",
        ),
        (
            [
                "NR SubCarrier Size",
            ],
            [
                "nr_numerology_scs_1",
            ],
            "nr_cell_meas",
        ),
        (
            [
                "NR N Rx Ant",
            ],
            [
                "nr_num_rx_ant_1",
            ],
            "nr_cell_meas",
        ),
        (
            [
                "NR CRI",
            ],
            [
                "nr_cri_1",
            ],
            "nr_csi_report",
        ),
        (
            [
                "NR RI",
            ],
            [
                "nr_ri_1",
            ],
            "nr_deb_stat",
        ),
        (
            [
                "NR NumLayers",
            ],
            [
                "nr_numlayers_1",
            ],
            "nr_deb_stat",
        ),
        (
            [
                "NR ENDC Total Tx Power",
                "NR PUSCH Tx Power",
            ],
            [
                "nr_endc_total_tx_power",
                "nr_pusch_tx_power_1",
            ],
            "nr_deb_stat"
        ),
        (
            [
                "NR PUCCH Tx Power",
            ],
            [
                "nr_pucch_tx_power_1",
            ],
            "nr_deb_stat"
        ),
        (
            [
                "NR SRX Tx Power",
            ],
            [
                "nr_srs_tx_power_1",
            ],
            "nr_tx_srs_status"
        ),
    ]
    return params_disp_df.get(
        dbcon,
        parameter_to_columns_list,
        time_before,
        not_null_first_col=True,
        custom_lookback_dur_millis=params_disp_df.DEFAULT_LOOKBACK_DUR_MILLIS,
    )
