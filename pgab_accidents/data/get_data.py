#!/usr/bin/env python3
import pandas as pd
import os
import zipfile as zf
import requests
import io

# Urls default to data from 2018
LIEUX_URL = os.environ.get(
    "LIEUX_URL", "https://www.data.gouv.fr/fr/datasets/r/d9d65ca1-16a3-4ea3-b7c8-2412c92b69d9")
USAGERS_URL = os.environ.get(
    "USAGERS_URL", "https://www.data.gouv.fr/fr/datasets/r/72b251e1-d5e1-4c46-a1c2-c65f1b26549a")
VEHICULES_URL = os.environ.get(
    "VEHICULES_URL", "https://www.data.gouv.fr/fr/datasets/r/b4aaeede-1a80-4d76-8f97-543dad479167")
CARACS_URL = os.environ.get(
    "CARACS_URL", "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405")

print("Reading location data...")
lieux = pd.read_csv(LIEUX_URL)
print("Reading user data...")
usagers = pd.read_csv(USAGERS_URL)
print("Reading vehicle data...")
vehicules = pd.read_csv(VEHICULES_URL)
print("Reading accident caracteristics data...")
caracs = pd.read_csv(CARACS_URL, encoding='iso-8859-1')

# TODO process data, cleanup, join...
# ...

print("Writing final file(s)...")
lieux.to_csv("lieux-2018.csv")
usagers.to_csv("usagers-2018.csv")
vehicules.to_csv("vehicules-2018.csv")
caracs.to_csv("caracteristiques-2018.csv")
print()
print("Done.")
