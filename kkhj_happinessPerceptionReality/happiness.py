import pandas as pd
import cleanEducationLevelData as education
import cleanGdpData as gdp
import cleanSafetyData as safety
import cleanSocialSecurityContributionData as social
import cleanUnemploymentData as unemployment

def get_perceived_happiness_dataset():
    df = pd.read_csv('data/perceivedHappiness.csv')
    df.rename(columns={'Entity': 'Country', 'Life satisfaction in Cantril Ladder (World Happiness Report 2021)': 'Happiness Index'}, inplace=True)
    mask = (df['Year'] >= 2012) & (df['Year'] <= 2021)
    df = df[mask].reset_index()
    del df['Code']
    del df['index']
    return df

def get_countries_list(dataset):
    list_countries = dataset['Country'].unique()
    return list_countries

def intersection(list1, list2):
    list = [value for value in list1 if value in list2]
    return list

def get_missing_values(dataset):
    # for all countries in datset
    # for all years in 2012, 2021
    # if missing then look for x - 1 if >= 2012 and x + 1 if <= 2021
    # while one missing then -1 or +1 (or both)
    # if one take it, else mean of the two
    # if all missing and all over boundaries --> RAISE ERROR (but not possible)
    # copy row to dataset --> change value and date

if __name__ == "__main__":
    perceived_happiness_dataset = get_perceived_happiness_dataset()
    safety_dataset = safety.safety_out_of_10()
    education_level_dataset = education.education_out_of_10()
    gdp_dataset = gdp.gdp_out_of_10()
    social_security_contribution_dataset = social.security_contribution_out_of_10()
    unemployment_dataset = unemployment.unemployment_out_of_ten()

    list = get_countries_list(perceived_happiness_dataset)

    perceived_happiness_countries = get_countries_list(perceived_happiness_dataset)
    safety_countries = get_countries_list(safety_dataset)
    education_level_countries = get_countries_list(education_level_dataset)
    gdp_countries = get_countries_list(gdp_dataset)
    social_security_contribution_countries = get_countries_list(social_security_contribution_dataset)
    unemployment_countries = get_countries_list(unemployment_dataset)

    all_countries = intersection(intersection(intersection(intersection(perceived_happiness_countries,
                                                                                     safety_countries), gdp_countries),
                                              social_security_contribution_countries), unemployment_countries)

    print(len(all_countries))


# include the mask2 when counting countries #we're going to assume it's true
# ignore education level for now


# form huge dataset
# behavior for missing values
# graph part with inputs
# calculate real happiness with input
# update graph
# test all
