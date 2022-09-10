import pandas as pd

def preprocess(data, reg_data):
    # Filtering Summer Olympics
    data = data.merge(reg_data, on='NOC', how='left')
    data = data[data['Season'] == 'Summer']
    data.drop_duplicates(inplace=True)
    data = pd.concat([data, pd.get_dummies(data['Medal'])], axis=1)
    return data

