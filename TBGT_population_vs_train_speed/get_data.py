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

Coords = Tuple[float, float]


def _clean_train(train_df: pd.DataFrame) -> None:
    train_df.loc[train_df["Relations"] == "PARIS - BOULOGNE", "Relations"] = "PARIS - BOULOGNE-SUR-MER"
    train_df.loc[train_df["Relations"] == "PARIS - CHERBOURG", "Relations"] = "PARIS - CHERBOURG-EN-COTENTIN"
    train_df.loc[train_df["Relations"] == "PARIS - CLERMONT FERRAND", "Relations"] = "PARIS - CLERMONT-FERRAND"
    train_df.loc[train_df["Relations"] == "PARIS - ST ETIENNE", "Relations"] = "PARIS - SAINT-ETIENNE"

def get_train_data() -> pd.core.groupby.DataFrameGroupBy:
    train_df = pd.read_csv(TRAIN_PATH, sep=";")
    train_df.sort_values("Année", inplace=True)
    _clean_train(train_df)

    return train_df.groupby("Relations")

def get_cities() -> dict[str, Coords]:
    with open(CITIE_PATH, "r") as f:
        cities = json.load(f)

    return cities
