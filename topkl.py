import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])
df.to_pickle(sys.argv[1].split('.')[0] + '.pkl')    #to save the dataframe, df to 123.pkl
