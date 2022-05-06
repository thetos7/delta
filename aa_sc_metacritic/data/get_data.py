import pandas as pd

def get_data():
    data = pd.read_csv("vgcritics.csv")
    data = data.loc[(data.critics > 5) & (data.genre != "No info")]
    return data
