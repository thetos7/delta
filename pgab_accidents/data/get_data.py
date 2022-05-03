#!/usr/bin/env python3
import pandas as pd
import os
import zipfile as zf
import requests
import io

# Urls default to data from 2018
IMMATRICULATION_URL = os.environ.get(
    "IMMATRICULATION_URL", "https://www.data.gouv.fr/fr/datasets/r/5ec2789d-585a-4a4a-9efd-c47f6f085b64")
LIEUX_URL = os.environ.get(
    "LIEUX_URL", "https://www.data.gouv.fr/fr/datasets/r/d9d65ca1-16a3-4ea3-b7c8-2412c92b69d9")
USAGERS_URL = os.environ.get(
    "USAGERS_URL", "https://www.data.gouv.fr/fr/datasets/r/72b251e1-d5e1-4c46-a1c2-c65f1b26549a")
VEHICULES_URL = os.environ.get(
    "VEHICULES_URL", "https://www.data.gouv.fr/fr/datasets/r/b4aaeede-1a80-4d76-8f97-543dad479167")
CARACS_URL = os.environ.get(
    "CARACS_URL", "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405")
POP_URL = os.environ.get(
    "POP_URL", "https://www.insee.fr/fr/statistiques/fichier/5395878/BTT_TD_POP1A_2018.zip")
POP_CSV_FILENAME = os.environ.get(
    "POP_CSV_FILENAME", f"{'.'.join(POP_URL.split('/')[-1].split('.')[:-1])}.CSV")

print("Reading immatriculation data...")
immatriculations = pd.read_csv(IMMATRICULATION_URL, sep=";")
print("Reading location data...")
lieux = pd.read_csv(LIEUX_URL)
print("Reading user data...")
usagers = pd.read_csv(USAGERS_URL)
print("Reading vehicle data...")
vehicules = pd.read_csv(VEHICULES_URL)
print("Reading accident caracteristics data...")
caracs = pd.read_csv(CARACS_URL, encoding='iso-8859-1')

zip = zf.ZipFile(io.BytesIO(requests.get(POP_URL).content))
pop = pd.read_csv(zip.open(POP_CSV_FILENAME), sep=';')


# TODO process data, cleanup, join...
# ...

print("Writing final file(s)...")
immatriculations.to_csv("immatriculation-2018.csv", sep=';')
lieux.to_csv("lieux-2018.csv")
usagers.to_csv("usagers-2018.csv")
vehicules.to_csv("vehicules-2018.csv")
caracs.to_csv("caracteristiques-2018.csv")
pop.to_csv("pop-2018.csv", sep=';')
print()
print("Done.")
