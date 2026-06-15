import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Categorical Analysis")

files = [
    f for f in os.listdir("data")
    if f.endswith(".xlsx")
]

if len(files) == 0:

    st.warning(
        "No variables saved yet."
    )

else:

    selected_file = st.selectbox(
        "Select Variable",
        files
    )

    df = pd.read_excel(
        f"data/{selected_file}"
    )

    total = df["Count"].sum()

    df["Percentage"] = (
        df["Count"] / total
    ) * 100

    st.subheader(
        "Frequency Table"
    )

    st.dataframe(df)

    st.subheader(
        "Pie Chart"
    )

    pie = px.pie(
        df,
        names="Category",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    st.subheader(
        "Bar Chart"
    )

    bar = px.bar(
        df,
        x="Category",
        y="Count",
        text="Count"
    )

    st.plotly_chart(
        bar,
        use_container_width=True
    )