#! ~/anaconda3/envs/cygnss/bin/python

''' 
Auth: Jiawei Zheng, GNSS Research Center, Wuhan University
Cont: jwzheng@whu.edu.cn
Github: https://github.com/jwzhengWHU
Profile: http://panda.whu.edu.cn/info/1329/1401.htm
ResearchGate: https://www.researchgate.net/profile/Jiawei-Zheng-4
GoogleScholar: https://scholar.google.com.hk/citations?user=0Te3Ps0AAAAJ&hl=zh-CN
'''

import matplotlib.pyplot as plt
import os
import glob
import numpy as np
import pandas as pd

import cygnss_lib as cylib
import era5_lib as erlib
import ncfile_lib as nclib

figsdir='./'
cygnss_filedir='./cygnss/'
era5_filedir='./ERA5/'
year_st,month_st,day_st=2019,7,1
year_ed,month_ed,day_ed=2019,7,2

os.system('clear')
# cylib.cygnss_download_L1(cygnss_filedir,year_st,month_st,day_st,year_ed,month_ed,day_ed)
cygnss_ncfiles=glob.glob('./cygnss/*.nc')
era5_ncfiles=glob.glob('./ERA5/era5_reanalysis_shts_????????.nc')
cygnss_vars=('spacecraft_num','ddm_timestamp_utc','sp_lat','sp_lon', \
            'brcs','sp_inc_angle','ddm_nbrcs','ddm_les','nst_att_status','sp_rx_gain','rx_to_sp_range','tx_to_sp_range','quality_flags')

for cygnss_ncfile in cygnss_ncfiles:
    attr_list,global_attr,var_list,var_attr_list,var_data_list=nclib.read_ncfile(cygnss_ncfile,cygnss_vars)
    t_utc_mjd,t_utc_sod=cylib.cygnss_get_time_utc_mjdsod(attr_list,global_attr,var_list,var_data_list)
    u10v10,shts=erlib.era5_get_u10v10shts(t_utc_mjd,era5_filedir)
    df=pd.DataFrame(columns=['t_utc_mjd','t_utc_sod','sp_lat','sp_lon', \
    'sp_inc_angle','ddm_les','ddm_nbrcs','u10','v10','shts'])
    cylib.cygnss_quality_control(df,t_utc_mjd,t_utc_sod,var_list,var_data_list,u10v10,shts)
    spacecraft_num=nclib.nc_get_varsValue('spacecraft_num',var_list,var_data_list)
    df.to_csv(path_or_buf='./cygnss_csv/'+cylib.cygnss_num2str(spacecraft_num[0])+'_'+'{:5d}'.format(t_utc_mjd)+'.csv',sep=',')
    # ddm_brcs_uncert=var_data_list[var_list.index('ddm_brcs_uncert')]
    # quality_flags=var_data_list[var_list.index('quality_flags')]
    # raw_counts=var_data_list[var_list.index('raw_counts')]
    # power_analog=var_data_list[var_list.index('power_analog')]
    # brcs=var_data_list[var_list.index('brcs')]
    # eff_scatter=var_data_list[var_list.index('eff_scatter')]
    # fresnel_coeff=var_data_list[var_list.index('fresnel_coeff')]
    # brcs_ddm_sp_bin_delay_row=var_data_list[var_list.index('brcs_ddm_sp_bin_delay_row')]
    # brcs_ddm_sp_bin_dopp_col=var_data_list[var_list.index('brcs_ddm_sp_bin_dopp_col')]
    # delay_resolution=var_data_list[var_list.index('delay_resolution')]
    # dopp_resolution=var_data_list[var_list.index('dopp_resolution')]
    
    # cylib.cygnss_fig_ddm_brcs(figsdir,brcs[0,1],brcs_ddm_sp_bin_delay_row[0,1],brcs_ddm_sp_bin_dopp_col[0,1],delay_resolution,dopp_resolution)
#     sp_lat=var_data_list[vars.index('sp_lat')]
#     sp_lon=var_data_list[vars.index('sp_lon')]
#     sc_num=var_data_list[vars.index('spacecraft_num')]
#     sp_lat_save=ma.concatenate([sp_lat_save,sp_lat],axis=0)
#     sp_lon_save=ma.concatenate([sp_lon_save,sp_lon],axis=0)
#     cylib.cygnss_fig_sp_distribution(figsdir,sc_num,sp_lat,sp_lon)
# cylib.cygnss_fig_sp_distribution(figsdir,0,sp_lat_save[1:,:],sp_lon_save[1:,:])
    
    
    
    
         
