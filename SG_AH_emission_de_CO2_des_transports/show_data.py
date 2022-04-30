from get_data import get_pollution_per_vehicules_in_france as func
import numpy as np
import pandas as pd
import plotly.express as px

def update_graph(self, name="HC et Nox"):
    col = f"Emission {name}"
    df = func()
    agg = (
        df[["Marque", col]]
        .groupby(["Marque"])
        .mean()
        .reset_index()
        .sort_values(by=[col, "Marque"])
        # .replace(np.NaN,0)
    )

    fig = px.bar(agg, y=col, x="Marque", title=f"Moyenne d'{col} pour les modèles par marque")
    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )
    fig.show()
