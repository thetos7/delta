import pandas as pd

def get_security_contribution():
    df = pd.read_excel("data/socialSecurityContributions.xlsx")
    df = df.melt(['Country'], var_name='Year', value_name='Social Security Employer Contribution Index')
    # TODO if don't want to keep empty cells => decomment line below
    return df[(df != '-').all(1)]

# print(get_security_contribution()['Year'])

def security_contribution_out_of_10():
    df = get_security_contribution()
    df.loc[:, df.columns == 'Social Security Employer Contribution Index'] = df.loc[:, df.columns == 'Social Security Employer Contribution Index'].div(10)
    return df