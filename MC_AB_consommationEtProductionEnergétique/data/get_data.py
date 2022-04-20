import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    usecols = ['siec', 'unit', 'geo', 'TIME_PERIOD', 'OBS_VALUE']
    df = pd.read_csv('conso_energie_renouvelable.csv', usecols=usecols)
    df = df[df.unit != "NR"]
    df = df[df.OBS_VALUE != 0]
    return df


def get_by_country(data, country):
    return data[data.geo == country]

def get_by_energy(data, energy):
    return data[data.siec == energy]

def list_energies(data):
    return data['siec'].unique()

def list_countries(data):
    return data['geo'].unique()

def sum_energies(data):
    return data["OBS_VALUE"].sum()

def plot_evolution(data):
    data.plot(x='TIME_PERIOD', y='OBS_VALUE', kind='line')
    plt.show()

    #data = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
    #    'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
    #   }
    #df = pd.DataFrame(data,columns=['Year','Unemployment_Rate'])
    #df.plot(x ='Year', y='Unemployment_Rate', kind = 'line')
    #plt.show()

def clear_unique_values(data):
    nunique = data.nunique()
    cols_to_drop = nunique[nunique == 1].index
    return data.drop(cols_to_drop, axis=1)

if __name__ == '__main__':
    data = get_data()
    FR = get_by_country(data, "FR")
    FR_E7000 = get_by_energy(FR, "E7000")
    unit = FR_E7000['unit'].unique()[0]
    print(str(sum_energies(FR_E7000)) + " " + str(unit))
    FR_cleaned = FR_E7000#clear_unique_values(FR_E7000)
    print(FR_cleaned[FR_cleaned.TIME_PERIOD == 2004])
    plot_evolution(FR_cleaned.nunique())