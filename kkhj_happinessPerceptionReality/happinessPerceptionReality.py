from getDatasets import get_datasets
from missingValues import *
from perceivedIndex import add_perceived_index


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

        # Initialise variables
        self.df = datasets
        self.countries = get_countries_list(df)


if __name__ == "__main__":
    res = happinessPerceptionReality()
    df = res.df
    res.df.to_excel("output.xlsx")
