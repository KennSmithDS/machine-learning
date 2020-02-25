import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import matplotlib.dates as mdt
import pprint
import json
import sys
import re
import os
import logging
import datetime
#nltk.download('stopwords')
#from nltk.tokenize import word_tokenize
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import statsmodels.formula.api as smf
from nltk import bigrams
from nltk.corpus import stopwords
import string
from bs4 import BeautifulSoup
from collections import Counter
import warnings

warnings.simplefilter("ignore")
pp = pprint.PrettyPrinter(indent=4)

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
    # capture warning messages
    logging.captureWarnings(capture=True)
    # Setup file logging
    if log_dir and log_file:
        fh = logging.FileHandler(os.path.join(log_dir, log_file))
        fh.setFormatter(log_format)
        logger.addHandler(fh)

    return logger

def read_json_file():
    log.info('Importing and merging Twitter stream output files')
    tweets=[]
    with open('tweet_output_020218.json', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            tweets.append(json.loads(line))
        file.close()
    with open('tweet_output_021318.json', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            tweets.append(json.loads(line))
        file.close()
    tweets = [tweet for tweet in tweets if len(tweet) > 1]
    log.info('After merging two test json files, there are {} rows of data.'.format(len(tweets)))
    # n = np.random.randint(1,1000)
    # pp.pprint(tweets[n])
    return tweets

def create_tweet_df(tweets):
    try:
        log.info('Converting JSON to dataframe and filtering paramters')
        tweet_data = pd.DataFrame()
        tweet_data['short_text'] = list(map(lambda tweet: tweet['text'], tweets))
        tweet_data['full_text'] = list(map(lambda tweet: tweet['extended_tweet']['full_text'] if 'extended_tweet' in tweet.keys() else '', tweets))
        tweet_data['created'] = list(map(lambda tweet: tweet['created_at'], tweets))
        tweet_data['source'] = list(map(lambda tweet: ahref_strip(tweet['source']), tweets))
        # tweet_data['source'] = tweet_data['source'].apply(ahref_strip())
        tweet_data['user'] = list(map(lambda tweet: tweet['user']['screen_name'], tweets))
        # tweet_data['country'] = list(map(lambda tweet: tweet['place']['country_code'] if 'place' in tweet.keys() else '', tweets))
        tweet_data['description'] = list(map(lambda tweet: tweet['user']['description'] if 'user' in tweet.keys() else '', tweets))
        tweet_data['location'] = list(map(lambda tweet: tweet['user']['location'] if 'user' in tweet.keys() else '', tweets))
        tweet_data['followers'] = list(map(lambda tweet: tweet['user']['followers_count'], tweets))
        tweet_data['listed'] = list(map(lambda tweet: tweet['user']['listed_count'], tweets))
        tweet_data['favourites'] = list(map(lambda tweet: tweet['user']['favourites_count'], tweets))
        tweet_data['statuses'] = list(map(lambda tweet: tweet['user']['statuses_count'], tweets))
        tweet_data['user_created'] = list(map(lambda tweet: tweet['user']['created_at'], tweets))
        tweet_data['user_timezone'] = list(map(lambda tweet: tweet['user']['time_zone'], tweets))
        # tweet_data['tweet_replies'] = list(map(lambda tweet: tweet['reply_count'] if tweet['reply_count'] != None else '', tweets))
        # tweet_data['tweet_retweets'] = list(map(lambda tweet: tweet['retweet_count'] if tweet['retweet_count'] != None else '', tweets))
        # tweet_data['tweet_favourites'] = list(map(lambda tweet: tweet['favorite_count'] if tweet['favorite_count'] != None else '', tweets))
        return tweet_data
    except Exception as e:
        log.error('Error on line: {} - Error type: {} - Error code: {}'.format((sys.exc_info()[-1].tb_lineno), type(e), e))
        pass

def create_regex_compilers():
    # tweet preprocessing code credit given to Marco Bonzanini
    # https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

    emoticons_str = r"""
    (?:
        [:=;] # eyes
        [oO0\-] # nose
        [D\)\]\(\]/\\OpP] #mouth
    )"""

    regex_str = [
        emoticons_str,
        r'<[^>]+>',  # HTML tags
        r'(?:@[\w_]+)',  # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
        r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
        r'(?:[\w_]+)',  # other words
        r'(?:\S)'  # anything else
    ]

    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    return tokens_re, emoticon_re

def ahref_strip(text):
    soup = BeautifulSoup(text, 'lxml')
    cleaned = soup.get_text()
    return cleaned

def remove_stops(lst):
    punctuation = list(string.punctuation)
    noise = ['like', 'follow', 'retweet', 'RT', 'giveaway', 'enter', '…']
    stop = stopwords.words('english') + punctuation + ['rt', 'via']
    no_stops = [term for term in lst if term not in stop]
    no_noise = [term for term in no_stops if term not in noise]
    return no_noise

def tokenize(str, tokenizer):
    return tokenizer.findall(str.lower())

def preprocess(str, lowercase=False):
    tokenizer, emoticonizer = create_regex_compilers()
    tokens = tokenize(str, tokenizer)
    if lowercase:
        tokens = [token if emoticonizer.search(token) else token.lower() for token in tokens]
    return tokens

def get_bigrams(lst):
    bigram_obj = bigrams(lst)
    bigram_lst = [bigram for bigram in bigram_obj]
    return bigram_lst

def token_unit_test():
    test_tweet = '#btcusd #imrichbitch this market is crazy right meow! :-D'
    tokens = preprocess(test_tweet)
    #log.info('Unit test output as follows: {}'.format(tokens))
    assert isinstance(tokens, list)

def clean_tweet_date(row):
    dt = datetime.datetime.strptime(row['created'], "%a %b %d %H:%M:%S +0000 %Y")
    tweet_date = dt.date()
    return tweet_date

def clean_tweet_time(row):
    dt = datetime.datetime.strptime(row['created'], "%a %b %d %H:%M:%S +0000 %Y")
    tweet_time = dt.time().hour
    return tweet_time

def clean_price_date(row):
    clean_date = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %I-%p').date()
    return clean_date

def clean_price_time(row):
    time = datetime.datetime.strptime(row['Date'], '%Y-%m-%d %I-%p')
    return time.hour

def float_convert(x):
    return x.astype(float)

def clean_and_modify(df):

    try:
        log.info('Cleaning Bitcoin pricing dataframe')

        # Remove top two rows and reset index, then delete it
        df = df.ix[2:]
        df.reset_index(inplace=True)
        del df['index']

        # Apply function to make date field into datetime
        df['Dates'] = df.apply(clean_price_date, axis=1)
        df['Hours'] = df.apply(clean_price_time, axis=1)

        # Reset the index to the date field
        df.set_index(['Dates', 'Hours'], inplace=True)
        df.sort_index(ascending=True, inplace=True)

        # Drop rows with Nan values
        df.dropna()

        # Convert strings to floats for all pricing values
        df[['Open', 'High', 'Low', 'Close', 'Volume From', 'Volume To']] = df[['Open', 'High', 'Low', 'Close', 'Volume From', 'Volume To']].apply(float_convert, axis=1)

        # Create new fields for change and percent change in value between closing price of each period, and difference between open and close of each period
        df['Change_Close'] = df.Close.diff()
        df['Perc_Change_Close'] = df.Close.pct_change()
        df['Change_Open_Close'] = df['Close'] - df['Open']
        df['Perc_Change_Open_Close'] = df['Change_Open_Close']/df['Open']
        df['Abs_Price_Change'] = abs(df['Change_Close'])

        # Reduce size of dataframe output to range that matches tweet data
        df = df.loc['2018-01-31':'2018-02-13']
        df = df[['Open', 'High', 'Low', 'Close', 'Volume From', 'Volume To', 'Change_Close', 'Perc_Change_Close', 'Change_Open_Close', 'Perc_Change_Open_Close','Abs_Price_Change']]

        return df

    except Exception as e:
        log.error('Error on line {}, error type {}, error code {}'.format((sys.exc_info()[-1].tb_lineno), type(e).__name__, e))
        pass

def get_btc_data():
    btc_price_data = pd.read_csv('http://www.cryptodatadownload.com/cdd/Bittrex_BTCUSD_1h.csv', header=None, names=['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume From', 'Volume To'])
    log.info('Successfully fetched Bitcoin pricing data, {} rows in total.'.format(len(btc_price_data)))
    btc_price_clean = clean_and_modify(btc_price_data)
    return btc_price_clean

def correlation_heat_map(df):
    f, ax = plt.subplots(figsize=(10, 8))
    df_corr = df.corr()
    sb.heatmap(df_corr, square=True, ax=ax, annot=True)
    plt.xticks(rotation=45)
    plt.yticks(rotation=45)
    plt.show()

    #sb.pairplot(df, diag_kind='kde', palette='husl', markers="+", plot_kws=dict(s=25, edgecolor="b", linewidth=.5), diag_kws=dict(shade=True))
    #plt.show()

def build_linear_ols_model(df):
    log.info('Creating linear regression with OLS model with only comparing closing price to tweet volume')
    estimation = smf.ols(formula='Abs_Price_Change ~ Tweet_Count', data=df).fit()
    summary = estimation.summary()
    log.info('Printing summary of OLS model results\n{}'.format(summary))
    log.info('R2: {}'.format(estimation.rsquared))
    log.info('Standard errors:\n{}'.format(estimation.bse))

    # Make predictions from the model
    prediction = estimation.predict(df[['Tweet_Count']])

    # Interpret the output parameters - intercept and slopes, as well as r-squared values
    log.info('Here is the parameter output (intercept and slope) for OLS model\n{}'.format(estimation.params))
    intercept, slope = round(estimation.params, 5)
    log.info('Formula for line of best fit is: y = {}x + {}'.format(slope, intercept))

    return prediction

def build_multilinear_ols_model_all_features(df):
    log.info('Creating multi-linear regression with OLS model using all features')
    estimation = smf.ols(formula='Tweet_Count ~ Open + High + Low + Close + Volume_From + Volume_To + Perc_Change_Close + Change_Open_Close + Perc_Change_Open_Close + Change_Close + Abs_Price_Change', data=df).fit()
    summary = estimation.summary()
    log.info('Printing summary of OLS model results\n{}'.format(summary))
    log.info('R2: {}'.format(estimation.rsquared))
    log.info('Standard errors:\n{}'.format(estimation.bse))

    # Make predictions from the model
    prediction = estimation.predict(df[['Open', 'High', 'Low', 'Close', 'Volume_From', 'Volume_To', 'Perc_Change_Close', 'Change_Open_Close', 'Perc_Change_Open_Close', 'Change_Close', 'Abs_Price_Change']])

    # Interpret the output parameters - intercept and slopes, as well as r-squared values
    log.info('Here is the parameter output (intercept and slopes) for OLS model\n{}'.format(estimation.params))
    intercept, slope_a, slope_b, slope_c, slope_d, slope_e, slope_f, slope_g, slope_h, slope_i, slope_j, slope_k = round(estimation.params, 5)
    log.info('Formula for line of best fit is: y = {}x + {}x + {}x + {}x + {}x + {}x + {}x + {}x + {}x + {}x + {}x + {}'.format(slope_a, slope_b, slope_c, slope_d, slope_e, slope_f, slope_g, slope_h, slope_i, slope_j, slope_k, intercept))

    return prediction

def build_multilinear_ols_model_selected_features(df):
    log.info('Creating multi-linear regression with OLS model using selected best K features')
    estimation = smf.ols(formula='Tweet_Count ~ Volume_From + Volume_To + Abs_Price_Change', data=df).fit()
    summary = estimation.summary()
    log.info('Printing summary of OLS model results\n{}'.format(summary))
    log.info('R2: {}'.format(estimation.rsquared))
    log.info('Standard errors:\n{}'.format(estimation.bse))

    # Make predictions from the model
    prediction = estimation.predict(df[['Volume_From','Volume_To','Abs_Price_Change']])

    # Interpret the output parameters - intercept and slopes, as well as r-squared values
    log.info('Here is the parameter output (intercept and slopes) for OLS model\n{}'.format(estimation.params))
    intercept, slope_a, slope_b, slope_c = round(estimation.params, 5)
    log.info('Formula for line of best fit is: y = {}x + {}x + {}x + {}'.format(slope_a, slope_b, slope_c, intercept))

    return prediction

def find_bestK(df):
    try:
        array = df.values
        X = array[:,1:12]
        y = array[:,0:1]
        y = y.astype('int')
        test = SelectKBest(score_func=chi2, k=2)
        fit = test.fit(X, y)
        log.info('Feature selection scores using chi2 test:\n{}'.format(fit.scores_))
        new_X = SelectKBest(chi2, k=3).fit_transform(X, y)
        log.info('Selecting three best features.')
        return new_X
    except Exception as e:
        log.error('Error on line: {} - Error type: {} - Error code: {}'.format((sys.exc_info()[-1].tb_lineno), type(e), e))
        pass

def get_mse_value(actual,predicted):
    log.info('Calculating the residual error between predicted and actual values, before squaring the errors, and finding the mean squared error.')
    y_residuals = np.array(actual) - np.array(predicted.values.reshape(207, 1))
    sq_errors = [x ** 2 for x in y_residuals]
    records = len(actual)
    mse = round(np.sum(sq_errors) / records, 5)
    log.info('The mean-squared error of the model is {}'.format(mse))

def show_actual_vs_predicted_scatter(df):
    sb.lmplot(x='Tweet_Count', y='Close', data=df)
    plt.xlabel('Tweets with BTC hashtags')
    plt.ylabel('Closing Price')
    plt.title('Tweet Volume vs Closing Price')
    plt.show()

    # sb.lmplot(x='Tweet_Count', y='linear_price_predictions', data=df)
    # plt.xlabel('Tweets with BTC hashtags')
    # plt.ylabel('Predicted Closing Price')
    # plt.title('Tweet Volume vs Predicted Closing Price')
    # plt.show()

if __name__ == "__main__":
    # Setup directories
    logging_dir = 'logs'
    time_date = datetime.datetime.now()
    string_date = time_date.strftime("%Y%m%d_%H%M%S")

    # Setup Logging
    logging_level = logging.INFO
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    logging_file = 'crypto_tweets_{}.log'.format(string_date)
    log = setup_logger(logging_dir, logging_file, log_level=logging_level)

    try:
        # Import twitter stream output file to dataframe
        json_data = read_json_file()

        # Convert JSON data file to Pandas dataframes
        tweet_df = create_tweet_df(json_data)

        # Run unit test for token preprocessing
        log.info('Running unit test on token preprocesser')
        token_unit_test()

        # Tokenize short text parameter of each tweet
        tweet_df['tokens'] = tweet_df['short_text'].apply(preprocess)

        # Remove stop words for english punctuation
        tweet_df['tokens'] = tweet_df['tokens'].apply(remove_stops)

        # Count term frequency in unigrams
        count_all = Counter()
        for tokens in tweet_df['tokens']:
            count_all.update(tokens)
        log.info('Most common tokens after removing stop words are {}'.format(count_all.most_common(5)))

        # Count term frequency in bigrams
        tweet_df['bigrams'] = tweet_df['tokens'].apply(get_bigrams)
        count_bigrams = Counter()
        for bigram in tweet_df['bigrams']:
            count_bigrams.update(bigram)
        log.info('Most common bigrams after removing stop words are {}'.format(count_bigrams.most_common(5)))

        # Run function to clean tweet created string and set index to date and time values
        tweet_df['Dates'] = tweet_df.apply(clean_tweet_date, axis=1)
        tweet_df['Hours'] = tweet_df.apply(clean_tweet_time, axis=1)
        tweet_df.set_index(['Dates', 'Hours'], inplace=True)
        tweet_df.sort_index(ascending=True, inplace=True)

        # Narrowing date range to exclude dates with minimal observations
        tweet_df = tweet_df.loc['2018-01-31':'2018-02-13']

        # Filtering tweet_df values to only tweets with Bitcoin related hashtags/tokens
        btc_tags = ['btc', '#btc', '#bitcoin', 'bitcoin', 'btcusd', '#btcusd']
        btc_df = tweet_df[tweet_df.tokens.apply(lambda x: pd.Series(x).isin(btc_tags).any())]

        # Scale data using min max scaler
        scaler = MinMaxScaler()

        # Group Bitcoin dataframe by size/count of tweets for each hour/day
        btc_grouped_tweets = pd.DataFrame(btc_df.groupby(['Dates', 'Hours']).size())
        btc_grouped_tweets.columns = ['Tweet_Count']
        #btc_grouped_tweets[['Tweet_Count']] = scaler.fit_transform(btc_grouped_tweets[['Tweet_Count']])

        # Import Bitcoin price data from cryptodatadownload.com
        btc_price_data = get_btc_data()

        # Visualize the pricing data using a heatmap for day and hour
        btc_price_to_pivot = btc_price_data[['Abs_Price_Change']]
        btc_price_to_pivot.reset_index(inplace=True)
        btc_price_to_pivot.columns = ['Dates', 'Hours', 'Abs_Price_Change']
        btc_price_pivot = btc_price_to_pivot.pivot('Hours', 'Dates', 'Abs_Price_Change')
        f, ax = plt.subplots(figsize=(9, 6))
        sb.heatmap(btc_price_pivot, annot=True, fmt='.2f', linewidths=.5, ax=ax)
        plt.xticks(rotation=45)
        plt.show()

        # Scale the price data using MinMaxScaler
        btc_price_data[['Open', 'High', 'Low', 'Close']] = scaler.fit_transform(btc_price_data[['Open', 'High', 'Low', 'Close']])
        btc_price_data[['Volume From', 'Volume To']] = scaler.fit_transform(btc_price_data[['Volume From', 'Volume To']])
        btc_price_data[['Change_Close', 'Change_Open_Close', 'Abs_Price_Change']] = scaler.fit_transform(btc_price_data[['Change_Close', 'Change_Open_Close', 'Abs_Price_Change']])
        btc_price_data[['Perc_Change_Close', 'Perc_Change_Open_Close']] = scaler.fit_transform(btc_price_data[['Perc_Change_Close', 'Perc_Change_Open_Close']])

        # Merging twitter counts and pricing data to single dataframe
        btc_merged_data = pd.merge(btc_grouped_tweets, btc_price_data, left_index=True, right_index=True)
        btc_merged_data.columns = ['Tweet_Count', 'Open', 'High', 'Low', 'Close', 'Volume_From', 'Volume_To', 'Perc_Change_Close', 'Change_Open_Close', 'Perc_Change_Open_Close', 'Change_Close', 'Abs_Price_Change']

        # Visualize correlation between features
        correlation_heat_map(btc_merged_data)

        # Build linear regression models
        btc_merged_data['linear_price_predictions'] = build_linear_ols_model(btc_merged_data)
        btc_merged_data['multilinear_price_predictions'] = build_multilinear_ols_model_all_features(btc_merged_data)
        best_features = find_bestK(btc_merged_data)
        btc_selected_features = btc_merged_data[['Tweet_Count', 'Volume_From', 'Volume_To', 'Abs_Price_Change']]
        multilinear_price_predictions_f_selected = build_multilinear_ols_model_selected_features(btc_selected_features)
        log.info('Selecting features with best K value using chi2 test did not improve model predictive capability at all, in fact it lowered the r^2.')

        # Calculate the MSE of the model
        actuals = btc_selected_features['Tweet_Count']
        get_mse_value(actuals, multilinear_price_predictions_f_selected)
        show_actual_vs_predicted_scatter(btc_merged_data)

        # Write dataframe to csv file format
        # log.info('Writing tweet dataset to csv file.')
        # tweet_df.to_csv('tweet_output_{}.csv'.format(string_date), index=False)

    except Exception as e:
        log.error('Error on line: {} - Error type: {} - Error code: {}'.format((sys.exc_info()[-1].tb_lineno), type(e), e))
        pass