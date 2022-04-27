from cleanSocialSecurityContributionData import *
from cleanSafetyData import *
from cleanUnemploymentData import *
from cleanGdpData import *
from missingValues import get_real_happiness_dataset
from cleanEducationLevelData import *


def get_datasets():

    # Extract datasets
    datasets = {'safety': safety_out_of_10(), 'unemployment': unemployment_out_of_ten(),
                'socialContribution': security_contribution_out_of_10(), 'gdpPerCapital': extract_gdp_index(),
                'realHappiness': get_real_happiness_dataset()}
    # TODO find better dataset for educationLevel/literacy and append line below to dict datasets
    # 'educationLevel': education_out_of_10()

    # Merge all datasets
    df = datasets['safety']
    for count, key in enumerate(datasets):
        if count == 0:
            continue
        df = pd.merge(datasets[key], df, on=["Country", "Year"])

    return df
