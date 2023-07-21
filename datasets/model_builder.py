import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
import pickle
import os

google_sheets_url = os.getenv('PUBLIC_GSHEETS_URL')
file_name = 'ss4_urban'

def fetch():

    if google_sheets_url:
        def load_data(sheets_url, save_path):
            csv_url = sheets_url.replace('/edit#gid=', '/export?format=csv&gid=')
            df = pd.read_csv(csv_url)
            df.to_csv(save_path, index=False)
            
        load_data(google_sheets_url, 'datasets/' + file_name + '.csv')
    
    train()

def train():
    students = pd.read_csv('datasets/' + file_name + '.csv')

    df = students.copy()
    target = 'attacker_won'

    df['a5'] = np.where(df['a5'] < df['a6'], df['a5'] + '+' + df['a6'], df['a6'] + '+' + df['a5'])
    df['d5'] = np.where(df['d5'] < df['d6'], df['d5'] + '+' + df['d6'], df['d6'] + '+' + df['d5'])

    columns_to_drop = [target, 'a6', 'd6']
    X = df.drop(columns_to_drop, axis=1)
    Y = df[target]

    clf = CatBoostClassifier(cat_features=['a1','a2','a3','a4','a5','d1','d2','d3','d4','d5'], iterations=1000)
    clf.fit(X, Y)

    pickle.dump(clf, open('datasets/' + file_name + '_clf.pkl', 'wb'))

if not os.path.exists('datasets/' + file_name + '.csv') or not os.path.exists('datasets/' + file_name + '_clf.pkl'):
    fetch()
