import requests, json
import pandas as pd
import datetime as dt
from datetime import timezone, timedelta, time
from credentials import client_id
import re, sys, os, time

class EquityPriceHistory():

    def __init__(self, ticker, periodType, period, frequencyType, frequency, startDate, endDate, needExtendedHoursData):
        self.apikey = client_id
        self.ticker = ticker
        self.periodType = periodType
        self.period = period
        self.frequencyType = frequencyType
        self.frequency = frequency
        self.startDate = startDate
        self.endDate = endDate
        self.extendedHours = needExtendedHoursData
        self.requestUrl = f'https://api.tdameritrade.com/v1/marketdata/{self.ticker}/pricehistory'

    def getPayload(self):
        # need to devise a way to customize the payload based on request time, e.g. daily within 10 year time range, or hourly/minute/etc.
        payload = {
            'apikey': self.apikey,
            'periodType': self.periodType,
            # 'period': self.period,
            'frequencyType': self.frequencyType,
            # 'frequency': self.frequency,
            'startDate': self.startDate,
            'endDate': self.endDate,
            # 'needExtendedHoursData': self.extendedHours
        }
        return payload

    def makeRequest(self):
        try:
            response_content = requests.get(url=self.requestUrl, params=self.getPayload())

            if response_content.status_code == 200:
                print('Request successful')
                json_data = response_content.json()
                bars = pd.DataFrame(json_data['candles'])
            else:
                print(f'Request failed: {response_content.status_code}')
                bars = pd.DataFrame()

            return bars

        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), e)
            pass

class EquityQuotes():
    pass

class OptionChainRequest():
    pass

def getYearEpochTimeRange(startYear, endYear):
    epochRange = []

    for year in range(startYear, endYear+1):
        yearStart = dt.date(year, 1, 1)
        yearEnd = dt.date(year, 12, 31)
        # print(startingDate)

        yearStartDt = dt.datetime.combine(yearStart, dt.time())
        yearEndDt = dt.datetime.combine(yearEnd, dt.time())
        # print(startingDatetime)

        startingEpoch = datetimeToEpoch(yearStartDt)
        endingEpoch = datetimeToEpoch(yearEndDt)
        # print(startingEpoch)

        epochRange.append([startingEpoch, endingEpoch])

    return epochRange

def getDayEpochTimeRange(startDate, endDate):
    dateRange = pd.to_datetime(pd.date_range(startDate, endDate, freq='D').to_series(), unit='s')
    weekdayList = [date for date in dateRange if date.weekday() != 0 and date.weekday() != 6]

    # epochRange = []

    #
    # startDt = dt.datetime.combine(startDate, dt.time())
    # startEpoch = datetimeToEpoch(startDt)
    # print(startEpoch)
    #
    # endDt = dt.datetime.combine(endDate, dt.time())
    # endEpoch = datetimeToEpoch(endDt)
    # print(endEpoch)
    #
    # for day in dateRange:
    #     print(day)
    #
    # return epochRange

    return weekdayList

def datetimeToEpoch(dateTime):
    return int((dateTime - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)

def epochToDate(epochInt):
    return dt.datetime.fromtimestamp(epochInt/1000, timezone.utc).strftime('%Y-%m-%d')

# 631184400000 1/1/1990 midnight
# 662677199000 12/31/1990 midnight
# 728287200000 first epoch available 1/19/1993
# '1262354268000', '15851157690000' 1/1/2010 to 3/25/2020

if __name__ == '__main__':
    try:
        timeRange = getYearEpochTimeRange(1993, 2020)

        masterHistoryDF = pd.DataFrame()
        equity = 'SPY'
        pt = 'day'
        p = '5'
        ft = 'minute'
        f = '1'
        preMarket = 'true'

        # startEpoch, endEpoch = getDayEpochTimeRange('2020-01-01', '2020-3-25')

        dateList = getDayEpochTimeRange('2020-01-01', '2020-3-25')

        # spyHistory = EquityPriceHistory(equity, pt, p, ft, f, f'{startEpoch}', f'{endEpoch}', preMarket)
        # priceData = spyHistory.makeRequest()
        # print(priceData.tail())

        # BELOW FETCHES ALL DAILY PRICE DATA AVAILABLE BETWEEN START AND END YEAR
        # for pair in timeRange:
        #     print(f'Requesting price history between {epochToDate(pair[0])} and {epochToDate(pair[1])}')
        #
        #     spyHistory = EquityPriceHistory(equity, pt, p, ft, f, f'{pair[0]}', f'{pair[1]}', preMarket)
        #     priceData = spyHistory.makeRequest()
        #     priceData['datetime_epoch'] = priceData['datetime']
        #     priceData['datetime'] = priceData['datetime'].apply(lambda x: epochToDate(x))
        #
        #     if not priceData.empty:
        #         masterHistoryDF = pd.concat([masterHistoryDF, priceData])
        #
        #     time.sleep(2)
        #
        # masterHistoryDF.to_csv(f'{equity}_history_test.csv', index=False)

    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), e)
        pass