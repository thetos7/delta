import pandas as pd
import numpy as np


def get_europe_pollution(geoToCountry):
    df = pd.read_csv("data/sdg_13_10_linear.csv")
    df.replace(geoToCountry.to_dict(), inplace=True)
    
    clean_date=[1990, 1991, 1992,1993, 1994]
    drop_country=['Turquie', 'Royaume-Uni', 'Union européenne - 28 pays (2013-2020)', 'Islande']
    
    I90_df = df[(df.unit == 'I90') & (df.src_crf == 'TOTXMEMONIA')]
    I90_clean_df = pd.DataFrame(data={'Pays' : I90_df.geo, 'Value' : I90_df.OBS_VALUE, 'Time': I90_df.TIME_PERIOD})
    I90_clean_df.set_index('Time', inplace=True)
    I90_clean_df.drop(clean_date, inplace=True, axis=0)
    I90_clean_df = I90_clean_df[~I90_clean_df['Pays'].isin(drop_country)]
    I90_clean_df.rename(columns={'Value': "I90"}, inplace=True)

    T_HAB_df = df[(df.unit == 'T_HAB') & (df.src_crf == 'TOTXMEMONIA')]
    T_HAB_clean_df = pd.DataFrame(data={'Pays' : T_HAB_df.geo, 'Value' : T_HAB_df.OBS_VALUE, 'Time': T_HAB_df.TIME_PERIOD})
    T_HAB_clean_df.set_index('Time', inplace=True)
    T_HAB_clean_df.drop(clean_date, inplace=True, axis=0)
    T_HAB_clean_df = T_HAB_clean_df[~T_HAB_clean_df['Pays'].isin(drop_country)]
    T_HAB_clean_df.rename(columns={'Value': "T_HAB"}, inplace=True)
    
    T_HAB_clean_df['T_HAB'].where(T_HAB_clean_df.T_HAB > 0, other= 0, inplace=True)
    I90_clean_df['I90'].where(I90_clean_df.I90 > 0, other= 0, inplace=True)
    return T_HAB_clean_df.merge(I90_clean_df, on=['Time', 'Pays'], how='left')


def get_europe_environment_outgoings(geoToCountry):
    fisc_df = pd.read_csv("data/t2020_rt320_linear.csv")
    fisc_df.replace(geoToCountry.to_dict(), inplace=True)
    
    drop_country = [ 'LI', 'EA19']
    
    PC_GDP_df = fisc_df[fisc_df.unit == 'PC_GDP']
    PC_GDP_clean_df = pd.DataFrame(data={'Pays' : PC_GDP_df.geo, 'Value' : PC_GDP_df.OBS_VALUE, 'Time': PC_GDP_df.TIME_PERIOD})
    PC_GDP_clean_df.set_index('Time', inplace=True)
    PC_GDP_clean_df.drop([2020], inplace=True, axis=0)
    PC_GDP_clean_df = PC_GDP_clean_df[~PC_GDP_clean_df['Pays'].isin(drop_country)]
    PC_GDP_clean_df.rename(columns={'Value': "PIB"}, inplace=True)
    
    PC_TSCO_X_ISCO_df = fisc_df[fisc_df.unit == 'PC_TSCO_X_ISCO']
    PC_TSCO_X_ISCO_clean_df = pd.DataFrame(data={'Pays' : PC_TSCO_X_ISCO_df.geo, 'Value' : PC_TSCO_X_ISCO_df.OBS_VALUE, 'Time': PC_TSCO_X_ISCO_df.TIME_PERIOD})
    PC_TSCO_X_ISCO_clean_df.set_index('Time', inplace=True)
    PC_TSCO_X_ISCO_clean_df.drop([2020], inplace=True, axis=0)
    PC_TSCO_X_ISCO_clean_df = PC_TSCO_X_ISCO_clean_df[~PC_TSCO_X_ISCO_clean_df['Pays'].isin(drop_country)]
    PC_TSCO_X_ISCO_clean_df.rename(columns={'Value': "TAXES"}, inplace=True)
    return PC_GDP_clean_df.merge(PC_TSCO_X_ISCO_clean_df, on=['Time', 'Pays'], how='left')
    
def save_combined_df(polution_df, outgoing_df):
    combine_df = polution_df.merge(outgoing_df, on=['Time', 'Pays'], how='left')
    combine_df = combine_df.reset_index()
    combine_df.to_csv("europeanEnvTaxesPIB.csv")

def get_cleaned_data():
    return pd.read_csv('ALVS_Greenhouse_gas_and_Environmental_Policy_in_Europe/data/europeanEnvTaxesPIB.csv')
   
if __name__ == '__main__':
    geoToCountry = pd.read_csv("data/geo_country.csv", index_col=1, squeeze=True)
    polution_df = get_europe_pollution(geoToCountry)
    outgoing_df = get_europe_environment_outgoings(geoToCountry)
    save_combined_df(polution_df, outgoing_df)