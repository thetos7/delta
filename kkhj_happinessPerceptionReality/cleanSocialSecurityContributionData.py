import pandas as pd

def get_security_contribution():
    df = pd.read_excel("data/socialSecurityContributions.xlsx")
    df = df.melt(['Country'], var_name='Year', value_name='Social Security Employer Contribution')
    return df[(df != '-').all(1)]

def security_contribution_out_of_10():
    df = get_security_contribution()
    df.loc[:, df.columns == 'Social Security Employer Contribution'] = df.loc[:, df.columns == 'Social Security Employer Contribution'].div(10)
    return df