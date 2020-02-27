import requests
import pandas as pd
import json
import sys
import time
import numpy as np
import os
import datetime as dt

def classify(row):
    row_class = 0
    if row['close'] > row['open'] and row['close'] == row['high']:
        row_class = 3
    elif row['close'] > row['open'] and row['close'] < row['high']:
        row_class = 2
    elif row['close'] < row['open'] and row['close'] > row['low']:
        row_class = 1
    else:
        pass
    return row_class

def get_equity_data(ticker):
    try:
        api_key = 'YOUR API KEY HERE'
        end_date = '1526108400000'
        start_date = '1451606400000'
        type = 'minute'
        freq = '1'
        url = 'https://api.tdameritrade.com/v1/marketdata/' + ticker + '/pricehistory?apikey=' + api_key + '&frequencyType=' + type + '&frequency=' + freq + '&endDate=' + str(end_date) + '&startDate=' + str(start_date)
        print(url)
        response = requests.get(url)
        json_data = response.json()
        print(json_data)
        bars = pd.DataFrame(json_data['candles'])
        if not bars.empty():
            print(bars.info())
            bars['equity'] = ticker
            bars['class'] = bars.apply(classify, axis=1)
            return bars
        else:
            bars['equity'] = ticker
            bars['class'] = 0
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), e)
        pass

def convert_to_datetime(row):
    ts = row['datetime'] / 1000.0
    dts = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return dts

def convert_to_date(row):
    ts = row['datetime'] / 1000.0
    date = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    return date

def convert_to_epoch(date):
    pattern = '%Y %m %d'
    return int(time.mktime(time.strptime(date, pattern)))*1000

if __name__ == '__main__':
    ticker_list = ['SPY','UVXY','GLD','LQD','VTI','IVV','QQQ','AAPL','AMZN','IWM','DIA','GOOGL','MSFT','FB','XOM','JNJ','JPM','BAC','XLK','NVDA','INTC','CSCO','CMCSA','NFLX','AMGN','ADBE','TXN','BKNG','AVGO','BIDU','PYPL','COST','GILD','ASML','QCOM','PEP','SBUX']

    try:
        for ticker in ticker_list:
            ticker_bars = get_equity_data(ticker)
            filename = ticker + '_prices_1min_2016_to_2018.csv'
            if ticker_bars is None:
                print('API extraction failed for ' + ticker + ', continuing to next ticker.')
                pass
            else:
                ticker_bars['epoch'] = ticker_bars['datetime']
                ticker_bars['date'] = ticker_bars.apply(convert_to_date, axis=1)
                ticker_bars['datetime'] = ticker_bars.apply(convert_to_datetime, axis=1)
                ticker_bars.to_csv(filename, index=False)
            sleeper = np.random.randint(15,45)
            print('Sleep timer for {} seconds.'.format(str(sleeper)))
            time.sleep(sleeper)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass
