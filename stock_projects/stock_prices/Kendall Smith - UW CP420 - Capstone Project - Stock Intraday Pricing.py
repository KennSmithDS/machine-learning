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
import warnings
warnings.simplefilter("ignore")
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor

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
        row_class = 3
    elif row['close'] > row['open'] and row['close'] < row['high']:
        row_class = 2
    elif row['close'] < row['open'] and row['close'] > row['low']:
        row_class = 1
    else:
        pass
    return row_class

def unscaled_histogram(df):
    x = df['close']
    plt.hist(x, bins='auto')
    plt.title('Histogram of Unscaled Pricing Data')
    plt.xlabel('Equity Price')
    plt.show()

def scaled_histogram(df):
    min_cols = df.filter(regex='min').copy()
    print(min_cols.head())
    min_cols.drop(['volume_15_min','volume_30_min','volume_45_min','volume_60_min'], axis=1, inplace=True)
    print(min_cols.head())
    print(df.head())
    x = [val for sublist in min_cols.values for val in sublist]
    print(x[0:25])
    plt.hist(x, bins='auto')
    plt.title('Histogram of Scaled Pricing Data')
    plt.xlabel('Equity Price')
    plt.show()

def get_equity_data(ticker, end_date, start_date):
    api_key = f'{api_key_here}%40AMER.OAUTHAP'
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

def convert_to_weekday(row):
    pattern = '%Y-%m-%d'
    weekday = dt.datetime.strptime(row['date'], pattern).weekday()
    return weekday

def convert_to_epoch(date):
    pattern = '%Y %m %d'
    return int(time.mktime(time.strptime(date, pattern)))*1000

def convert_str_date(row):
    pattern = '%m/%d/%Y'
    date = dt.datetime.strptime(row['date'], pattern).strftime('%Y-%m-%d')
    # print('Converting {} to {}'.format(row['date'],date))
    return date

def etf_yes_no(row):
    etf_list = ['SPY',	'UVXY',	'GLD',	'LQD',	'VTI',	'IVV',	'QQQ',	'IWM',	'DIA',	'XLK']
    if row['ticker'] in etf_list:
        etf_switch = 1
    else:
        etf_switch = 0
    return etf_switch

def split_nonmarket_data(in_df):
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
    mkt_df.sort_values(by=['ticker','datetime'], inplace=True)
    pre_mkt_df.sort_values(by=['ticker','datetime'], inplace=True)
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
    try:
        dates = np.sort(in_df['date'].unique())
        tickers = in_df['ticker'].unique()
        list_of_dicts = []
        for ticker in tickers:
            ticker_set = in_df[in_df['ticker']==ticker]
            for date in dates:
                intraday_dates_dic = {}
                log.info('Processing first 60 minutes for market data on {} for {}'.format(date, ticker))
                date_set = ticker_set[ticker_set['date']==date]
                if len(date_set[['close']].iloc[0:60].values) > 0:
                    scaled_closes = scale_something(date_set[['close']].iloc[0:60].values)
                    vol_15_min = np.sum(date_set['volume'].iloc[0:15].values)
                    vol_30_min = np.sum(date_set['volume'].iloc[15:30].values)
                    vol_45_min = np.sum(date_set['volume'].iloc[30:45].values)
                    vol_60_min = np.sum(date_set['volume'].iloc[45:60].values)
                    flat_close_list = [val for sublist in scaled_closes for val in sublist]
                    for i in range(len(flat_close_list)):
                        col_name = 'min_' + str(i+1).zfill(2)
                        intraday_dates_dic[col_name] = flat_close_list[i]
                        intraday_dates_dic['date'] = date
                        intraday_dates_dic['ticker'] = ticker
                        intraday_dates_dic['volume_15_min'] = vol_15_min
                        intraday_dates_dic['volume_30_min'] = vol_30_min
                        intraday_dates_dic['volume_45_min'] = vol_45_min
                        intraday_dates_dic['volume_60_min'] = vol_60_min
                    list_of_dicts.append(intraday_dates_dic)
                else:
                    log.info('There is no data for {} on {}'.format(ticker, date))
                    pass

        out_df = pd.DataFrame(list_of_dicts)
        return out_df
    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

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

    x = df[['close']]
    sb.distplot(x)
    plt.show()

    sb.boxplot(x='class', y='open', data=df)
    plt.show()

    sb.boxplot(x='class', y='close', data=df)
    plt.show()

def day_of_week_plot(df):
    sb.boxplot(x='dayofweek', y='close', hue='class', data=df)
    plt.show()

def feature_correlations(df):
    corr = df.corr()
    corr_heatmap = sb.heatmap(corr, xticklabels=corr.columns.values, yticklabels=corr.columns.values)
    loc, labels = plt.xticks()
    corr_heatmap.set_xticklabels(labels, rotation=90)
    corr_heatmap.set_yticklabels(labels[::-1], rotation=0)  # reversed order for y
    plt.show()

    y = df[['class']]
    xdf = df.drop(['class','ticker'], axis=1)
    X = xdf
    cols = X.columns
    estimator = LinearRegression()
    selector = RFE(estimator, 5, step=1)
    selector = selector.fit(X, y)
    feature_bool = selector.support_
    feature_rank = selector.ranking_
    for i in range(len(cols)):
        log.info('Feature Bool {} : {}'.format(cols[i],feature_bool[i]))
        log.info('Feature Rank {} : {}'.format(cols[i],feature_rank[i]))

def create_random_forest(Xt, yt):
    try:
        forest = RandomForestClassifier(max_depth=3, random_state=42)
        forest.fit(Xt, yt)
        # cols = Xt.columns
        # for i in range(len(Xt.columns)):
        #     log.info(cols[i], forest.feature_importances_[i])
        feature_imp = forest.feature_importances_
        cols = Xt.columns
        list_of_feature_imp = []
        rfc_imp_features = []
        for i in range(len(cols)):
            log.info('Feature importance of {} in random forest: {}'.format(cols[i], feature_imp[i]))
            rfc_features_dict = {}
            rfc_features_dict['col'] = cols[i]
            rfc_features_dict['imp'] = feature_imp[i]
            list_of_feature_imp.append(rfc_features_dict)
            if feature_imp[i] >= .025:
                rfc_imp_features.append(cols[i])
            else:
                pass
        y_pred = np.array(forest.predict(Xt)).reshape(len(Xt))
        y_target = np.array(yt).reshape(len(yt))
        acc1 = metrics.accuracy_score(y_target, y_pred)
        log.info('Accuracy of untuned random forest classifier: {:0.2f}%'.format(acc1))
        feature_imp_df = pd.DataFrame(list_of_feature_imp)
        feature_imp_df.sort_values(by='imp', ascending=False, inplace=True)
        top_80_imp = []
        for i in range(len(feature_imp_df)):
            if np.sum(feature_imp_df['imp'].iloc[0:i+1]) < .8:
                top_80_imp.append(feature_imp_df['col'].iloc[i])
            else:
                pass
        rfc_imp_features.sort()
        top_80_imp.sort()
        return rfc_imp_features, top_80_imp
    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

def optimize_random_forest_params(Xt, yt):
    try:
        # Code for finding optimal random forest tuning found from folks at towarddatascience.com
        # https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74

        # Number of trees in random forest
        n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
        # Number of features to consider at every split
        max_features = ['auto', 'sqrt']
        # Maximum number of levels in tree
        max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
        max_depth.append(None)
        # Minimum number of samples required to split a node
        min_samples_split = [2, 5, 10]
        # Minimum number of samples required at each leaf node
        min_samples_leaf = [1, 2, 4]
        # Method of selecting samples for training each tree
        bootstrap = [True, False]
        # Create the random grid
        random_grid = {'n_estimators': n_estimators,
                       'max_features': max_features,
                       'max_depth': max_depth,
                       'min_samples_split': min_samples_split,
                       'min_samples_leaf': min_samples_leaf,
                       'bootstrap': bootstrap}

        rf = RandomForestClassifier(random_state=42)
        log.info('Parameters currently in use: \n{}'.format(rf.get_params()))
        rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=100, cv=10, verbose=2, random_state=42, n_jobs=-1)
        rf_random.fit(Xt, yt)
        log.info('The best paramters using random combinations are: \n'.format(rf_random.best_params_))
        best_random = rf_random.best_estimator_
        return best_random
    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

def find_opt_estimators(Xtr, ytr, Xts, yts):
    n_estimators = [int(x) for x in np.linspace(1, 200, 200)]
    acc_arr = []
    for i in range(len(n_estimators)):
        est_model = RandomForestClassifier(random_state=42, n_estimators=n_estimators[i])
        est_model.fit(Xtr, ytr)
        y_pred = np.array(est_model.predict(Xts)).reshape(len(Xts))
        y_target = np.array(yts).reshape(len(yts))
        acc_arr.append(metrics.accuracy_score(y_target, y_pred))
    sb.set_style('darkgrid')
    plt.plot(acc_arr)
    plt.show()

def find_opt_depth(Xtr, ytr, Xts, yts):
    max_depth = [int(x) for x in np.linspace(1, 50, 50)]
    acc_arr = []
    for i in range(len(max_depth)):
        dep_model = RandomForestClassifier(random_state=42, max_depth=max_depth[i])
        dep_model.fit(Xtr, ytr)
        y_pred = np.array(dep_model.predict(Xts)).reshape(len(Xts))
        y_target = np.array(yts).reshape(len(yts))
        acc_arr.append(metrics.accuracy_score(y_target, y_pred))
    sb.set_style('darkgrid')
    plt.plot(acc_arr)
    plt.show()

def create_opt_random_forest(Xt, yt):
    rfc = RandomForestClassifier(random_state=42, n_estimators=117, max_depth=9)
    rfc.fit(Xt, yt)
    return rfc

def evaluate_model(model, Xtest, ytest):
    try:
        # y_pred = np.array(forest.predict(Xt)).reshape(len(Xt))
        # y_target = np.array(yt).reshape(len(yt))
        predictions = np.array(model.predict(Xtest)).reshape(len(Xtest))
        targets = np.array(ytest).reshape(len(ytest))

        # Determine accuracy of model using confusion matrix and AUC
        y_target_s = pd.Series(targets, name="Actual")
        y_pred_s = pd.Series(predictions, name="Predicted")

        df_confusion = pd.crosstab(y_target_s, y_pred_s)
        log.info('\n{}'.format(df_confusion))
        accuracy = metrics.accuracy_score(targets, predictions)
        log.info('Accuracy: {:0.2f}%'.format(accuracy))
        fpr, tpr, thresholds = metrics.roc_curve(targets, predictions, pos_label=1)
        log.info('Accuracy of model using AUC metric = {:0.2f}'.format(metrics.auc(fpr, tpr)))

        # errors = abs(predictions - targets)
        # mape = 100 * np.mean(errors / targets)
        # accuracy = 100 - mape
        # log.info('Model Performance')
        # log.info('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
        # log.info('Accuracy: {:0.2f}%.'.format(accuracy))

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))

def show_ROC_curve(model, Xtest, ytest):
    # Plot ROC curve of model
    y_pred_proba = model.predict_proba(Xtest)[::, 1]
    fpr, tpr, _ = metrics.roc_curve(ytest, y_pred_proba)
    auc = metrics.roc_auc_score(ytest, y_pred_proba)
    plt.plot(fpr, tpr, label="data 1, auc=" + str(auc))
    plt.legend(loc=4)
    plt.show()

def scale_something(arr):
    scaler = preprocessing.StandardScaler().fit(arr.reshape(-1,1))
    arr_scaled = scaler.transform(arr)
    return arr_scaled

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
        spy_1_min_data = pd.read_csv('master_min_price_data.csv')
        unscaled_histogram(spy_1_min_data)
        # spy_1_min_data = pd.read_csv('SPY_prices_1min_2016_to_2018.csv')
        spy_1_min_data['date'] = spy_1_min_data.apply(convert_str_date, axis=1)
        # Split market data from premarket data and build array of first 60 minutes
        log.info('Compiling first 60 minutes of trading data for market hours...')
        spy_1_min_mkt_data, spy_1_min_premkt_data = split_nonmarket_data(spy_1_min_data)
        spy_1_min_mkt_arr_data = intraday_first_60min(spy_1_min_mkt_data)
        # spy_1_min_premkt_arr_data = make_premarket_array(spy_1_min_premkt_data)
        # spy_1_min_mkt_arr_data = intraday_min_ranges(spy_1_min_mkt_data)

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
        spy_1_day_data = pd.read_csv('master_day_price_data.csv')
        # spy_1_day_data = pd.read_csv('SPY_prices_1d_2016_to_2018.csv')
        spy_1_day_data['date'] = spy_1_day_data.apply(convert_str_date, axis=1)
        spy_1_day_df = spy_1_day_data[spy_1_day_data['date'] >= '2018-04-06'][['ticker', 'date', 'open', 'high', 'low', 'close', 'volume','class']]
        tickers = spy_1_day_df['ticker'].unique()
        for ticker in tickers:
            spy_1_day_df['open'] = np.where(spy_1_day_df.ticker==ticker, scale_something(spy_1_day_df['open'].values), spy_1_day_df['open'])
            spy_1_day_df['high'] = np.where(spy_1_day_df.ticker==ticker, scale_something(spy_1_day_df['high'].values), spy_1_day_df['high'])
            spy_1_day_df['low'] = np.where(spy_1_day_df.ticker==ticker, scale_something(spy_1_day_df['low'].values), spy_1_day_df['low'])
            spy_1_day_df['close'] = np.where(spy_1_day_df.ticker==ticker, scale_something(spy_1_day_df['close'].values), spy_1_day_df['close'])
            spy_1_day_df['volume'] = np.where(spy_1_day_df.ticker==ticker, scale_something(spy_1_day_df['volume'].values), spy_1_day_df['volume'])

        # Merge/join daily data with intraday arrays into single dataframe object
        spy_intraday_df = pd.merge(spy_1_min_mkt_arr_data, spy_1_day_df, how='left', on=['ticker','date'])
        # print(spy_intraday_df.head())
        spy_intraday_df.dropna(inplace=True)
        scaled_histogram(spy_intraday_df)
        # spy_intraday_df['premarket_min_closes'] = spy_intraday_df.apply(flatten_premarket, axis=1)
        spy_intraday_df['dayofweek'] = spy_intraday_df.apply(convert_to_weekday, axis=1)
        # boxplot of scaled pricing movement by day of week
        spy_intraday_df['etf'] = spy_intraday_df.apply(etf_yes_no, axis=1)
        spy_intraday_df.drop(['date'], axis=1, inplace=True)
        spy_intraday_bkup = spy_intraday_df.copy()

        # Display distribution and correlations between features
        show_distribution(spy_intraday_df)
        feature_correlations(spy_intraday_df)
        day_of_week_plot(spy_intraday_df)
        # log.info('Logging statistical description of merged dataframe: \n{}'.format(spy_intraday_df.describe()))

        # Define X and y from dataframe
        log.info('Assigning X and y variables...')
        y = spy_intraday_df[['class']]
        spy_intraday_df.drop(['class','ticker'], axis=1, inplace=True)
        X = spy_intraday_df

        # Split data into training and testing sets using 30% test size
        log.info('Creating train and test sets...')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        log.info('Length of X training set = {} records.'.format(len(X_train)))
        log.info('Length of X testing set = {} records.'.format(len(X_test)))
        log.info('Length of y training set = {} records.'.format(len(y_train)))
        log.info('Length of y testing set = {} records.'.format(len(y_test)))

        # Instantiate 1st random forest classifier and test accuracy
        log.info('Building 1st random forest with training data to filter by feature importance...')
        high_corr_features_over_03_1, high_corr_features_to_80_1 = create_random_forest(X_train, y_train)
        log.info('Features to keep from first pass of random forest over .03 importance: {}'.format(high_corr_features_over_03_1))
        log.info('Features to keep from first pass of random forest up to .80 total: {}'.format(high_corr_features_to_80_1))
        X_train_filtered_to_80_1 = X_train.filter(items=high_corr_features_to_80_1)
        X_test_filtered_to_80_1 = X_test.filter(items=high_corr_features_to_80_1)
        high_corr_features_over_03_2, high_corr_features_to_80_2 = create_random_forest(X_train_filtered_to_80_1, y_train)
        log.info('Features to keep from second pass of random forest over .03 importance: {}'.format(high_corr_features_over_03_2))
        log.info('Features to keep from second pass of random forest up to .80 total: {}'.format(high_corr_features_to_80_2))
        X_train_filtered_to_80_2 = X_train.filter(items=high_corr_features_to_80_2)
        X_test_filtered_to_80_2 = X_test.filter(items=high_corr_features_to_80_2)

        # Find optimal random forest parameters, make model into binary targets
        # best_estimators = optimize_random_forest_params(X_train, y_train)
        # find_opt_estimators(X_train, y_train, X_test, y_test) # peaks at roughly ~117 & ~184 estimators
        # find_opt_depth(X_train, y_train, X_test, y_test) # peaks at max depth 9
        final_df = spy_intraday_df.filter(items=high_corr_features_to_80_2)
        final_df['class'] = spy_intraday_bkup['class']
        final_df['ticker'] = spy_intraday_bkup['ticker']
        feature_correlations(final_df)
        final_df.replace([0,1,2,3],[0,0,1,1], inplace=True)
        y_train.replace([0,1,2,3],[0,0,1,1], inplace=True)
        y_test.replace([0,1,2,3],[0,0,1,1], inplace=True)

        # Building model using all features and determining AUC performance
        rfc_model = create_opt_random_forest(X_train, y_train)
        evaluate_model(rfc_model, X_test, y_test)
        show_ROC_curve(rfc_model, X_test, y_test)

        # Building model using optimal features and determining AUC performance
        rfc_model = create_opt_random_forest(X_train_filtered_to_80_2, y_train)
        evaluate_model(rfc_model, X_test_filtered_to_80_2, y_test)
        show_ROC_curve(rfc_model, X_test_filtered_to_80_2, y_test)

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass
