#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd


PATH_RESOURCES = Path("TBGT_population_vs_train_speed/data")
TRAIN_PATH = PATH_RESOURCES / "meilleurs-temps-des-parcours-des-trains.csv"
POPUL_PATH = PATH_RESOURCES / "base-pop-historiques-1876-2019.xlsx"
CITIE_PATH = PATH_RESOURCES / "cities.json"

def get_train_data() -> pd.DataFrame:
    train_df = pd.read_csv(TRAIN_PATH, sep=";")
    train_df.sort_values("Année", inplace=True)

    return train_df.groupby("Relations")

def get_cities() -> dict[str, Tuple[float, float]]:
    with open(CITIE_PATH, "r") as f:
        cities = json.load(f)

    return cities
