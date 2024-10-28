#! /home/jwzheng/anaconda3/envs/cygnss/bin/python

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy.ma as npma
import numpy as np
import scipy.interpolate as interp
import glob
import os

import time_lib as tlib
import ncfile_lib as nclib

def cygnss_download_L1(cygnss_dir,year_st,month_st,day_st,year_ed,month_ed,day_ed):
    year_st_str='{:04d}'.format(year_st)
    month_st_str='{:02}'.format(month_st)
    day_st_str='{:02}'.format(day_st)
    year_ed_str='{:04d}'.format(year_ed)
    month_ed_str='{:02}'.format(month_ed)
    day_ed_str='{:02}'.format(day_ed)
    podaac_cmdstr='podaac-data-downloader -c CYGNSS_L1_V3.1 -d '+cygnss_dir
    podaac_cmdstr+=' --start-date '+year_st_str+'-'+month_st_str+'-'+day_st_str+'T00:00:00Z'
    podaac_cmdstr+=' --end-date '+year_ed_str+'-'+month_ed_str+'-'+day_ed_str+'T00:00:00Z'
    podaac_cmdstr+=' -e ""'
    print(podaac_cmdstr)
    os.system(podaac_cmdstr)
    md5files=glob.glob(cygnss_dir+'*.md5')
    [os.remove(md5file) for md5file in md5files]
    txtfiles=glob.glob(cygnss_dir+'*.txt')
    [os.remove(txtfile) for txtfile in txtfiles]
    
def cygnss_showattr():
    attr=('time_coverage_start','time_coverage_end','time_coverage_duration', \
        'time_coverage_resolution')
    print(attr)

def cygnss_showvars():
    vars=('spacecraft_num','ddm_timestamp_utc', \
        'ddm_timestamp_gps_week','ddm_timestamp_gps_sec', \
        'nst_att_status','prn_code','track_id','ddm_ant', \
        'sp_lat','sp_lon','sp_alt','sp_inc_angle','sp_rx_gain', \
        'gps_eirp','ddm_snr','rx_to_sp_range','tx_to_sp_range', \
        'ddm_nbrcs','ddm_les','ddm_brcs_uncert','quality_flags', \
        'raw_counts','power_analog','brcs','eff_scatter','fresnel_coeff', \
        'brcs_ddm_sp_bin_delay_row','brcs_ddm_sp_bin_dopp_col', \
        'delay_resolution','dopp_resolution')
    print(vars)

def cygnss_get_time_utc_mjdsod(attr_list,global_attr,var_list,var_data_list):
    t_st=global_attr[attr_list.index('time_coverage_start')]
    t_st_mjd=tlib.ymd2mjd(int(t_st[0:4]),int(t_st[5:7]),int(t_st[8:10]))
    t_st_sod=tlib.hms2sod(int(t_st[11:13]),int(t_st[14:16]),float(t_st[17:-1]))
    ddm_timestamp_utc=nclib.nc_get_varsValue('ddm_timestamp_utc',var_list,var_data_list)
    if(ddm_timestamp_utc[2]==0): t_utc_sod=ddm_timestamp_utc[0]+t_st_sod
    else: print("ERROR???????????????????")
    return t_st_mjd,t_utc_sod
    
def cygnss_calRCG(sp_rx_gain,rx_to_sp_range,tx_to_sp_range):
    """
    calculate Range Corrected Gain(RCG)
    """
    sp_rx_gain=sp_rx_gain.astype(dtype='float64')
    tx_to_sp_range=tx_to_sp_range.astype(dtype='int64')
    rx_to_sp_range=rx_to_sp_range.astype(dtype='int64')
    rcg=sp_rx_gain*1e+027/rx_to_sp_range**2/tx_to_sp_range**2
    return rcg
    
def cygnss_num2str(sc_num):
    return 'cygnss'+'{:02d}'.format(sc_num)

def cygnss_quality_control(df,t_utc_mjd,t_utc_sod,var_list,var_data_list,u10v10,shts):
    sp_lat=nclib.nc_get_varsValue('sp_lat',var_list,var_data_list)
    sp_lon=nclib.nc_get_varsValue('sp_lon',var_list,var_data_list)
    ddm_nbrcs=nclib.nc_get_varsValue('ddm_nbrcs',var_list,var_data_list)
    ddm_les=nclib.nc_get_varsValue('ddm_les',var_list,var_data_list)
    sp_rx_gain=nclib.nc_get_varsValue('sp_rx_gain',var_list,var_data_list)
    rx_to_sp_range=nclib.nc_get_varsValue('rx_to_sp_range',var_list,var_data_list)
    tx_to_sp_range=nclib.nc_get_varsValue('tx_to_sp_range',var_list,var_data_list)
    quality_flags=nclib.nc_get_varsValue('quality_flags',var_list,var_data_list)
    nst_att_status=nclib.nc_get_varsValue('nst_att_status',var_list,var_data_list)
    sp_inc_angle=nclib.nc_get_varsValue('sp_inc_angle',var_list,var_data_list)
    rcg=cygnss_calRCG(sp_rx_gain[0],rx_to_sp_range[0],tx_to_sp_range[0])
    epochs=len(t_utc_sod)
    for epoch in np.arange(0,10000,1):
        print('{:08d}'.format(epoch)+'/'+'{:d}'.format(epochs))
        if(nclib.nc_varsValue_isnoteffective(nst_att_status[0][epoch],nst_att_status[1],nst_att_status[2])): continue 
        if(nst_att_status[0][epoch]!=0): continue
        for channel in np.arange(0,4,1):
            if(nclib.nc_varsValue_isnoteffective(sp_lat[0][epoch,channel],sp_lat[1],sp_lat[2])): continue 
            if(nclib.nc_varsValue_isnoteffective(sp_lon[0][epoch,channel],sp_lon[1],sp_lon[2])): continue
            if(nclib.nc_varsValue_isnoteffective(sp_inc_angle[0][epoch,channel],sp_inc_angle[1],sp_inc_angle[2])): continue
            if(nclib.nc_varsValue_isnoteffective(ddm_nbrcs[0][epoch,channel],ddm_nbrcs[1],ddm_nbrcs[2])): continue
            if(nclib.nc_varsValue_isnoteffective(ddm_les[0][epoch,channel],ddm_les[1],ddm_les[2])): continue
            if(nclib.nc_varsValue_isnoteffective(sp_rx_gain[0][epoch,channel],sp_rx_gain[1],sp_rx_gain[2])): continue
            if(nclib.nc_varsValue_isnoteffective(rx_to_sp_range[0][epoch,channel],rx_to_sp_range[1],rx_to_sp_range[2])): continue
            if(nclib.nc_varsValue_isnoteffective(tx_to_sp_range[0][epoch,channel],tx_to_sp_range[1],tx_to_sp_range[2])): continue
            if(nclib.nc_varsValue_isnoteffective(quality_flags[0][epoch,channel],quality_flags[1],quality_flags[2])): continue
            if(quality_flags[0][epoch,channel]!=0): continue
            if(rcg[epoch,channel]<3): continue
            sp_u10,sp_v10,sp_shts=cygnss_Spatiotemporal_matching(t_utc_sod[epoch],sp_lat[0][epoch,channel],sp_lon[0][epoch,channel],u10v10,shts)
            if(np.isnan(sp_u10)): continue
            if(np.isnan(sp_v10)): continue
            if(np.isnan(sp_shts)): continue
            df.loc[len(df.index)]=[t_utc_mjd,t_utc_sod[epoch], \
                sp_lat[0][epoch,channel],sp_lon[0][epoch,channel], \
                sp_inc_angle[0][epoch,channel],
                ddm_les[0][epoch,channel],ddm_nbrcs[0][epoch,channel], \
                sp_u10,sp_v10,sp_shts]
            
def cygnss_Spatiotemporal_matching(sp_sod,sp_lat,sp_lon,u10v10,shts):
    # u10
    lon=u10v10[0][0]
    lat=u10v10[1][0]
    t_hour=u10v10[2][0]-u10v10[2][0][0]
    t_sod=tlib.hms2sod(t_hour,0,0)
    index_lon=np.argsort(np.abs(lon-sp_lon))[0:2]
    index_lat=np.argsort(np.abs(lat-sp_lat))[0:2]
    index_t=np.argsort(np.abs(t_sod-sp_sod))[0:2]    
    lon_use=[lon[index_lon[0]],lon[index_lon[1]]]
    lat_use=[lat[index_lat[0]],lat[index_lat[1]]]
    t_use=[t_sod[index_t[0]],t_sod[index_t[1]]]
    u10_use_01=[[u10v10[3][0][index_t[0],index_lat[0],index_lon[0]],u10v10[3][0][index_t[0],index_lat[0],index_lon[1]]],
                [u10v10[3][0][index_t[0],index_lat[1],index_lon[0]],u10v10[3][0][index_t[0],index_lat[1],index_lon[1]]]]
    fillvalue=u10v10[3][1]
    sp_u10=np.nan
    if(u10_use_01[0][0]!=fillvalue and u10_use_01[0][1]!=fillvalue \
        and u10_use_01[1][0]!=fillvalue and u10_use_01[1][1]!=fillvalue):
        inter=interp.interp2d(lon_use,lat_use,u10_use_01,kind='linear')
        u10_01=inter(sp_lon,sp_lat)
        u10_use_02=[[u10v10[3][0][index_t[1],index_lat[0],index_lon[0]],u10v10[3][0][index_t[1],index_lat[0],index_lon[1]]],
                    [u10v10[3][0][index_t[1],index_lat[1],index_lon[0]],u10v10[3][0][index_t[1],index_lat[1],index_lon[1]]]]
        if(u10_use_02[0][0]!=fillvalue and u10_use_02[0][1]!=fillvalue \
            and u10_use_02[1][0]!=fillvalue and u10_use_02[1][1]!=fillvalue):
            inter=interp.interp2d(lon_use,lat_use,u10_use_02,kind='linear')
            u10_02=inter(sp_lon,sp_lat)
            sp_u10=np.interp(sp_sod,t_use,list(u10_01)+list(u10_02)) 
    # v10      
    v10_use_01=[[u10v10[4][0][index_t[0],index_lat[0],index_lon[0]],u10v10[4][0][index_t[0],index_lat[0],index_lon[1]]],
                [u10v10[4][0][index_t[0],index_lat[1],index_lon[0]],u10v10[4][0][index_t[0],index_lat[1],index_lon[1]]]]
    fillvalue=u10v10[4][1]
    sp_v10=np.nan
    if(v10_use_01[0][0]!=fillvalue and v10_use_01[0][1]!=fillvalue \
        and v10_use_01[1][0]!=fillvalue and v10_use_01[1][1]!=fillvalue):
        inter=interp.interp2d(lon_use,lat_use,v10_use_01,kind='linear')
        v10_01=inter(sp_lon,sp_lat)
        v10_use_02=[[u10v10[4][0][index_t[1],index_lat[0],index_lon[0]],u10v10[4][0][index_t[1],index_lat[0],index_lon[1]]],
                    [u10v10[4][0][index_t[1],index_lat[1],index_lon[0]],u10v10[4][0][index_t[1],index_lat[1],index_lon[1]]]]
        if(v10_use_02[0][0]!=fillvalue and v10_use_02[0][1]!=fillvalue \
            and v10_use_02[1][0]!=fillvalue and v10_use_02[1][1]!=fillvalue):
            inter=interp.interp2d(lon_use,lat_use,v10_use_02,kind='linear')
            v10_02=inter(sp_lon,sp_lat)
            sp_v10=np.interp(sp_sod,t_use,list(v10_01)+list(v10_02)) 
    # shts
    lon=shts[0][0]
    lat=shts[1][0]
    t_hour=shts[2][0]-shts[2][0][0]
    t_sod=tlib.hms2sod(t_hour,0,0)
    index_lon=np.argsort(np.abs(lon-sp_lon))[0:2]
    index_lat=np.argsort(np.abs(lat-sp_lat))[0:2]
    index_t=np.argsort(np.abs(t_sod-sp_sod))[0:2]    
    lon_use=[lon[index_lon[0]],lon[index_lon[1]]]
    lat_use=[lat[index_lat[0]],lat[index_lat[1]]]
    t_use=[t_sod[index_t[0]],t_sod[index_t[1]]]
    shts_use_01=[[shts[3][0][index_t[0],index_lat[0],index_lon[0]],shts[3][0][index_t[0],index_lat[0],index_lon[1]]],
                [shts[3][0][index_t[0],index_lat[1],index_lon[0]],shts[3][0][index_t[0],index_lat[1],index_lon[1]]]]
    fillvalue=shts[3][1]
    sp_shts=np.nan
    if(shts_use_01[0][0]!=fillvalue and shts_use_01[0][1]!=fillvalue \
        and shts_use_01[1][0]!=fillvalue and shts_use_01[1][1]!=fillvalue):
        inter=interp.interp2d(lon_use,lat_use,shts_use_01,kind='linear')
        shts_01=inter(sp_lon,sp_lat)
        shts_use_02=[[shts[3][0][index_t[1],index_lat[0],index_lon[0]],shts[3][0][index_t[1],index_lat[0],index_lon[1]]],
                    [shts[3][0][index_t[1],index_lat[1],index_lon[0]],shts[3][0][index_t[1],index_lat[1],index_lon[1]]]]
        if(shts_use_02[0][0]!=fillvalue and shts_use_02[0][1]!=fillvalue \
            and shts_use_02[1][0]!=fillvalue and shts_use_02[1][1]!=fillvalue):
            inter=interp.interp2d(lon_use,lat_use,shts_use_02,kind='linear')
            shts_02=inter(sp_lon,sp_lat)
            sp_shts=np.interp(sp_sod,t_use,list(shts_01)+list(shts_02)) 
    return [sp_u10,sp_v10,sp_shts]


def cygnss_fig_sp_distribution(figsdir,sc_num,sp_lat,sp_lon):
    sp_lon[sp_lon>180]=sp_lon[sp_lon>180]-360 # 0~360 to -180~180
    plt.figure(figsize=(12,9))
    plt.rc('font',family='Times New Roman') 
    mymap=Basemap(projection='cyl', \
                llcrnrlat=-60,urcrnrlat=60,llcrnrlon=-180,urcrnrlon=180, \
                resolution='i',area_thresh=5000.0)
    mymap.drawcoastlines(color='k',linewidth=0.1)
    mymap.drawcountries(color='k',linewidth=0.05)
    mymap.fillcontinents(color='white',lake_color='lightskyblue')
    mymap.drawmapboundary(fill_color='skyblue')
    mymap.scatter(sp_lon,sp_lat,marker='o',s=2,color='none',linewidth=0.1,edgecolors='r',alpha=0.05) 
    mymap.drawmeridians(np.arange(0,360,60),labels=[1,0,0,1],fontsize=11) # left,right,up,down
    mymap.drawparallels(np.arange(-90,90.001,30),labels=[1,0,0,1],fontsize=11) # left,right,up,down
    sc_str=cygnss_num2str(sc_num)
    plt.title('sp_distribution_'+sc_str)
    plt.savefig(figsdir+'sp_distribution_'+sc_str+'.png',dpi=1080,bbox_inches='tight')
    plt.close('all') 
    print(figsdir+'sp_distribution_'+sc_str+'.png')

def cygnss_get_ddmbin_delays_and_dopps(brcs_ddm_sp_bin_delay_row,brcs_ddm_sp_bin_dopp_col,delay_resolution,dopp_resolution):
    sp_delay_row=np.around(brcs_ddm_sp_bin_delay_row)
    rows=np.arange(0,17,1)
    ddmbin_delays=['{:.2f}'.format((row-sp_delay_row)*delay_resolution) for row in rows]
    sp_dopp_col=np.around(brcs_ddm_sp_bin_dopp_col)
    cols=np.arange(0,11,1)
    ddmbin_dopps=['{:.1f}'.format((col-sp_dopp_col)*dopp_resolution/1000) for col in cols]
    return ddmbin_delays,ddmbin_dopps

def cygnss_fig_ddm_brcs(figsdir,ddm_brcs,brcs_ddm_sp_bin_delay_row,brcs_ddm_sp_bin_dopp_col,delay_resolution,dopp_resolution):
    font_dict=dict(fontsize=12,color='k',family='Times New Roman',weight='light',style='italic')
    fig,ax=plt.subplots(figsize=(6,7)) 
    plt.rc('font',family='Times New Roman') 
    ddmbin_delays,ddmbin_dopps=cygnss_get_ddmbin_delays_and_dopps(brcs_ddm_sp_bin_delay_row,brcs_ddm_sp_bin_dopp_col,delay_resolution,dopp_resolution)
    ax.set_yticks(np.arange(17))
    ax.set_xticks(np.arange(11))
    ax.set_yticklabels(ddmbin_delays,fontdict=font_dict)
    ax.set_xticklabels(ddmbin_dopps,fontdict=font_dict)
    plt.ylabel('Delay (chips)',fontdict=font_dict)
    plt.xlabel('Doppler (kHz)',fontdict=font_dict)
    plt.imshow(ddm_brcs,cmap='jet',origin='upper',aspect="auto")
    cbar=plt.colorbar(label='BRCS')
    plt.clim(vmin=0)
    plt.savefig(figsdir+'ddm_brcs.png',dpi=1080,bbox_inches='tight')
    plt.close('all') 

if __name__=='__main__':
    os.system('clear')
    cygnss_dir='./cygnss/'
    years=np.arange(2019,2020,1)
    months=np.arange(8,9,1)
    for year_st in years:
        for month_st in months:
            dom=tlib.get_dom(year_st,month_st)
            days=np.arange(1,dom+1,1)
            for day_st in days:
                year_ed,month_ed,day_ed=tlib.ymd_plus_oneday(year_st,month_st,day_st)
                cygnss_download_L1(cygnss_dir,year_st,month_st,day_st,year_ed,month_ed,day_ed)
