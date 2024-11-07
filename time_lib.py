''' 
Auth: Jiawei Zheng, GNSS Research Center, Wuhan University
Cont: jwzheng@whu.edu.cn
Github: https://github.com/jwzhengWHU
Profile: http://panda.whu.edu.cn/info/1329/1401.htm
ResearchGate: https://www.researchgate.net/profile/Jiawei-Zheng-4
GoogleScholar: https://scholar.google.com.hk/citations?user=0Te3Ps0AAAAJ&hl=zh-CN
'''

import os

def yr2year(yr):
    if yr>1900:
        year=yr
    elif yr<50:
        year=yr+2000
    else:
        year=yr+1900
    return year

def ymd2mjd(year,month,day):
    doy_of_month=[0,31,59,90,120,151,181,212,243,273,304,334]
    yr=year
    if month<=2:
        yr=yr-1
    mjd=365*year-678941+int(yr/4)-int(yr/100)+int(yr/400)+day
    if month!=0:
        mjd=mjd+doy_of_month[month-1]
    return mjd

def mjd2ymd(mjd):
    a=int(mjd+2400000.5+0.5)
    b=a+1537
    c=int((b-122.1)/365.25)
    d=int(365.25*c)
    e=int((b-d)/30.6001)
    day=int(b-d-int(30.6001*e)+(mjd+2400000.5+0.5-a))
    month=e-1-12*int(e/14)
    year=c-4715-int((7+month)/10)
    return [year,month,day]

def hms2sod(hour,minute,second):
    sod=hour*3600+minute*60+second
    return sod

def sod2hms(sod):
    hour=int(sod/3600)
    minute=int((sod-hour*3600)/60)
    second=sod-hour*3600-minute*60
    return [hour,minute,second]

def ymdhms2mjdd(year,month,day,hour,minute,second):
    mjd=ymd2mjd(year,month,day)
    sod=hms2sod(hour,minute,second)
    mjdd=mjd+sod/86400
    return mjdd

def mjdd2gpsweek(mjdd):
    gps_week=(mjdd-44244)//7
    gps_day=mjdd-44244-gps_week*7
    gps_second=(mjdd-44244)*3600*24-gps_week*3600*24*7
    return [gps_week,gps_day,gps_second]

def ymdhms2gpsweek(year,month,day,hour,minute,second):
    mjdd=ymdhms2mjdd(year,month,day,hour,minute,second)
    gpsweek=mjdd2gpsweek(mjdd)
    return gpsweek

def gpsweek2mjdd(gpsweek,sow):
    return (sow+gpsweek*3600*24*7)/(3600*24)+44244

def mjdd2mjdsod(mjdd):
    mjd=int(mjdd)
    sod=(mjdd-mjd)*24*3600
    return [mjd,sod]

def gpsweek2ymdhms(gpsweek,sow):
    mjdd=gpsweek2mjdd(gpsweek,sow)
    mjdsod=mjdd2mjdsod(mjdd)
    ymd=mjd2ymd(mjdsod[0])
    hms=sod2hms(mjdsod[1])
    return [ymd[0],ymd[1],ymd[2],hms[0],hms[1],hms[2]]

def ydoy2ymd(year,doy):
    [month,day]=[9999,9999]
    dom=[31,28,31,30,31,30,31,31,30,31,30,31]
    if((year%4==0 and year%100!=0) or year%400==0):
        dom[1]=29
    for imonth in range(12):
        doy=doy-dom[imonth]
        if(doy>0):
            continue
        day=doy+dom[imonth]
        month=imonth+1
        break
    return [year,month,day]
    
def mjd2ydoy(mjd):
    year=(mjd+678940)//365
    doy=mjd-ymd2mjd(year,1,1)
    while(doy<0):
        year=year-1
        doy=mjd-ymd2mjd(year,1,1)+1
    return [year,doy]

def ymd2ydoy(year,month,day):
    mjd=ymd2mjd(year,month,day)
    [year,doy]=mjd2ydoy(mjd)
    return [year,doy]
    
def get_dom(year,month):
    dom=[31,28,31,30,31,30,31,31,30,31,30,31]
    if((year%4==0 and year%100!=0) or year%400==0):
        dom[1]=29
    return dom[month-1]
    
def ymd_plus_oneday(year,month,day):
    mjd=ymd2mjd(year,month,day)
    return mjd2ymd(mjd+1)
    
if __name__ == "__main__":
    os.system("cls")
    print(mjdd2gpsweek(ymd2mjd(2020,2,2)))
    print(mjdd2gpsweek(59244))
    print(sod2hms(44175))
    print(ydoy2ymd(2020,62))
    print(ymd2ydoy(2020,3,2))
    