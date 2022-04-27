# Here is the script to get all the data needed in our project
import pandas as pd

def transform_countries_names(df, col):
    countries_name = { 'AT': 'Autriche', 'BE' : 'Belgique', 'BG' : 'Bulgarie',
                       'CH' : 'Suisse', 'CY': 'Chypre', 'CZ': 'République Tchèque',
                       'DE' : 'Allemagne', 'DK' : 'Danemark', 'EE' : 'Estonie',
                       'EL' : 'Grèce', 'ES' : 'Espagne', 'FI' : 'Finlande',
                       'FR' : 'France', 'HR' : 'Croatie', 'HU' : 'Hongrie',
                       'IE' : 'Irlande', 'IS' : 'Islande', 'IT' : 'Italie',
                       'LI' : 'Liechtenstein', 'LT' : 'Lituanie', 'LU' : 'Luxembourg',
                       'LV' : 'Lettonie', 'MT' : 'Malte', 'NL' : 'Pays-Bas',
                       'NO' : 'Norvège', 'PL' : 'Pologne', 'PT' : 'Portugal',
                       'RO' : 'Roumanie', 'SE' : 'Suède', 'SI' : 'Slovénie',
                       'SK' : 'Slovaquie', 'TR' : 'Turquie', 'UK' : 'Royaume-Uni'}
    df[col].replace(countries_name, inplace = True)
    return df

def get_transport_pollution_eu():
    df = pd.read_csv("data/emission_de_polluant_des_transports_1990-2020.csv")
    
    # Remove the useless columns, keeping only:
    # The data (TIME_PERIOD), The country (geo), Pollution type (airpol), the value of the pollution (OBS_VALUE) 
    columns_to_keep = ['airpol', 'geo', 'TIME_PERIOD', 'OBS_VALUE']
    df = df[columns_to_keep]

    # Seperate data for all EUROPE
    df_all_eu = df.loc[df['geo'] == 'EU27_2020']
    df = df[df['geo'] != 'EU27_2020']
    
    # Rename geo columns with right names
    df = transform_countries_names(df, 'geo')
    return (df_all_eu, df[df['airpol'] == 'NMVOC'], df[df['airpol'] == 'NOX'], df[df['airpol'] == 'PM10'])

def get_mean_co2_new_vehicules():
    df = pd.read_csv("data/moyenne_emissions_CO2_vehicules_neuf_2000-2020.csv")

    # Remove the useless columns
    # Keep : geo, TIME_PERIOD, OBS_VALUE
    columns_to_keep = ['geo', 'TIME_PERIOD', 'OBS_VALUE']
    df = df[columns_to_keep]

    # Seperate data for all EUROPE
    df_all_eu = df.loc[(df['geo'] == 'EU27_2020')]
    df = df[(df['geo'] != 'EU27_2020') & (df['geo'] != 'EU27_2007') & (df['geo'] != 'EU28')]
    
    # Rename geo columns with right names
    df = transform_countries_names(df, 'geo')
    return (df, df_all_eu)

def get_air_pollution_schools():
    df = pd.read_csv("data/ecoles-creches-idf-prepared_2012-2017.csv")

    # remove useless columns
    df = df.drop(['ID', 'ville', 'CP', 'type', 'geometry'], axis=1)
    df.to_csv("e")
    # Seperate according to the type of pollution
    df_no2 = df.filter(regex="nom|departement|NO2.*")
    df_pm10 = df.filter(regex="nom|departement|PM10.*")
    df_pm25 = df.filter(regex="nom|departement|PM25.*")

    return (df_no2, df_pm10, df_pm25)