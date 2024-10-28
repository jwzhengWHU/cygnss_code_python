#! ~/anaconda3/envs/cygnss/bin/python

import cdsapi
import numpy as np
import os

import time_lib as tlib

def download_ECMWF_ERA5(year,month,day,ERA5_vars,save_dir):
    c=cdsapi.Client()
    c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type':'reanalysis',
        'format':'netcdf',
        'variable':ERA5_vars,
        'year':year,
        'month':month,
        'day':day,
        'time':[
            '00:00','01:00','02:00',
            '03:00','04:00','05:00',
            '06:00','07:00','08:00',
            '09:00','10:00','11:00',
            '12:00','13:00','14:00',
            '15:00','16:00','17:00',
            '18:00','19:00','20:00',
            '21:00','22:00','23:00',
        ],
    },
    save_dir+year+month+day+'.nc')
    
if __name__=='__main__':
    os.system('clear')
    save_dir='./ERA5/era5_reanalysis_u10_v10_'
    ERA5_vars=['10m_u_component_of_wind','10m_v_component_of_wind']
    # save_dir='./ERA5/era5_reanalysis_shts_'
    # ERA5_vars=['significant_height_of_total_swell']
    years=np.arange(2020,2021,1)
    months=np.arange(8,9,1)
    for year in years:
        year_str='{:04d}'.format(year)
        for month in months:
            month_str='{:02d}'.format(month)
            dom=tlib.get_dom(year,month)
            days=np.arange(1,dom+1,1)
            for day in days:
                day_str='{:02d}'.format(day)
                download_ECMWF_ERA5(year_str,month_str,day_str,ERA5_vars,save_dir)
                
