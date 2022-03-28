import pandas as pd

def extract_data():
    country_name_fr = [
        'Autriche', 'Belgique', 'Bulgarie', 'Croatie', 'Chypre', 'République tchèque', 'Danemark', 'Estonie',
        'Finlande', 'France', 'Allemagne', 'Grèce', 'Hongrie', 'Irlande', 'Italie', 'Lettonie', 'Lituanie',
        'Luxembourg', 'Malte', 'Pays-Bas', 'Pologne', 'Portugal', 'Roumanie', 'Slovaquie', 'Slovénie', 'Espagne',
        'Suède', 'Royaume-Uni'
    ]
    columns = ['eu', 'year', 'country', 'iso', 'gov_right1', 'gov_cent1', 'gov_left1', 'gov_right3', 'gov_cent3', 'gov_left3']

    df1 = pd.read_excel('./politique_mondiale.xlsx', usecols=columns, skipfooter=1, dtype={'year': int}).query('(eu == 1) & (year >= 2000)')
    df1 = df1.replace(df1['country'].unique().tolist(), country_name_fr)

    df2 = pd.read_excel('./inegalite_europe.xlsx', header=None, names=['country', 'def', 'pall', 'year', 'geni'], usecols=['country', 'year', 'geni'])

    return pd.merge(df1, df2)