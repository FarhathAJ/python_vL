import pandas as pd;
import json;

def import_data():
    df = pd.read_csv(r'inputdf.csv')
    df.to_json(r'templates\static\impdatajson.json', orient="records")