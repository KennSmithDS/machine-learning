United Nations Millennium Development Goals

**NOTE: I only began work on this project a week ago, so it is a living project and will add to it in coming weeks!  Project deadline is in late March 2020.**

Jupyter Notebook Description:

1) mdg_data_exploration.ipynb - this is a notebook I created to start performing data exploration.

Training data:
We've aggregated their data from 1972-2007 on over 1200 macroeconomic indicators in 214 countries around the world. A random snapshot of the data looks like the below. Each row represents a timeseries for a specific indicator and country. The row has an id, a country name, a series code, a series name, and data for the years 1972 - 2007.

Prediction data and submission format
We're not interested in predicting all of these timeseries--just the ones that are relevant to the Millenium Development Goals. There are a set of indicators from the World Bank dataset that represent our progress towards these goals. We're withholding the names and codes of the World Bank indicators we want to predict, since the data is readily available publicly. However, these all have a series code labeled with the MDG goal and sub-goal we are interested in (e.g., 1.2 or 3.1).

We've also taken the subset of predictions that we can reliably make. We first made sure that we only looked at goals where we had true measures to compare them against in the forecast years (2008, 2012). We also removed rows that didn't have any data before 2008, since these will be impossible to predict.

Project Website:
https://www.drivendata.org/competitions/1/united-nations-millennium-development-goals/

Data Source:
https://s3.amazonaws.com/drivendata/data/1/public/cd238763-ed29-4a46-8584-f9334d57ec94.zip