from unicodedata import category
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

if __name__ == "__main__":

    # Read CSV
    df = pd.read_csv("./parrainagestotal.csv", sep=";")

    # Clean data: parse publication date
    df['Date de publication'] = pd.to_datetime(
        df['Date de publication'], format='%d/%m/%Y')

    # Display sidebar
    candidats_occurences = df['Candidat'].value_counts()
    candidat = st.sidebar.radio(
        'Candidat',
        candidats_occurences[candidats_occurences > 500].keys()
    )

    # Select candidate
    parainnages = df[df['Candidat'] == candidat]

    count_by_date = parainnages.groupby(["Date de publication"]).size()

    index = count_by_date.index
    index.name = 'date'

    df_count_by_date = pd.DataFrame(
        {"count": count_by_date, "cummulative_sum": count_by_date.cumsum()}, index=index)

    df_count_by_date = df_count_by_date.reset_index().melt('date', var_name="category", value_name="y")

    """
        TODO:
        - display month
    """

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['date'], empty='none')

    chart = alt.Chart(df_count_by_date).mark_line(
        interpolate='monotone'
    ).encode(
        x="date:T",
        y="y:Q",
        color="category:N"
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(df_count_by_date).mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = chart.mark_point().encode(
        opacity=alt.value(1)
    )

    # Draw text labels near the points, and highlight based on selection
    text = chart.mark_text(align='left', dx=5, dy=-5, color='white').encode(
        text=alt.condition(nearest, 'y:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(df_count_by_date).mark_rule(color='white').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )
    
    layer = alt.layer(chart, selectors, points, rules, text)

    st.altair_chart(layer, use_container_width=True)
