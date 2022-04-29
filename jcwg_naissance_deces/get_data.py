from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import dateutil as du
import pandas as pd


def save_data_as_pkl(data, filename):
    data = urlopen(data)
    zipfile = ZipFile(BytesIO(data.read()))
    files = []
    with zipfile as f:
        for name in f.namelist():
            with f.open(name) as zd:
                files.append(pd.read_csv(zd, delimiter=';', dtype={
                    'DEPDOM': str}))
    db, _ = files
    df = db[
        ['ANAIS', 'MNAIS', 'AGEMERE', 'AGEPERE', 'DEPNAIS', 'NBENF', 'ORIGINOM',
         'SEXE']].copy()

    # df.groupby(['ANAIS', 'MNAIS']).mean()
    df['date'] = df.apply(lambda x: convert_date(x.ANAIS, x.MNAIS), axis=1)
    df = df.set_index('date')
    df.to_pickle('data/naissance-2019.pkl')
    # d_date = df.groupby('date').mean()
    # print(d_date[['AGEMERE', 'AGEPERE']])
    # d_date[['AGEMERE', 'AGEPERE']].plot()


def convert_date(y, m):
    return du.parser.parse(f"15-{m}-{y}")


if __name__ == '__main__':
    save_data_as_pkl('https://www.insee.fr/fr/statistiques/fichier/4768335'
                     '/etatcivil2019_nais2019_csv.zip', 'naissance-2019.pkl')
