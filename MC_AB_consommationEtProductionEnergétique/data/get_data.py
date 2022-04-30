import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    usecols = ['siec', 'unit', 'geo', 'TIME_PERIOD', 'OBS_VALUE']
    prod_cons = pd.read_csv('data/resources/conso_production_petrole.csv', usecols=usecols)
    prod_cons = df[df.unit != "NR"]
    prod_cons = df[df.OBS_VALUE != 0]
    export = pd.read_csv('data/resources/export_petrole.csv', usecols=usecols)
    export = df[df.unit != "NR"]
    export = df[df.OBS_VALUE != 0]
    impor = pd.read_csv('data/resources/import_petrole.csv', usecols=usecols)
    impor = df[df.unit != "NR"]
    impor = df[df.OBS_VALUE != 0]
    return prod_cons, export, impor


def get_by_country(data, country):
    return data[data.geo == country]

def get_by_energy(data, energy):
    return data[data.siec == energy]


def list_countries(data):
    return data['geo'].unique()

def sum_energies(data):
    return data["OBS_VALUE"].sum()

def plot_evolution(data):
    data.plot(x='TIME_PERIOD', y='OBS_VALUE', kind='line')
    plt.show()


def clear_unique_values(data):
    nunique = data.nunique()
    cols_to_drop = nunique[nunique == 1].index
    return data.drop(cols_to_drop, axis=1)

if __name__ == '__main__':
    data = get_data()
    FR = get_by_country(data, "FR")
    FR_RA000 = get_by_energy(FR, "RA000")
    unit = FR_RA000['unit'].unique()[0]
    print(str(sum_energies(FR_RA000)) + " " + str(unit))
    FR_cleaned = clear_unique_values(FR_RA000)
    FR_cleaned.reset_index(drop=True, inplace=True)
    plot_evolution(FR_cleaned)