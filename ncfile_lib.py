#! ~/anaconda3/envs/cygnss/bin/python

''' 
Auth: Jiawei Zheng, GNSS Research Center, Wuhan University
Cont: jwzheng@whu.edu.cn
Github: https://github.com/jwzhengWHU
Profile: http://panda.whu.edu.cn/info/1329/1401.htm
ResearchGate: https://www.researchgate.net/profile/Jiawei-Zheng-4
GoogleScholar: https://scholar.google.com.hk/citations?user=0Te3Ps0AAAAJ&hl=zh-CN
'''

from netCDF4 import Dataset

def readGlobalAttrs(nc_file):
    """
    Usag: attr_list,global_attr=readGlobalAttrs(nc_file)
    Purp: read and return global_atts
    Auth: jwzheng@whu.edu.cn
    Date: 2023/10/30
    """
    attr_list=[]
    global_attr=[]
    for attr_name in nc_file.ncattrs():
        attr_list.append(attr_name)
        atts=getattr(nc_file,attr_name)
        global_attr.append(atts)
    return attr_list,global_attr 

def readVars(nc_file,vars=()):
    """
    Usag: var_list,var_attr_list,var_data_list=readVars(nc_file)
    Usag: var_list,var_attr_list,var_data_list=readVars(nc_file,vars)
    Purp: read and return variables and their attributes
    Auth: jwzheng@whu.edu.cn
    Date: 2023/10/30
    """
    keys=nc_file.variables.keys()
    if(len(vars)==0):
        vars=keys
    var_attr_list=[]
    var_data_list=[]
    var_list=[]   
    for var in vars:
        if(var not in keys):
            print('###ERROR### read_ncfile.py ---> '+var+' not in keys!')
            continue
        attr=nc_file.variables[var]
        vardata=nc_file.variables[var][:]
        var_list.append(var)
        var_attr_list.append(attr)
        var_data_list.append(vardata)
    return var_list,var_attr_list,var_data_list

def read_ncfile(ncfile,vars=()):
    """
    Usag: attr_list,global_attr,var_list,var_attr_list,var_data_list=read_ncfile(ncfile)
    Usag: attr_list,global_attr,var_list,var_attr_list,var_data_list=read_ncfile(ncfile,vars)
    Purp: read ncfile
    Auth: jwzheng@whu.edu.cn
    Date: 2023/10/30
    """
    try:
        nc_file=Dataset(ncfile,'r')
    except IOError:
        print('not a valid netCDF file')
    attr_list,global_attr=readGlobalAttrs(nc_file)
    var_list,var_attr_list,var_data_list=readVars(nc_file,vars)
    nc_file.close()
    return attr_list,global_attr,var_list,var_attr_list,var_data_list

def nc_get_varsValue(var,var_list,var_data_list):
    var_data_ma=var_data_list[var_list.index(var)]
    fillvalue=var_data_ma.fill_value
    var_data=var_data_ma.filled(fill_value=fillvalue)
    if(var_data_ma.fill_value in var_data): fillflag=1
    else: fillflag=0
    return [var_data,fillvalue,fillflag]

def nc_varsValue_isnoteffective(var_data_value,fillvalue,fillflag):
    if(fillflag==0): return 0
    else: 
        if(var_data_value==fillvalue): return 1
        else: return 0

if __name__=='__main__':
   pass     
 
