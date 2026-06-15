import streamlit as st
import pandas as pd
import os

st.title("📂 Upload Excel Dataset")

uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=["xlsx"]
)

if uploaded_file:

    os.makedirs(
        "data/uploaded",
        exist_ok=True
    )

    file_path = (
        f"data/uploaded/{uploaded_file.name}"
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )

    df = pd.read_excel(
        file_path
    )

    st.success(
        "File Uploaded Successfully"
    )

    st.write(
        "Rows:",
        df.shape[0]
    )

    st.write(
        "Columns:",
        df.shape[1]
    )

    st.dataframe(
        df.head(),
        use_container_width=True
    )

    st.subheader(
        "Detected Columns"
    )

    st.write(
        list(df.columns)
    )