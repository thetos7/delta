from getDatasets import get_datasets
from missingValues import *
from perceivedIndex import *
import pycountry_convert as pc


class happinessPerceptionReality():
    def __init__(self):
        # Extract datasets
        datasets = get_datasets()

        # TODO Read importance rate entered by users

        # Store importance rates
        importanceRate = {'safety': 0.25,
                          'unemployment': 0.25,
                          'socialContribution': 0.25,
                          'gdpPerCapital': 0.25,
                          'educationLevel': 0}

        # Add perceived happiness
        datasets = add_perceived_index(datasets, importanceRate)

        continents = {
            'NA': 'North America',
            'SA': 'South America',
            'AS': 'Asia',
            'OC': 'Australia',
            'AF': 'Africa',
            'EU': 'Europe'
        }

        datasets['Country_code'] = datasets['Country'].apply(lambda x : pc.country_name_to_country_alpha2(x, cn_name_format="default"))
        datasets['Continent'] = datasets['Country_code'].apply(lambda x : continents[pc.country_alpha2_to_continent_code(x)])
        datasets.drop("Country_code", inplace=True, axis=1)


        # Initialise variables
        self.df = datasets
        self.countries = get_countries_list(self.df)


if __name__ == "__main__":
    res = happinessPerceptionReality()
    df = res.df
    res.df.to_excel("output.xlsx")
