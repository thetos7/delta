import pandas as pd

df = pd.read_csv('https://www.insee.fr/fr/statistiques/fichier/4768335'
                 '/etatcivil2019_nais2019_csv.zip', compression='zip',
                 delimiter=';')

# pd.set_option('display.max_columns', 200)
# pd.set_option('display.max_rows', 100)
# pd.set_option('display.min_rows', 100)
# pd.set_option('display.expand_frame_repr', True)

print(df.head())
