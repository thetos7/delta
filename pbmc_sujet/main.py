import time
import data.get_data as dp
import plotly.express as px

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

color = {
	"Léger" : "#FFFF00",
	"mortel" : "#FF0000",
	"grave non mortel" : "#FF7F00"
}

figure1 = px.histogram(
    df,
    x=df["Année"],
    color = df["Catégorie véhicule"],
    facet_col = "Type Accident",
    facet_col_wrap = 3,
)

figure1.update_layout(barmode="stack", bargap=0.2)

figure2 = px.scatter_3d(
    dp.getMortality(df),
    x = 'Année',
    y = 'Age véhicule',
    z = 'Count',
    color = 'Type Accident',
    color_discrete_map=color,
)

figure1.show()
figure2.show()
