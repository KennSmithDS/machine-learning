import os
import datetime as dt
import pandas as pd
from datetime import datetime, timedelta

def get_date_cmd(this_date):
    prev_day = this_date - timedelta(days=1)
    this_month = prev_day.month
    this_day = prev_day.day
    this_year = prev_day.year
    command = f"scrapy crawl prnews --logfile prnews_printout.log -o prnews_archive_{this_year}_{this_month}_{this_day}.json -a pr_year={this_year} -a pr_month={this_month} -a pr_day={this_day}"
    return command

# date_list = pd.date_range(start="2016-01-01", end="2020-04-27").tolist()
date_list = pd.date_range(start="2020-04-27", end="2020-04-29").tolist()
for this_date in reversed(date_list):
    str_date = this_date.strftime('%Y_%m_%d%H%M')
    print(f'Getting scrapy command sequence for {str_date}')
    scrapy_cmd = get_date_cmd(this_date)
    print(scrapy_cmd)
    os.system(scrapy_cmd)