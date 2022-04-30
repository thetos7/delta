def apply_importance_rate(index, rate):
    newIndex = index * rate
    return newIndex


def add_perceived_index(datasets, rates):
    safetyImportance = rates['safety']
    unemploymentImportance = rates['unemployment']
    socialContributionImportance = rates['socialContribution']
    gdpPerCapitalImportance = rates['gdpPerCapital']
    # educationLevelImportance = rates['educationLevel']

    modifiedIndex = [apply_importance_rate(datasets['Safety Index'], safetyImportance),
                     apply_importance_rate(datasets['Unemployment Index'], unemploymentImportance),
                     apply_importance_rate(datasets['Social Security Employer Contribution Index'],
                                           socialContributionImportance),
                     apply_importance_rate(datasets['GDP Index'], gdpPerCapitalImportance)]

    # TODO if educationLevel then append lines below to the prev list
    # ,
    #                      apply_importance_rate(datasets[''])

    datasets['Percieved Happiness'] = modifiedIndex[0] + modifiedIndex[1] + modifiedIndex[2] + modifiedIndex[3]

    # TODO if educationLevel then append line below to the prev
    # + modifiedIndex[4]
    return datasets


# importanceRate = {'safety': 0.25,
#                   'unemployment': 0.25,
#                   'socialContribution': 0.25,
#                   'gdpPerCapital': 0.25,
#                   'educationLevel': 0}
# get_perceived_index(happinessPerceptionReality().df, importanceRate).to_excel('perceived.xlsx')
