import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Visualization Studio",
    layout="wide"
)

st.title("📈 Visualization Studio")

folder = "data/categorical"

if not os.path.exists(folder):

    st.warning(
        "No datasets found. Generate a dataset first."
    )

else:

    files = [
        f for f in os.listdir(folder)
        if f.endswith(".xlsx")
    ]

    if len(files) == 0:

        st.warning(
            "No saved variables found."
        )

    else:

        selected_file = st.selectbox(
            "Select Variable Dataset",
            files
        )

        df = pd.read_excel(
            f"{folder}/{selected_file}"
        )

        st.subheader("Dataset")

        st.dataframe(
            df,
            use_container_width=True
        )

        chart_type = st.selectbox(
            "Select Visualization",
            [
                "Pie Chart",
                "Donut Chart",
                "Bar Chart",
                "Horizontal Bar Chart",
                "Histogram"
            ]
        )

        if chart_type == "Pie Chart":

            fig = px.pie(
                df,
                names="Category",
                values="Count",
                title=selected_file
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif chart_type == "Donut Chart":

            fig = px.pie(
                df,
                names="Category",
                values="Count",
                hole=0.5,
                title=selected_file
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif chart_type == "Bar Chart":

            fig = px.bar(
                df,
                x="Category",
                y="Count",
                text="Count",
                title=selected_file
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif chart_type == "Histogram":

            fig = px.histogram(
                df,
                x="Count",
                nbins=20,
                title=f"Histogram of Counts"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif chart_type == "Horizontal Bar Chart":

            fig = px.bar(
                df,
                y="Category",
                x="Count",
                text="Count",
                orientation="h",
                title=selected_file
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        total = df["Count"].sum()

        st.metric(
            "Total Participants",
            int(total)
        )