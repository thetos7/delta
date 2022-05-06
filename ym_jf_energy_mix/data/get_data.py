# must be run from file root (python3 get_data.py)
# step 1 : have a kaggle account https://www.kaggle.com/
# step 2 : install kaggle API : pip install kaggle
# step 3 : go to account -> scroll down to API -> click Create token
# step 4 : move file to ~/kaggle/kaggle.json
# step 5 : run python file

# if it doesn't work or you don't want to waste your time, just download the file from the website at
# https://www.kaggle.com/datasets/pralabhpoudel/world-energy-consumption
# rename it to World_Energy_Consumption.csv (note the underscores)
# place it in data/ and ym_jf_energy_mix/data/

import kaggle
import os
import shutil

kaggle.api.authenticate()

kaggle.api.dataset_download_files('pralabhpoudel/world-energy-consumption', path='.', unzip=True)

os.rename("./World Energy Consumption.csv", "./World_Energy_Consumption.csv")

shutil.copyfile("./World_Energy_Consumption.csv", "../../data/World_Energy_Consumption.csv")