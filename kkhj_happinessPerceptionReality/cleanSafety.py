import pandas as pd

def extract_safety(year):
    file = "data/criminality" + str(year) + ".xlsx"
    tab = pd.read_excel(file)
    df = pd.DataFrame({'Country': tab["Country"], f"{year}": tab["Safety Index"]})
    return df

def combine_dfs():
    tab = extract_safety(2012)
    for x in range(13, 22):
        file = str(20) + str(x)
        tab = tab.join(extract_safety(file).set_index(['Country']), on='Country')
    return tab.melt(['Country'], var_name='Year', value_name='Safety Index')

def safety_out_of_10():
    tab = combine_dfs()
    tab['Safety Index'] = tab['Safety Index'].div(10)
    return tab