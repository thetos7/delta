import pandas as pd
import os
import glob
import numpy as np

path = os.path.join(os.getcwd(), "mzgl_inegalites_de_revenus/data/")


def get_inegalities_df(countries_df):
    """
    Read every csv files of the World Inegalities Database, load it into one dataframe
    """
    df = pd.concat(
        [
            pd.read_csv(filename, index_col=False, sep=";")
            for filename in glob.glob("".join([path, "wid_data/WID_data_*.csv"]))
        ]
    )
    df = df.loc[df["year"] >= 1995]
    df = (
        df.drop(["pop", "age", "variable"], axis=1)
        .set_index(["country", "percentile", "year"])
        .rename_axis(["alpha2", "Percentile", "Year"], axis=0)
        .sort_index()
    )
    return (
        df.join(countries_df, sort=False)
        .reset_index()
        .set_index(["alpha3", "Percentile", "Year"])
        .sort_index()
    )


def get_corruption_df():
    """
    Read corruption perception dataset, load it into one dataframe
    """
    list_dataframe = []
    for filename in os.listdir("".join([path, "Corruption_perceptions_index/"])):
        year = filename[4:8]
        tmp_df = (
            pd.read_csv(
                "".join([path, "Corruption_perceptions_index/", filename]),
                sep=",",
                index_col=False,
            )
            .filter(["ISO", "Rank", "Score"], axis=1)
            .rename(columns={"Score": "score"})
        )
        tmp_df["Year"] = year
        # Update CPI (Corruption Perceptions Index) score before 2012
        if year < "2012":
            tmp_df.score = tmp_df.score.astype("float64").apply(lambda x: x * 10)
        list_dataframe.append(tmp_df)
    return (
        pd.concat(list_dataframe, axis=0)
        .astype({"Year": "int64"})
        .set_index(["ISO", "Year"])
        .rename_axis(["alpha3", "Year"], axis=0)
        .rename(columns={"Score": "score"})
        .sort_index()
    )


def get_democratie_index_df():
    """
    Read democracy dataset, load it into one dataframe
    """
    df = pd.read_csv("".join([path, "Democracy_Indices.csv"]))
    df.geo = df.geo.str.upper()
    return (
        df.set_index(["geo", "time"])
        .rename_axis(["alpha3", "Year"], axis=0)
        .filter(["Democracy index (EIU)"])
        .rename(columns={"Democracy index (EIU)": "score"})
        .sort_index()
    )


def get_countries_df():
    """
    Read countries dataset, load it into one dataframe
    """
    return (
        pd.read_csv("".join([path, "Countries.csv"]), sep=";", index_col=False)
        .set_index(["alpha2"])
        .replace(
            {
                "Africa": "Afrique",
                "Asia": "Asie",
                "Oceania": "Océanie",
                "Americas": "Amérique",
            }
        )
        .sort_index()
    )


def get_population_df():
    """
    Read population dataset, load it into one dataframe
    """
    return (
        pd.read_csv("".join([path, "Population/data.csv"]))
        .set_index(["alpha3"])
        .drop(["Country Name", "Series Name", "Series Code"], axis=1)
        .replace("..", 0)
        .sort_index()
    )


def get_gdp_df():
    """
    Read Gross domestic product per capita dataset, load it into one dataframe
    """
    gdp_df = (
        pd.read_csv("".join([path, "GDP/data.csv"]))
        .drop(["Series Code", "Country Name"], axis=1)
        .set_index(["alpha3", "Series Name"])
        .replace("..", np.nan)
        .sort_index()
    )
    gdp_df = gdp_df.loc[(slice(None), "GDP per capita (current US$)", slice(None))]
    return gdp_df.loc[
        :,
        [
            "1995",
            "1996",
            "1997",
            "1998",
            "1999",
            "2000",
            "2001",
            "2002",
            "2003",
            "2004",
            "2005",
            "2006",
            "2007",
            "2008",
            "2009",
            "2010",
            "2011",
            "2012",
            "2013",
            "2014",
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
        ],
    ]
