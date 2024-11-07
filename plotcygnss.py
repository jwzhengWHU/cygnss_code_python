''' 
Auth: Jiawei Zheng, GNSS Research Center, Wuhan University
Cont: jwzheng@whu.edu.cn
Github: https://github.com/jwzhengWHU
Profile: http://panda.whu.edu.cn/info/1329/1401.htm
ResearchGate: https://www.researchgate.net/profile/Jiawei-Zheng-4
GoogleScholar: https://scholar.google.com.hk/citations?user=0Te3Ps0AAAAJ&hl=zh-CN
'''

import os
os.environ['PROJ_LIB']='~/anaconda3/pkgs/proj4-5.2.0-h295c915_1001/share/proj'
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
import pyproj
from pyproj import Proj, transform
import pandas as pd
import numpy as np
import glob
 
# In[define a function to read nc file]
def read_ncfile(nc_file):
    ncfile=Dataset(nc_file)
        #Specular point position Z(meter)ECEF
    sp_rx_gain=(ncfile.variables['sp_pos_z'][:])     #Specular point Rx antenna gain(dBi)
    return [sp_x,sp_y,sp_z,sp_rx_gain]
x=[]
y=[]
z=[]
files=glob.glob('./data/*')
for file in files:
    data=read_ncfile(file)
    sp_x=data[0]
    sp_y=data[1]
    sp_z=data[2]
    x=np.append(x,sp_x)
    y=np.append(y,sp_y)
    z=np.append(z,sp_z)
    
ecef = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
lla= pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
B,L,H = pyproj.transform(lla, ecef, x, y, z, radians=False)  # radians否用弧度返回值
fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])
map = Basemap()
map.shadedrelief(scale=0.1)
map.drawparallels(circles=np.linspace(-90, 90, 7),
                  labels=[1, 0, 0, 0], color='gray')
map.drawmeridians(meridians=np.linspace(-180, 180, 13),
                  labels=[0, 0, 0, 1], color='gray')
map.scatter(B,L, marker='o', s=10, facecolor='#00BFFF',
            edgecolor='k', linewidth=0.1)
plt.savefig('./test.png')
