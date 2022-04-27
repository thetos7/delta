
import pandas as pd
import dateutil
import glob

def clean_data(df):
    # remove odd rows
    df = df.iloc[::2]
    
    df = df.replace('ND', 0)
    df.iloc[:,5:36].apply(pd.to_numeric)
    
    # groupby date
    df = df.groupby(pd.Grouper(key='Date')).sum()
    df.reset_index(inplace=True)
    
    return df

df = pd.concat({dateutil.parser.parse(f.split('RTE-')[1].split('csv')[0]):clean_data(pd.read_csv(f, delimiter=";", low_memory=False)) for f in glob.glob('RTE-*')})
df.sort_index(inplace=True)
df.reset_index(drop=True, inplace=True)

df_full = df.copy()
df_full['Date'] = pd.to_datetime(df_full['Date'], format='%d/%m/%Y')
df_full.set_index('Date', inplace=True)
df_full.rename(columns={'NuclÈaire': 'Nuclèaire',
                   'BioÈnergies': 'Bioénergies'}, inplace=True)
selection = ['Fioul', 'Charbon', 'Nuclèaire', 'Eolien', 'Solaire', 'Hydraulique', 'Bioénergies']
df_full_selected = df_full[selection]

df_full_selected.to_pickle("preprocessed_maingraphdata.pkl")

df_animated = df_full_selected.groupby(pd.Grouper(freq='M')).sum().copy()
df_animated.reset_index(inplace=True)
df_animated = df_animated.melt(id_vars="Date", var_name="Type", value_name="Value")
df_animated.sort_index(inplace=True)
df_animated['Date'] = df_animated['Date'].apply(lambda x: str(x))

df_animated.to_pickle("preprocessed_barplotdata.pkl")

df_prix = pd.read_csv('TRV_electricite_2012-2022.csv', delimiter=';', decimal=',')
df_prix.drop(columns=['Unnamed: 7', 'DATE_FIN'], inplace=True)
df_prix['DATE_DEBUT'] = pd.to_datetime(df_prix['DATE_DEBUT'], format='%d/%m/%Y')
df_prix.set_index('DATE_DEBUT', inplace=True)
df_prix[['PART_FIXE_HT','PART_FIXE_TTC','PART_VARIABLE_HT','PART_VARIABLE_TTC']] = df_prix[['PART_FIXE_HT','PART_FIXE_TTC','PART_VARIABLE_HT','PART_VARIABLE_TTC']] * 1000

df_prix.to_pickle("preprocessed_pricedata.pkl")
