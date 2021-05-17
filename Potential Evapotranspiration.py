import numpy as np
import pandas as pd
import math as m
def windspeed():
    df=pd.read_excel(x)
    df['E']=(df['WKH']*4.87)/np.log1p(67.8*df['ELV']-(5.42))
    return df['E']
def slopecurve():
    df=pd.read_excel(x)
    df['C']=(df['MAX']+df['MIN'])/2
    df['D']=np.exp((17.27*df['C']/(df['C']+237.3)))
    df['E']=(4098*0.6108*df['D'])/(np.power((df['C']+237.3),2))
    return df['E']
def relativehumidity():
    df = pd.read_excel(x)
    df['D']= (df['MAX']+df['MIN'])/2
    df['E']= 0.6108*np.exp(((17.27*df['D'])/(df['D']+237.3)))
    df['F']=(df['E']*(df['RH']/100))
    df['G']=df['E']-df['F']
    return df['G']
def psychometric():
    df = pd.read_excel(x)
    df['C']= ((293-(0.0065*df['ELV']))/293)
    df['D']=101.3*(np.power(df['C'],5.26))
    df['E']=((1.013*m.pow(10,-3)*df['D']))/(0.622*2.45)
    return df['E']
def radiaton():
    df = pd.read_excel(x)
    df['TEM'] = (df['MAX'] + df['MIN']) / 2
    df['E'] = 0.6108 * np.exp(((17.27 * df['TEM']) / (df['TEM'] + 237.3)))
    df['F'] = (df['E'] * (df['RH'] / 100))
    df['LA']= df['LAT']*(np.pi/180)
    df['DR']= 1+(0.033*np.cos((2*np.pi/365)*df['DAYS']))
    df['SD']= 0.409*np.sin(((2*np.pi/365)*df['DAYS'])-1.39)
    df['WS']=np.arccos(-np.tan(df['LA'])*np.tan(df['SD']))
    df['RA']=((24*60)/np.pi)*0.0820*df['DR']*((df['WS']*np.sin(df['LA'])*np.sin(df['SD']))+(np.cos(df['LA'])*np.cos(df['SD'])*np.sin(df['WS'])))
    df['MAXDURATION']= (24/np.pi)*df['WS']
    df['RS']=0.20+(0.50*(6/df['MAXDURATION']))*df['RA']
    df['RS0']=(0.75+(2*np.exp(m.pow(10,-5)))*df['ELV'])*(df['RA'])
    df['RNS']=(1-0.23)*df['RS']
    df['RNL']= 4.903*m.pow(10,-9)*(((np.power((df['MAX']+273.16),4))+(np.power((df['MIN']+273.16),4)))/2)*(0.34-(0.14*np.sqrt(df['F'])))*((1.35*(df['RS']/df['RS0']))-0.35)
    df['RN']=df['RNS']-df['RNL']
    return df['RN']
print('EVAPOTRANSPIRATION CALUCULATOR FOR X YEARS:')
x=input('Please enter the path in which the input excel file is present with extension : ')
y=input('Please enter the path in which the output excel file should be exported with extension : ')
df = pd.read_excel(x)
df['TEM'] = (df['MAX'] + df['MIN']) / 2
df['WI']=windspeed()
df['SL']=slopecurve()
df['RH']=relativehumidity()
df['PY']=psychometric()
df['RN']=radiaton()
df['EVA']=((0.408*df['SL']*(df['RN']-0.329))+(df['PY']*(900/(df['TEM']+273))*(df['WI']*df['RH'])))/(df['SL']+(df['PY']*(1+(0.34*df['WI']))))
df['PEVA']=df['EVA']*0.85
print(df['EVA'])
export_excel = df.to_excel(y)



