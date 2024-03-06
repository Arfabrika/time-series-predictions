import pandas as pd
import json

def loadData(path):
    return pd.read_csv(path)

def loadConfig(path):
    f = open(path, 'r')
    return json.loads(f.read())