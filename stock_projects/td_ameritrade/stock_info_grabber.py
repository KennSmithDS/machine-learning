from yahoo_finance import Share
import pandas as pd
import numpy as np

symbols = ['RGLS','HRZN','SPWR','PDVW','RMD','LOPE','VRML','BBG','SHO','GHDX','ARC','CGNT','DVA','EXR','STAG','RIGL','IPCC','IPHS','RIBT','FLEX',\
           'APTS','ROL','DEI','NFX','OKE','VOYA','KMB','REXR','SEAS','PBA','DSE','GSS','ZTR','FMC','SYX','UIS','ALL','PAG','RHI','RPXC','X','SKT','WAC.BC','VST','FTK']

def get_stock_info(ticker):
    temp_share = Share(ticker)
    real_price = temp_share.get_price()
    adj_price = (float(temp_share.get_open()) + float(temp_share.get_close()) + float(temp_share.get_high()) + float(temp_share.get_low()))/4
    real_vol = temp_share.get_volume()
    avg_vol = temp_share.get_avg_daily_volume()
    avg_50_day = temp_share.get_50day_moving_avg()
    avg_200_day = temp_share.get_200day_moving_avg()
    return real_price, adj_price, real_vol, avg_vol, avg_50_day, avg_200_day

#%%

get_stock_info('SPWR')

#%%
 
for symbol in symbols:
    get_stock_info(symbol)
    
#%%

spwr = Share('SPWR')
print(spwr.get_historical('2017-07-21','2017-08-01'))

#%%

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

data_source = 'google'

symbols = ['RGLS','HRZN','SPWR','PDVW','RMD','LOPE','VRML','BBG','SHO','GHDX','ARC','CGNT','DVA','EXR','STAG','RIGL','IPCC','IPHS','RIBT','FLEX',\
           'APTS','ROL','DEI','NFX','OKE','VOYA','KMB','REXR','SEAS','PBA','DSE','GSS','ZTR','FMC','SYX','UIS','ALL','PAG','RHI','RPXC','X','SKT','WAC.BC','VST','FTK']

symbol = 'SPWR'
           
start_date = '2017-08-01'
end_date = '2017-08-01'

panel_data = data.DataReader(symbols, data_source, start_date, end_date)
df_data = panel_data.to_frame()

print(df_data.info())

df_data = df_data.apply(pd.to_numeric, errors='ignore')
filtered = df_data[(df_data['Close'] <= 50) & (df_data['Volume'] >= 500000)]

filtered['Gap$'] = filtered['High'] - filtered['Low']
filtered['Gap%'] = (filtered['High'] - filtered['Low']) / filtered['Open']

print(filtered)