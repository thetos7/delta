from missingValues import get_all_datasets
from cleanEducationLevelData import *


def get_datasets():

    # Extract datasets
    data = get_all_datasets()
    datasets = {'safety': data[1], 'unemployment': data[4],
                'socialContribution': data[3], 'gdpPerCapital': data[2],
                'realHappiness': data[0]}

    # TODO find better dataset for educationLevel/literacy and append line below to dict datasets
    # 'educationLevel': education_out_of_10()

    # Merge all datasets
    df = datasets['safety']
    for count, key in enumerate(datasets):
        if count == 0:
            continue
        df = pd.merge(datasets[key], df, on=["Country", "Year"])

    return df
