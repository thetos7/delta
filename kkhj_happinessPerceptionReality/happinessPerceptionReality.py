from cleanSocialSecurityContributionData import *
from cleanSafetyData import *
from cleanUnemploymentData import *
from cleanEducationLevelData import *
from cleanGdpData import *
from happiness import *


class happinessPerceptionReality():
    def __init__(self):

        # Extract datasets
        datasets = {'safety': safety_out_of_10(), 'unemployment': unemployment_out_of_ten(),
                    'socialContribution': security_contribution_out_of_10(), 'gdpPerCapita': extract_gdp_index(),
                    'perceivedHappiness': get_perceived_happiness_dataset()}
        # TODO find better dataset for educationLevel/literacy and decomment the line below
        # datasets['educationLevel'] = education_out_of_10()

        # Merge all datasets
        df = datasets['safety']
        for count, key in enumerate(datasets):
            if count == 0:
                continue
            df = pd.merge(datasets[key], df, on=["Country", "Year"])

        # Initialise variables
        self.df = df
        self.countries = get_countries_list(df)


if __name__ == "__main__":
    res = happinessPerceptionReality()
    df = res.df
    res.df.to_excel("output.xlsx")
