#! ~/anaconda3/envs/cygnss/bin/python

import numpy as np
import os

import ncfile_lib as nclib
import download_ERA5
import time_lib as tlib

def era5_showvars():
    vars=('longitude','latitude','time','u10','v10','shts')
    print(vars)
        
def era5_get_u10v10shts(mjd,era5_filedir):
    mjd1=mjd
    mjd2=mjd+1
    year1,month1,day1=tlib.mjd2ymd(mjd1)
    year1_str='{:04d}'.format(year1)
    month1_str='{:02d}'.format(month1)
    day1_str='{:02d}'.format(int(day1))
    year2,month2,day2=tlib.mjd2ymd(mjd2)
    year2_str='{:04d}'.format(year2)
    month2_str='{:02d}'.format(month2)
    day2_str='{:02d}'.format(int(day2))
    era5_u10v10_filename1='era5_reanalysis_u10_v10_'+year1_str+month1_str+day1_str+'.nc'
    era5_u10v10_filename2='era5_reanalysis_u10_v10_'+year2_str+month2_str+day2_str+'.nc'
    era5_shts_filename1='era5_reanalysis_shts_'+year1_str+month1_str+day1_str+'.nc'
    era5_shts_filename2='era5_reanalysis_shts_'+year2_str+month2_str+day2_str+'.nc'
    if(os.path.isfile(era5_filedir+era5_u10v10_filename1)==False): 
        download_ERA5.download_ECMWF_ERA5(year1_str,month1_str,day1_str, \
            ['10m_u_component_of_wind','10m_v_component_of_wind'], \
            era5_filedir+'era5_reanalysis_u10_v10_')
    if(os.path.isfile(era5_filedir+era5_u10v10_filename2)==False): 
        download_ERA5.download_ECMWF_ERA5(year2_str,month2_str,day2_str, \
            ['10m_u_component_of_wind','10m_v_component_of_wind'], \
            era5_filedir+'era5_reanalysis_u10_v10_')
    if(os.path.isfile(era5_filedir+era5_shts_filename1)==False): 
        download_ERA5.download_ECMWF_ERA5(year1_str,month1_str,day1_str, \
            ['significant_height_of_total_swell'], \
            era5_filedir+'era5_reanalysis_shts_')
    if(os.path.isfile(era5_filedir+era5_shts_filename2)==False): 
        download_ERA5.download_ECMWF_ERA5(year2_str,month2_str,day2_str, \
            ['significant_height_of_total_swell'], \
            era5_filedir+'era5_reanalysis_shts_')
    attr_list,global_attr,var_list,var_attr_list,var_data_list=nclib.read_ncfile(era5_filedir+era5_u10v10_filename1,('longitude','latitude','time','u10','v10'))
    u10v10_lon_1=nclib.nc_get_varsValue('longitude',var_list,var_data_list)
    u10v10_lat_1=nclib.nc_get_varsValue('latitude',var_list,var_data_list)
    u10v10_time_1=nclib.nc_get_varsValue('time',var_list,var_data_list)
    u10v10_u10_1=nclib.nc_get_varsValue('u10',var_list,var_data_list)
    u10v10_v10_1=nclib.nc_get_varsValue('v10',var_list,var_data_list)
    attr_list,global_attr,var_list,var_attr_list,var_data_list=nclib.read_ncfile(era5_filedir+era5_u10v10_filename2,('longitude','latitude','time','u10','v10'))
    u10v10_lon_2=nclib.nc_get_varsValue('longitude',var_list,var_data_list)
    u10v10_lat_2=nclib.nc_get_varsValue('latitude',var_list,var_data_list)
    u10v10_time_2=nclib.nc_get_varsValue('time',var_list,var_data_list)
    u10v10_u10_2=nclib.nc_get_varsValue('u10',var_list,var_data_list)
    u10v10_v10_2=nclib.nc_get_varsValue('v10',var_list,var_data_list)
    np.append(u10v10_time_1[0],u10v10_time_2[0][0])
    np.append(u10v10_u10_1[0],u10v10_u10_2[0][0])
    u10v10_u10_1[2]=u10v10_u10_1[2]+u10v10_u10_2[2]
    np.append(u10v10_v10_1[0],u10v10_v10_2[0][0])
    u10v10_v10_1[2]=u10v10_v10_1[2]+u10v10_v10_2[2]
    attr_list,global_attr,var_list,var_attr_list,var_data_list=nclib.read_ncfile(era5_filedir+era5_shts_filename1,('longitude','latitude','time','shts'))
    shts_lon_1=nclib.nc_get_varsValue('longitude',var_list,var_data_list)
    shts_lat_1=nclib.nc_get_varsValue('latitude',var_list,var_data_list)
    shts_time_1=nclib.nc_get_varsValue('time',var_list,var_data_list)
    shts_shts_1=nclib.nc_get_varsValue('shts',var_list,var_data_list)
    attr_list,global_attr,var_list,var_attr_list,var_data_list=nclib.read_ncfile(era5_filedir+era5_shts_filename2,('longitude','latitude','time','shts'))
    shts_lon_2=nclib.nc_get_varsValue('longitude',var_list,var_data_list)
    shts_lat_2=nclib.nc_get_varsValue('latitude',var_list,var_data_list)
    shts_time_2=nclib.nc_get_varsValue('time',var_list,var_data_list)
    shts_shts_2=nclib.nc_get_varsValue('shts',var_list,var_data_list)
    np.append(shts_time_1[0],shts_time_2[0][0])
    np.append(shts_shts_1[0],shts_shts_2[0][0])
    shts_shts_1[2]=shts_shts_1[2]+shts_shts_2[2]
    return [u10v10_lon_1,u10v10_lat_1,u10v10_time_1,u10v10_u10_1,u10v10_v10_1], \
        [shts_lon_1,shts_lat_1,shts_time_1,shts_shts_1]

if __name__=='__main__':
    pass
