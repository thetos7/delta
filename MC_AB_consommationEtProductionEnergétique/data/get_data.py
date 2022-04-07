import pandas as pd


def get_data():
    usecols = ['siec', 'unit', 'geo', 'TIME_PERIOD', 'OBS_VALUE']
    df = pd.read_csv('conso_energie_renouvelable.csv', usecols=usecols)
    df = df[df.unit != "NR"]
    df = df[df.OBS_VALUE != 0]
    return df


if __name__ == '__main__':
    print(get_data())
