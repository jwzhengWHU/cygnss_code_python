#! ~/anaconda3/envs/cygnss/bin/python

''' 
Auth: Jiawei Zheng, GNSS Research Center, Wuhan University
Cont: jwzheng@whu.edu.cn
Github: https://github.com/jwzhengWHU
Profile: http://panda.whu.edu.cn/info/1329/1401.htm
ResearchGate: https://www.researchgate.net/profile/Jiawei-Zheng-4
GoogleScholar: https://scholar.google.com.hk/citations?user=0Te3Ps0AAAAJ&hl=zh-CN
'''

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def savefig(fig_savepath):
    plt.savefig(fig_savepath,dpi=360,bbox_inches='tight')
    plt.close('all')

def global_01():
    plt.figure(figsize=(12,9))
     # projection=cyl,robin,ortho
     # c(crude),l(low),i(intermediate),h(high),f(full)
    mymap=Basemap(projection='robin',lat_0=0,lon_0=0,resolution='i',area_thresh=5000.0)
     # color=gray,slategray,olive
    mymap.fillcontinents(color='white',lake_color='lightskyblue')
    mymap.drawmapboundary(fill_color='skyblue')
    mymap.drawmeridians(np.arange(0,360,60),labels=[1,0,0,1])
    mymap.drawparallels(np.arange(-90,90.001,30),labels=[1,0,0,1])
    return mymap
    
def global_02():
    mymap=Basemap()
    mymap.drawcoastlines()
    mymap.drawcountries()
    return mymap
    
def region():
    mymap = Basemap(llcrnrlon=-160.,llcrnrlat=0.,urcrnrlon=-60.,urcrnrlat=80., lat_0=40., lon_0=-110.,
                 resolution='i', area_thresh=5000.0)
    meridians=np.arange(-160.,-60.001,20.)
    mymap.drawmeridians(meridians,labels=[True,False,False,True])
    mymap.fillcontinents(color='white', lake_color='lightskyblue')
    mymap.drawmapboundary(fill_color='skyblue')
    mymap.drawmeridians(np.arange(0, 360, 60), labels=[1,0,0,1])
    mymap.drawparallels(np.arange(-90, 90.001, 30), labels=[1,0,0,1])
    return mymap

def ddm():
    fig,ax=plt.subplots(figsize=(9,12))
    ax.set_xticks(np.arange(11))
    ax.set_yticks(np.arange(17))
    #plt.imshow(var_data_list[3][0][0],cmap='jet',origin='upper',aspect="auto")
    # cmap: virdis
    plt.colorbar()
    plt.savefig('./ddm.png',bbox_inches='tight')

if __name__=='__main__':
    pass
