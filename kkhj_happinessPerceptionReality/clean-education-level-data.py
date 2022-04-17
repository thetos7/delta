import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_means():
    df = pd.read_csv("data/educationLevel.csv")
    mask = (df['TIME'] >= 2012) & (df['TIME'] <= 2021)
    df = df[mask]
    df = (df.groupby(['LOCATION', 'TIME'], as_index=False))["Value"].mean()
    return df

if __name__ == "__main__":
    get_means()