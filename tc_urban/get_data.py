import pandas as pd

def get_clean_data():
    indicators_df = pd.read_csv("data/Indicators.csv")
    countries_df = pd.read_csv("data/countries_continents_codes_flags_url.csv")

    # Clean the countries dataframe
    countries_df = countries_df[['country', 'alpha-3', 'region']]
    countries_df.rename(columns = {'country': 'CountryName', 'alpha-3': 'CountryCode', 'region': 'RegionName'}, inplace = True)

    # Clean the indicators dataframe

    # Keep only the good indicators for us :
    #   - CO2 emission : EN.ATM.CO2E.KT
    #   - Total population : SP.POP.TOTL
    #   - Rural population : SP.RUR.TOTL
    #   - Urban population : SP.URB.TOTL
    indicators_df = indicators_df[(indicators_df.IndicatorCode == "SP.POP.TOTL") |
        (indicators_df.IndicatorCode == "SP.RUR.TOTL") |
        (indicators_df.IndicatorCode == "SP.URB.TOTL") |
        (indicators_df.IndicatorCode == "EN.ATM.CO2E.KT")]

    # With a five years step
    indicators_df = indicators_df[indicators_df.Year % 5 == 0]

    # Remove Countries without CO2 information
    tmp = indicators_df[indicators_df.IndicatorCode == "EN.ATM.CO2E.KT"]['CountryCode'].drop_duplicates()
    indicators_df = pd.merge(indicators_df, tmp, on = ['CountryCode'])

    # Main dataframe
    df = pd.merge(indicators_df, countries_df, on = ["CountryCode", "CountryName"])
    RegionName_Column = df.pop("RegionName")
    df.insert(2, 'RegionName', RegionName_Column)

    return df