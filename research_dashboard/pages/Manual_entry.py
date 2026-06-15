import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("📊 Manual Data Entry")

st.markdown(
    "Select a questionnaire variable and enter the frequency/count for each category."
)

# =====================================================
# QUESTIONNAIRE VARIABLES
# =====================================================

VARIABLES = {

    "Gender": [
        "Male",
        "Female",
        "Others"
    ],

    "Class": [
        "9",
        "10",
        "11",
        "12"
    ],

    "School Type": [
        "Government",
        "Private"
    ],

    "Father Occupation": [
        "Professional",
        "Skilled",
        "Semi Skilled",
        "Unskilled",
        "Business",
        "Agriculture",
        "Others"
    ],

    "Father Education": [
        "Illiterate",
        "Primary",
        "Middle",
        "Secondary",
        "Higher Secondary",
        "Graduate",
        "Postgraduate"
    ],

    "Mother Occupation": [
        "Homemaker",
        "Professional",
        "Skilled",
        "Business",
        "Others"
    ],

    "Mother Education": [
        "Illiterate",
        "Primary",
        "Middle",
        "Secondary",
        "Higher Secondary",
        "Graduate",
        "Postgraduate"
    ],

    "Comorbidity": [
        "Yes",
        "No"
    ],

    "Disease Type": [
        "Diabetes",
        "Hypertension",
        "Asthma",
        "Thyroid",
        "Others"
    ],

    "Past 3 Months Illness": [
        "Yes",
        "No"
    ],

    "Medication": [
        "Yes",
        "No"
    ],

    "Family Illness": [
        "Yes",
        "No"
    ],

    "Unlimited Data": [
        "Yes",
        "No"
    ],

    "Internet Access": [
        "Yes",
        "No"
    ],

    "Sleep Affected": [
        "Yes",
        "No"
    ],

    "Health Information Source": [
        "Parents",
        "AI Sources",
        "Google Search",
        "Social Media",
        "Authorized Websites"
    ],

    "Health Information Provider": [
        "Mother",
        "Father",
        "Sibling",
        "Grandparents",
        "Relatives",
        "Friends"
    ],

    "Health Topics Discussed": [
        "Nutrition",
        "Hygiene",
        "Mental Health",
        "Sexual Health",
        "Fitness",
        "Disease Prevention",
        "Substance Abuse"
    ],

    "Health Decision Maker": [
        "Self",
        "Parents",
        "Grandparents",
        "Joint Decision"
    ],

    "School Health Education": [
        "Yes",
        "No"
    ],

    "Smoking": [
        "Yes",
        "No"
    ],

    "Alcohol": [
        "Yes",
        "No"
    ],

    "Substance Use": [
        "Yes",
        "No"
    ]
}

# =====================================================
# VARIABLE SELECTION
# =====================================================

selected_variable = st.selectbox(
    "Select Variable",
    list(VARIABLES.keys())
)

st.subheader(f"Enter Counts for {selected_variable}")

categories = VARIABLES[selected_variable]

counts = {}

for category in categories:

    counts[category] = st.number_input(
        f"{category}",
        min_value=0,
        value=0,
        step=1
    )

# =====================================================
# GENERATE TABLE
# =====================================================

if st.button("Generate Dataset"):

    data = {
        "Category": list(counts.keys()),
        "Count": list(counts.values())
    }

    df = pd.DataFrame(data)

    total = df["Count"].sum()

    if total > 0:
        df["Percentage"] = round(
            (df["Count"] / total) * 100,
            2
        )
    else:
        df["Percentage"] = 0

    st.success("Dataset Generated")

    st.subheader("Frequency Table")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Create folder

    os.makedirs(
        "data/categorical",
        exist_ok=True
    )

    filename = selected_variable.replace(
        " ",
        "_"
    )

    df.to_excel(
        f"data/categorical/{filename}.xlsx",
        index=False
    )

    st.success(
        f"Saved as {filename}.xlsx"
    )

    st.subheader("Summary")

    st.metric(
        "Total Participants",
        int(total)
    )