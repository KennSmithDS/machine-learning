from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import sys
import numpy as np

data = pd.read_csv('mpu_pred.csv', sep=',')
data.fillna(0, inplace=True)

def remove_whitespace(value):
    return str(value).replace(" ","").lower()

def convert_to_dummies(data):
    scac_dummies = pd.get_dummies(data['scac'], prefix='scac')
    comm_dummies = pd.get_dummies(data['commodities'], prefix='commodity')
    model_data = data[\
        ['events_ran', 'po_to_ship', 'location_count', 'vendor_age', 'isior', 'peak', 'routed_day', 'routed_hour',\
         'request_day', 'min_request_hour', 'max_request_hour', 'route_to_pickup', 'request_window', 'pos', 'cartons',\
         'weight', 'units', 'pallets', 'fak', 'ft3', 'vendor_density', 'msa', 'lsa_flag', 'zps_flag',\
         'fc', 'lat', 'long', 'units_per_day', 'pos_per_day', 'asns_per_day', 'events_per_day', 'units_per_po',\
         'pos_per_asn', 'units_per_asn', 'MPU']]
    model_data = model_data.join(scac_dummies.loc[:, 'scac_2':])
    model_data = model_data.join(comm_dummies.loc[:, 'commodity_2':])
    return model_data

def show_correlations(data):
    corr = data.corr()
    corr.to_csv('model_correlations.csv')
    fig, ax = plt.subplots(figsize=(20, 20))
    sb.heatmap(data=corr, ax=ax)
    plt.interactive(False)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()

def split_train_test(data):
    y = data[['MPU']]
    X = data.drop(['MPU'], axis=1)
    print(len(y))
    print(len(X))
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    return X_train, X_test, y_train, y_test

def build_random_forest(x, y, estimators, depth):
    classifier = RandomForestClassifier(n_estimators=estimators, max_depth=depth, random_state=0)
    #x = np.ravel(x)
    #y = np.ravel(y)
    classifier.fit(x, y)
    print(classifier.feature_importances_)
    return classifier

try:
    data['commodities'] = data['commodities'].apply(remove_whitespace)
    model_data = convert_to_dummies(data)
    #show_correlations(model_data)
    X_train, X_test, y_train, y_test = split_train_test(model_data)
    estimators = 100
    depth = 6
    randomforest = build_random_forest(X_train, y_train, estimators, depth)
    scores = cross_val_score(randomforest, X_test, y_test)
    print('Mean Standard Error of RandomForest: ',scores.mean())

except Exception as e:
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)