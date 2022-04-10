import time
import data.get_data as dp
import plotly.express as px
import plotly.graph_objects as go

t_1 = time.time()
df = dp.loadData()
t_2 = time.time()
print("Loaded database in " + "{:.2f}".format(t_2 - t_1) + " seconds!")

# Vehicle Types:
# - PL - Poids Lourd
# - VT - Véhicules Tourisme
# - VU - Véhicules Utilitaires
# - TC - Transport en Commun
# - Moto lourde
# - Moto légère
# - Cyclo

# Accident Types:
# - mortel
# - grave non mortel
# - Léger

figure1 = px.histogram(
        dp.getInfo(df=df),
        x=df["Année"],
        color = df["Catégorie véhicule"],
        facet_col = "Type Accident",
        facet_col_wrap = 3,
)
figure1.update_layout(barmode="stack", bargap=0.2)
figure1.show()

mdf = dp.getCounts(df=df)
color = {"Léger": "#9ecbed", "mortel": "#2a6a99", "grave non mortel": "#3c97da"}

figure2 = px.scatter_3d(
    mdf,
    x = 'Année',
    y = 'Age véhicule',
    z = 'Count',
    color = 'Type Accident',
    color_discrete_map=color,
) 

figure2.show()
