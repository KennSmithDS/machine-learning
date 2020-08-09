import requests
import pandas as pd
import numpy as np
import json
import datetime as dt
import logging
from yahoo_historical import Fetcher
import time
import sys
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sb

def setup_logger(log_dir=None,
                 log_file=None,
                 log_format=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
                 log_level=logging.INFO):
    # Get logger
    logger = logging.getLogger('')
    # Clear logger
    logger.handlers = []
    # Set level
    logger.setLevel(log_level)
    # Setup screen logging (standard out)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(log_format)
    logger.addHandler(sh)
    # Setup file logging
    if log_dir and log_file:
        fh = logging.FileHandler(os.path.join(log_dir, log_file))
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    return logger

def classify(row):
    row_class = 0
    if row['close'] > row['open'] and row['close'] == row['high']:
        row_class = 2
    elif row['close'] > row['open'] and row['close'] < row['high']:
        row_class = 1
    # elif row['close'] < row['open'] and row['close'] > row['low']:
    #     row_class = 1
    else:
        pass
    return row_class

def get_equity_data(ticker, end_date, start_date):
    api_key = 'f'{api_key_here}%40AMER.OAUTHAP'
    end_date = '1526108400000'
    start_date = '1451606400000'
    #start_date = '1451635200000'
    type = 'minute'
    freq = '1'
    url = 'https://api.tdameritrade.com/v1/marketdata/' + ticker + '/pricehistory?apikey=' + api_key + '&frequencyType=' + type + '&frequency=' + freq + '&endDate=' + str(end_date) + '&startDate=' + str(start_date)
    print(url)
    response = requests.get(url)
    json_data = response.json()
    bars = pd.DataFrame(json_data['candles'])
    bars['equity'] = ticker
    bars['class'] = bars.apply(classify, axis=1)
    return bars

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

def remove_nonmarket_data(in_df):
    in_df['time'] = pd.DatetimeIndex(in_df['datetime'])
    in_df.set_index(keys='time', inplace=True)
    day_start = dt.time(0,0,0)
    mkt_start = dt.time(6,30,0)
    mkt_end = dt.time(13,0,0)
    day_end = dt.time(23,59,59)
    mkt_df = in_df.between_time(mkt_start,mkt_end)
    pre_mkt_df = in_df.between_time(day_start, mkt_start)
    post_mkt_df = in_df.between_time(mkt_end, day_end)
    frames = [pre_mkt_df,post_mkt_df]
    non_mkt_df = pd.concat(frames)
    return mkt_df, pre_mkt_df

# def get_min_val(row):
#     return dt.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S').minute
#
# def get_hour_val(row):
#     return dt.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S').hour
#
# def get_time_val(row):
#     return dt.datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S').time

def intraday_min_ranges(in_df):
    try:
        dates = in_df['date'].unique()
        intraday_dates_dic = {}
        # print(dates)

        for date in dates:
            log.info('Processing minute range arrays for market data on {}'.format(date))
            close_min_list = []
            for i in range(60):
                # print('Entering loop for {} minute(s)'.format(i+1))
                date_set = in_df[in_df['date']==date]
                temp_arr = date_set[['close']].values[0:i+1]
                # print('Temp array is: {}'.format(type(temp_arr)))
                # temp_stack_arr = np.vstack(temp_arr)
                # print('Temp stack array is: {}'.format(type(temp_stack_arr)))
                flat_min_closes = [val for sublist in temp_arr for val in sublist]
                # print(flat_min_closes)
                close_min_list.append(flat_min_closes)

            # print(type(each_days_arrs))
            # print(len(each_days_arrs))
            #each_days_arrs_stack = np.vstack(each_days_arrs)
            intraday_dates_dic[date] = close_min_list
            # print(type(intraday_dates_dic))

        # print(intraday_dates_dic['2018-04-30'])
        column_names = []
        for i in range(60):
            column_name = 'min_' + str(i+1)
            column_names.append(column_name)

        intraday_df = pd.DataFrame.from_dict(intraday_dates_dic, orient='index')
        # print(intraday_df.iloc[0])
        # print(intraday_df)
        intraday_df.columns = (column_names)

        return intraday_df
    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

def intraday_first_60min(in_df):
    dates = in_df['date'].unique()
    intraday_dates_dic = {}
    for date in dates:
        log.info('Processing first 60 minutes for market data on {}'.format(date))
        close_list = in_df[['close']].iloc[0:60].values
        flat_close_list = [val for sublist in close_list for val in sublist]
        intraday_dates_dic[date] = flat_close_list

    column_names = []
    for i in range(60):
        column_name = 'min_' + str(i+1)
        column_names.append(column_name)

    out_df = pd.DataFrame.from_dict(intraday_dates_dic, orient='index')
    out_df.colums = column_names
    return out_df

def make_premarket_array(in_df):
    dates = in_df['date'].unique()
    # tickers = in_df['equity'].unique()
    premarket_dates_dic = {}

    # for ticker in tickers:
    for date in dates:
        log.info('Processing minute range arrays for premarket data on {}'.format(date))
        date_set = in_df[(in_df['date'] == date)]# & (in_df['equity']==ticker)]
        temp_arr = date_set[['close']].values
        # print(flat_min_closes[0:10])
        premarket_dates_dic[date] = temp_arr

    # print(premarket_dates_dic)
    premarket_df = pd.DataFrame.from_dict(premarket_dates_dic, orient='index')
    # print(premarket_df)
    premarket_df.columns = ['premarket_min_closes']
    return premarket_df

def flatten_premarket(row):
    return [val for sublist in row['premarket_min_closes'] for val in sublist]

def show_distribution(df):
    x = df[['open']]
    sb.distplot(x)
    plt.show()

    sb.boxplot(x='class', y='open', data=df)
    plt.show()

def feature_correlations(df):
    corr = df.corr()
    corr_heatmap = sb.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values)
    loc, labels = plt.xticks()
    corr_heatmap.set_xticklabels(labels, rotation=90)
    corr_heatmap.set_yticklabels(labels[::-1], rotation=0)  # reversed order for y
    plt.show()

    y = df[['class']]
    df.drop(['class'], axis=1, inplace=True)
    X = df
    estimator = LinearRegression()
    selector = RFE(estimator, 5, step=1)
    selector = selector.fit(X, y)
    feature_bool = selector.support_
    log.info('Here are the columns to keep: \n{}'.format(feature_bool))
    log.info('Here is the ranking of each column: \n{}'.format(selector.ranking_))

def create_random_forest(Xt, yt):
    try:
        forest = RandomForestClassifier(max_depth=3, random_state=42)
        forest.fit(Xt, yt)
        # cols = Xt.columns
        # for i in range(len(Xt.columns)):
        #     log.info(cols[i], forest.feature_importances_[i])
        log.info('Feature importance array of random forest: \n{}'.format(forest.feature_importances_))
        y_pred = np.array(forest.predict(Xt)).reshape(len(Xt))
        y_target = np.array(yt).reshape(len(yt))
        acc1 = metrics.accuracy_score(y_target, y_pred)
        log.info('Accuracy of random forest classifier before feature selection: {}'.format(acc1))
    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

if __name__ == "__main__":

    # Setup directories
    data_dir = 'data'
    logging_dir = 'logs'
    time_date = dt.datetime.now()
    string_date = time_date.strftime("%Y%m%d_%H%M%S")

    # Setup Logging
    logging_level = logging.INFO
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    logging_file = 'kendall_smith_stock_intraday_moves_log_{}.log'.format(string_date)
    log = setup_logger(logging_dir, logging_file, log_level=logging_level)

    try:
        # Configure start and end dates in epoch format
        # ticker = 'SPY'
        # end_dt = dt.date.today().strftime("%Y %m %d")
        # start_dt = (datetime.date.today() - datetime.timedelta(days=90)).strftime("%Y %m %d")
        # start_dt = dt.datetime.strptime('2017-08-28', '%Y-%m-%d').strftime("%Y %m %d")
        # print('Date range starts on {} and ends on {}.'.format(start_dt, end_dt))
        # end_date_ls = [int(n) for n in end_dt.split(" ")]
        # start_dt_ls = [int(n) for n in start_dt.split(" ")]
        # end_dt_ep = convert_to_epoch(end_dt)
        # start_dt_ep = convert_to_epoch(start_dt)
        # print('The epoch equivalent is {} and {} respectively.'.format(start_dt_ep, end_dt_ep))

        # Get minute pricing data from TD Ameritrade API
        # price_data = get_equity_data(ticker, end_dt_ep, start_dt_ep)
        # print(price_data.head())
        # price_data['epoch'] = price_data['datetime']
        # price_data['date'] = price_data.apply(convert_to_date, axis=1)
        # price_data['datetime'] = price_data.apply(convert_to_datetime, axis=1)
        # print(price_data.tail())
        # print(len(price_data))

        # Saving pricing data from TD Ameritrade API to CSV
        # price_data.to_csv('SPY_prices_min_2016_to_2018.csv', index=False)

        # Open CSV data for 1-minute granularity
        log.info('Reading minute price data file...')
        #spy_1_min_data = pd.read_csv('master_min_price_data.csv')
        spy_1_min_data = pd.read_csv('SPY_prices_1min_2016_to_2018.csv')
        spy_1_min_mkt_data, spy_1_min_premkt_data = remove_nonmarket_data(spy_1_min_data)
        spy_1_min_premkt_arr_data = make_premarket_array(spy_1_min_premkt_data)
        spy_1_min_mkt_arr_data = intraday_first_60min(spy_1_min_mkt_data)
        # spy_1_min_mkt_arr_data = intraday_min_ranges(spy_1_min_mkt_data)
        # print('Showing snippet of minute array data for market times...')
        # print(spy_1_min_mkt_arr_data.iloc[2])
        # print('Showing shippet of minute array data for premarket times...')
        # print(spy_1_min_premkt_arr_data.iloc[2])
        # spy_1_min_data['hour'] = spy_1_min_data.apply(get_hour_val, axis=1)
        # spy_1_min_data['min'] = spy_1_min_data.apply(get_min_val, axis=1)

        # Open CSV data for 5-minute granularity
        # log.info('Opening data file with 5 minute data...')
        # spy_5_min_data = pd.read_csv('SPY_prices_5min_2016_to_2018.csv')
        # spy_5_min_mkt_data, spy_5_min_not_mkt_data = remove_nonmarket_data(spy_5_min_data)
        # spy_5_min_data['hour'] = spy_5_min_data.apply(get_hour_val, axis=1)
        # spy_5_min_data['min'] = spy_5_min_data.apply(get_min_val, axis=1)

        # Open CSV data for 15-minute granularity
        # log.info('Opening data file with 15 minute data...')
        # spy_15_min_data = pd.read_csv('SPY_prices_15min_2016_to_2018.csv')
        # spy_15_min_mkt_data, spy_15_min_not_mkt_data = remove_nonmarket_data(spy_15_min_data)
        # spy_15_min_data['hour'] = spy_15_min_data.apply(get_hour_val, axis=1)
        # spy_15_min_data['min'] = spy_15_min_data.apply(get_min_val, axis=1)

        # Open CSV data for 30-minute granularity
        # log.info('Opening data file with 30 minute data...')
        # spy_30_min_data = pd.read_csv('SPY_prices_30min_2016_to_2018.csv')
        # spy_30_min_mkt_data, spy_30_min_not_mkt_data = remove_nonmarket_data(spy_30_min_data)
        # spy_30_min_data['hour'] = spy_30_min_data.apply(get_hour_val, axis=1)
        # spy_30_min_data['min'] = spy_30_min_data.apply(get_min_val, axis=1)

        # Get daily pricing data from yahoo historical API
        # fetcher_data = Fetcher(ticker, start_dt_ls, end_date_ls, interval="1d")
        # day_data = fetcher_data.getHistorical()
        # day_data['ticker'] = ticker
        # day_data.columns = ['date','open','high','low','close','adj close','volume','ticker']
        # day_data['class'] = day_data.apply(classify, axis=1)
        # print(day_data.head())

        # Saving pricing data from yahoo API to CSV
        # day_data.to_csv('SPY_prices_1d_2016_to_2018.csv', index=False)

        # Open CSV data on daily granularity
        log.info('Reading daily price data file...')
        #spy_1_day_data = pd.read_csv('master_day_price_data.csv')
        spy_1_day_data = pd.read_csv('SPY_prices_1d_2016_to_2018.csv')
        spy_1_day_df = spy_1_day_data[spy_1_day_data['date'] >= '2018-04-06'][['date', 'open', 'high', 'low', 'close', 'volume','class']]
        spy_1_day_df.set_index('date', inplace=True)
        # print('Showing snippet of daily price data...')
        # print(spy_1_day_df.iloc[2])

        # Merge/join daily data with intraday arrays into single dataframe object
        spy_intraday_df = spy_1_day_df.join(spy_1_min_mkt_arr_data)
        # spy_intraday_df = spy_intraday_df.join(spy_1_min_premkt_arr_data)
        spy_intraday_df.dropna(inplace=True)
        spy_intraday_bkup = spy_intraday_df
        # spy_intraday_df['premarket_min_closes'] = spy_intraday_df.apply(flatten_premarket, axis=1)
        spy_intraday_df.reset_index(inplace=True)
        spy_intraday_df.drop(['date'], axis=1, inplace=True)
        # print(spy_intraday_df.head())
        # print('Showing snippet of merged daily and minute dataframe...')
        # print(spy_intraday_df.iloc[2])

        # Display distribution and correlations between features
        # show_distribution(spy_intraday_df)
        # feature_test_df = spy_intraday_df.drop(['open','high','low','close','volume'], axis=1)
        # feature_correlations(spy_intraday_df)
        # log.info('Logging summary info of merged dataframe: \n{}'.format(spy_intraday_df.info()))
        log.info('Logging statistical description of merged dataframe: \n{}'.format(spy_intraday_df.describe()))

        # Define X and y from dataframe
        log.info('Assigning X and y variables and scaling data...')
        # print(spy_intraday_df.columns)
        y = spy_intraday_df[['class']]
        spy_intraday_df.drop(['class'], axis=1, inplace=True)
        training_df = spy_intraday_df[['open','high','low','volume']]
        X = training_df
        scaler = preprocessing.StandardScaler().fit(X)
        X_scaled = scaler.transform(X)
        # print(X_scaled[0:5])
        # print(y[0:5])

        # Split data into training and testing sets using 30% test size
        log.info('Creating train and test sets...')
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
        log.info('Length of X training set = {} records.'.format(len(X_train)))
        log.info('Length of X testing set = {} records.'.format(len(X_test)))
        log.info('Length of y training set = {} records.'.format(len(y_train)))
        log.info('Length of y testing set = {} records.'.format(len(y_test)))

        # Instantiate random forest classifier and test accuracy
        log.info('Building random forest with training data...')
        create_random_forest(X_train, y_train)

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass
