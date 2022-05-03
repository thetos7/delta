#!/usr/bin/env python3
import pandas as pd
import os

# Urls default to data from 2018
USAGERS_URL = os.environ.get(
    "USAGERS_URL", "https://www.data.gouv.fr/fr/datasets/r/72b251e1-d5e1-4c46-a1c2-c65f1b26549a")
CARACS_URL = os.environ.get(
    "CARACS_URL", "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405")

print("Reading user data...")
usagers = pd.read_csv(USAGERS_URL)
print("Reading accident caracteristics data...")
caracs = pd.read_csv(CARACS_URL, encoding='iso-8859-1')

# TODO process data, cleanup, join...
# ...

print("Writing final file(s)...")
usagers.to_csv("usagers-2018.csv", index=False)
caracs.to_csv("caracteristiques-2018.csv", index=False)
print()
print("Done.")
