import pandas as pd
import numpy as np


def get_sondage_tour_1():
    df = pd.read_csv('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv')
    df.drop(['id', 'echantillon', 'erreur_sup', 'sous_echantillon', 'commanditaire',
             'erreur_inf', 'population', 'rolling', 'media', 'parti'], axis=1, inplace=True)
    df = df[df['nom_institut'] == 'Ipsos']
    df["hypothese"].replace(np.nan, "tous", inplace=True)
    df = df[(df['hypothese'] == "tous") & (df['tour'] == "Premier tour")]
    df.reset_index()
    df['date_enquete'] = pd.to_datetime(df['fin_enquete'])
    df = df[df['tour'] == "Premier tour"]
    df = df.sort_values(by="date_enquete")
    df.to_csv('sondages_tour_1.csv')


def get_sondage_tour_2():
    df = pd.read_csv('https://raw.githubusercontent.com/nsppolls/nsppolls/master/presidentielle.csv')

    df.drop(['parti', 'id', 'commanditaire', 'debut_enquete', 'population', 'rolling', 'media', 'sous_echantillon'],
            axis=1, inplace=True)
    df = df[df['tour'] == "Deuxième tour"]
    df.replace("Hypothèse Macron", "Hypothèse Macron / Le Pen", inplace=True)
    df.replace("Hypothèse Le Pen / Macron", "Hypothèse Macron / Le Pen", inplace=True)
    df.replace(np.nan, "Hypothèse Macron / Le Pen", inplace=True)
    df.reset_index(inplace=True)
    df = df[df["hypothese"] == "Hypothèse Macron / Le Pen"]
    df['date_enquete'] = pd.to_datetime(df['fin_enquete'])
    df_ifop = df[df['nom_institut'] == 'Ifop']
    df_ifop = df_ifop.sort_values(by="date_enquete")
    df_ifop.to_csv('sondages_tour_2.csv')

def




if __name__ == '__main__':
    get_sondage_tour_1()
    get_sondage_tour_2()