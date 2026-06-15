


import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Manual Data Entry",
    layout="wide"
)

st.title("📊 Select Your Data variable")

# =====================================================
# YOUR QUESTIONNAIRE VARIABLES
# =====================================================

VARIABLES = {

    "Gender": [
        "Male",
        "Female",
        "Others"
    ],

    "School Type": [
        "Government",
        "Private"
    ],

    "Smoking": [
        "Yes",
        "No"
    ],

    "Alcohol": [
        "Yes",
        "No"
    ],


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


    # ADD ALL OTHER VARIABLES HERE


# =====================================================
# ENTRY TYPE
# =====================================================

entry_type = st.radio(
    "Choose Data Entry Type",
    [
        "Questionnaire Variable",
        "Custom Variable"
    ]
)

counts = {}

# =====================================================
# QUESTIONNAIRE VARIABLE
# =====================================================

if entry_type == "Questionnaire Variable":

    selected_variable = st.selectbox(
        "Select Variable",
        list(VARIABLES.keys())
    )

    st.subheader(
        f"Enter Counts for {selected_variable}"
    )

    for category in VARIABLES[selected_variable]:

        counts[category] = st.number_input(
            category,
            min_value=0,
            value=0,
            step=1,
            key=category
        )

# =====================================================
# CUSTOM VARIABLE
# =====================================================

else:

    selected_variable = st.text_input(
        "Custom Variable Name",
        placeholder="Example: Blood Group"
    )

    num_categories = st.number_input(
        "Number of Categories",
        min_value=2,
        max_value=50,
        value=2
    )

    st.subheader(
        "Enter Categories and Counts"
    )

    for i in range(num_categories):

        col1, col2 = st.columns(2)

        with col1:

            category_name = st.text_input(
                f"Category {i+1}",
                key=f"cat_{i}"
            )

        with col2:

            category_count = st.number_input(
                f"Count {i+1}",
                min_value=0,
                value=0,
                key=f"count_{i}"
            )

        if category_name.strip():

            counts[category_name] = category_count

# =====================================================
# GENERATE DATASET
# =====================================================

if st.button("Generate Dataset"):

    if not selected_variable:

        st.error(
            "Please enter/select a variable."
        )

    elif len(counts) == 0:

        st.error(
            "Please enter categories."
        )

    else:

        df = pd.DataFrame(
            {
                "Category": list(counts.keys()),
                "Count": list(counts.values())
            }
        )

        total = df["Count"].sum()

        if total > 0:

            df["Percentage"] = round(
                (df["Count"] / total) * 100,
                2
            )

        else:

            df["Percentage"] = 0

        st.success(
            "Dataset Generated Successfully"
        )

        st.subheader(
            "Frequency Table"
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.metric(
            "Total Participants",
            int(total)
        )

        os.makedirs(
            "data/categorical",
            exist_ok=True
        )

        filename = (
            selected_variable
            .replace(" ", "_")
            .replace("/", "_")
        )

        df.to_excel(
            f"data/categorical/{filename}.xlsx",
            index=False
        )

        st.success(
            f"Saved as {filename}.xlsx"
        )