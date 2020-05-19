import pandas as pd
import numpy as np
import sys
import re
import requests
from bs4 import BeautifulSoup
from pandas_datareader import data, wb
import datetime as dt
import time
import warnings
warnings.simplefilter("ignore")

def run_screener():
    try:
        finviz_url = 'https://finviz.com/screener.ashx?v=111&f=exch_nasd,sh_avgvol_o1000,sh_price_o10,ta_averagetruerange_o4.5,ta_volatility_mo3&ft=4&o=price'
        headers = {'User-agent': 'Chrome/41.0.2228.0'}
        page = requests.get(finviz_url, headers = headers)
        html_text = page.text
        soup = BeautifulSoup(html_text, 'lxml')
        # screener_list = soup.find_all(class_="screener-body-table-nw")

        # Find all tickers in html body
        tickers = []
        links = soup.find_all('a', class_='screener-link-primary')
        for link in links:
            tickers.append(link.text)
        screen_df = pd.DataFrame(tickers)
        screen_df.columns = ['Ticker']
        return screen_df

        # find prices and % change in html body
        # prices = []
        # changes = []
        # numbers = re.findall('<span style="color:#008800;">(.*?)</span>', html_text)
        # for i in range(len(numbers)):
        #     if i%2==0:
        #         prices.append(numbers[i])
        #     else:
        #         changes.append(numbers[i])
        #
        # print(len(tickers))
        # print(len(prices))
        # print(len(changes))

        # screener_output = pd.DataFrame()
        # screener_output['Ticker'] = tickers
        # screener_output['Price'] = prices
        # screener_output['Change'] = changes
        # print(screener_output.head())
        # return screener_output

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, e))
        pass

def get_history_test(stock):
    try:
        # Establish start and end dates
        start_date = dt.datetime.today() - dt.timedelta(days=2)
        end_date = dt.datetime.today()

        # Call historic data from yahoo finance API
        test_data = data.DataReader(stock, 'yahoo', start_date, end_date)
        #print(test_data.head())

        # Assign values for relevant prices/changes
        price_close = test_data['Close'].iloc[-1]
        close_change = (test_data['Close'].iloc[-1]-test_data['Close'].iloc[-2])/test_data['Close'].iloc[-2]
        intraday_change = (test_data['Close'].iloc[-1]-test_data['Open'].iloc[-1])/test_data['Open'].iloc[-1]
        price_change_log = np.log(test_data['Close'].iloc[-1]/test_data['Close'].iloc[-2])

        # Display API results
        print('Closing Price: {}'.format(price_close))
        print('Price Close Change: {}'.format(close_change))
        print('Intraday Price Change: {}'.format(intraday_change))
        print('Log of Price Change: {}'.format(price_change_log))

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass

def get_history(df):
    try:
        # Establish start and end dates
        start_date = dt.datetime.today() - dt.timedelta(days=2)
        end_date = dt.datetime.today()

        # Create filler fields for df
        df['Close'] = 0
        df['CloseChange'] = 0
        df['LogCloseChange'] = 0
        df['IntradayChange'] = 0
        df['LogIntradayChange'] = 0

        # Assign values for relevant prices/changes
        for i in range(len(df)):
            stock = str(df['Ticker'].iloc[i]).lower()
            history = data.DataReader(stock, 'yahoo', start_date, end_date)
            df['Close'].iloc[i] = history['Close'].iloc[-1]
            df['CloseChange'] = (history['Close'].iloc[-1]-history['Close'].iloc[-2])/history['Close'].iloc[-2]
            df['LogCloseChange'] = np.log(history['Close'].iloc[-1]/history['Close'].iloc[-2])
            df['IntradayChange'] = (history['Close'].iloc[-1]-history['Open'].iloc[-1])/history['Open'].iloc[-1]
            df['LogIntradayChange'] = np.log(history['Close'].iloc[-1]/history['Open'].iloc[-1])
            sleeper = np.random.randint(1,15,1)
            time.sleep(sleeper[0])

        return df

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        pass

if __name__ == "__main__":

    # Execute program
    print('Fetching stock screener results from finviz.com website...')
    screener_list = run_screener()
    print('Finviz gave us these top 20 stocks...')
    print(screener_list)

    # print('Fetching historical quote data for screened stocks...')
    # test_stock = str(screener_list['Ticker'].iloc[0]).lower()
    # print(test_stock)
    # get_history_test(test_stock)
    #stocks_to_scan = get_history(screener_list)
    # print('Showing stocks with historical data...')
    #print(stocks_to_scan)

