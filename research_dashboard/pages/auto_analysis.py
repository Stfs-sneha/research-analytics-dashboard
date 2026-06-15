import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Auto Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("🤖 Auto Analytics")

# =====================================================
# CHECK DATA FOLDER
# =====================================================

UPLOAD_FOLDER = "data/uploaded"

if not os.path.exists(UPLOAD_FOLDER):
    st.warning("Upload a dataset first using the Upload Excel page.")
    st.stop()

# =====================================================
# FIND EXCEL FILES
# =====================================================

files = [
    f for f in os.listdir(UPLOAD_FOLDER)
    if f.endswith(".xlsx")
]

if len(files) == 0:
    st.warning("No uploaded datasets found.")
    st.stop()

# =====================================================
# SELECT DATASET
# =====================================================

selected_file = st.selectbox(
    "Select Dataset",
    files
)

file_path = os.path.join(
    UPLOAD_FOLDER,
    selected_file
)

# =====================================================
# LOAD DATASET
# =====================================================

try:
    df = pd.read_excel(file_path)

except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# =====================================================
# DATASET OVERVIEW
# =====================================================

st.success(f"Loaded: {selected_file}")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Rows",
        df.shape[0]
    )

with col2:
    st.metric(
        "Columns",
        df.shape[1]
    )

with st.expander("Preview Dataset"):
    st.dataframe(
        df.head(),
        width=True
    )

# =====================================================
# DETECT COLUMN TYPES
# =====================================================

categorical_cols = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

numerical_cols = df.select_dtypes(
    include=["number"]
).columns.tolist()

# =====================================================
# SHOW DETECTED VARIABLES
# =====================================================

st.subheader("Detected Variables")

col3, col4 = st.columns(2)

with col3:
    st.write("### Categorical Variables")
    st.write(categorical_cols)

with col4:
    st.write("### Numerical Variables")
    st.write(numerical_cols)

# =====================================================
# ANALYSIS TYPE
# =====================================================

analysis_type = st.radio(
    "Choose Analysis Type",
    [
        "Categorical Analysis",
        "Numerical Analysis"
    ]
)

# =====================================================
# CATEGORICAL ANALYSIS
# =====================================================

if analysis_type == "Categorical Analysis":

    if len(categorical_cols) == 0:
        st.warning("No categorical variables found.")
        st.stop()

    column = st.selectbox(
        "Select Categorical Variable",
        categorical_cols
    )

    freq = (
        df[column]
        .value_counts(dropna=False)
        .reset_index()
    )

    freq.columns = [
        "Category",
        "Frequency"
    ]

    total = freq["Frequency"].sum()

    freq["Percentage"] = round(
        (freq["Frequency"] / total) * 100,
        2
    )

    st.subheader("Frequency Table")

    st.dataframe(
        freq,
        width=True
    )

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Pie Chart",
            "Donut Chart",
            "Bar Chart",
            "Horizontal Bar Chart"
        ]
    )

    if chart_type == "Pie Chart":

        fig = px.pie(
            freq,
            names="Category",
            values="Frequency",
            title=column
        )

        st.plotly_chart(
            fig,
            width=True
        )

    elif chart_type == "Donut Chart":

        fig = px.pie(
            freq,
            names="Category",
            values="Frequency",
            hole=0.5,
            title=column
        )

        st.plotly_chart(
            fig,
            width=True
        )

    elif chart_type == "Bar Chart":

        fig = px.bar(
            freq,
            x="Category",
            y="Frequency",
            text="Frequency",
            title=column
        )

        st.plotly_chart(
            fig,
            width=True
        )

    elif chart_type == "Horizontal Bar Chart":

        fig = px.bar(
            freq,
            y="Category",
            x="Frequency",
            text="Frequency",
            orientation="h",
            title=column
        )

        st.plotly_chart(
            fig,
            width=True
        )

# =====================================================
# NUMERICAL ANALYSIS
# =====================================================

elif analysis_type == "Numerical Analysis":

    if len(numerical_cols) == 0:
        st.warning("No numerical variables found.")
        st.stop()

    column = st.selectbox(
        "Select Numerical Variable",
        numerical_cols
    )

    data = df[column].dropna()

    st.subheader("Descriptive Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Mean",
            round(data.mean(), 2)
        )

    with c2:
        st.metric(
            "Median",
            round(data.median(), 2)
        )

    with c3:
        st.metric(
            "Minimum",
            round(data.min(), 2)
        )

    with c4:
        st.metric(
            "Maximum",
            round(data.max(), 2)
        )

    c5, c6, c7, c8 = st.columns(4)

    with c5:
        st.metric(
            "Standard Deviation",
            round(data.std(), 2)
        )

    with c6:
        st.metric(
            "Variance",
            round(data.var(), 2)
        )

    with c7:
        st.metric(
            "Range",
            round(data.max() - data.min(), 2)
        )

    with c8:
        st.metric(
            "Count",
            len(data)
        )

    st.subheader("Detailed Summary")

    st.dataframe(
        data.describe().to_frame(),
        width=True
    )

    st.subheader("Histogram")

    hist = px.histogram(
        df,
        x=column,
        nbins=20,
        title=f"{column} Distribution"
    )

    st.plotly_chart(
        hist,
        width=True
    )

    st.subheader("Box Plot")

    box = px.box(
        df,
        y=column,
        title=f"{column} Box Plot"
    )

    st.plotly_chart(
        box,
        width=True
    )