import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import openai

# ---------------------
# CONFIG
# ---------------------
st.set_page_config(page_title="KRI Risk Management", layout="wide")
OUTPUT_FOLDER = "kri_csv_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------------
# OPENAI SETUP
# ---------------------
openai.api_key = st.secrets["openai"]["api_key"]

# ---------------------
# TITLE
# ---------------------
st.title("KRI Risk Management - Excel Upload & Auto CSV")

# ---------------------
# STEP 1: UPLOAD EXCEL
# ---------------------
uploaded_file = st.file_uploader("Upload your KRI Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("Original Data Preview")
    st.dataframe(df)

    # ---------------------
    # STEP 2: GPT COLUMN MAPPING
    # ---------------------
    st.info("AI is identifying the relevant KRI columns...")

    prompt = f"""
    You are a data mapping assistant. I have an Excel file with these columns:
    {df.columns.tolist()}

    Map the columns to the following required KRI fields:
    Department, KRI Name, Value, Target, Status, Entry Date, Responsible Person.

    Reply ONLY with a JSON mapping like:
    {{
      "Department": "<original column name>",
      "KRI Name": "<original column name>",
      "Value": "<original column name>",
      "Target": "<original column name>",
      "Status": "<original column name>",
      "Entry Date": "<original column name>",
      "Responsible Person": "<original column name>"
    }}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        mapping_text = response.choices[0].message["content"]
        st.subheader("GPT Suggested Column Mapping")
        st.text(mapping_text)

        mapping = json.loads(mapping_text)
    except Exception as e:
        st.warning(f"GPT mapping failed, using original columns. Error: {e}")
        mapping = {col: col for col in df.columns}

    # ---------------------
    # STEP 3: VERIFY / EDIT MAPPING
    # ---------------------
    st.subheader("Verify / Correct Mapping")
    edited_mapping = {}
    for field, col in mapping.items():
        edited_col = st.text_input(f"{field} column:", value=col)
        edited_mapping[field] = edited_col

    # ---------------------
    # STEP 4: GENERATE STANDARDIZED CSV
    # ---------------------
    if st.button("Generate CSV"):
        try:
            standard_df = pd.DataFrame()
            for field, col in edited_mapping.items():
                standard_df[field] = df[col]

            # Auto-calculate Status if missing or unreliable
            if "Status" in standard_df.columns and "Value" in standard_df.columns and "Target" in standard_df.columns:
                standard_df["Status"] = standard_df.apply(
                    lambda row: "Green" if row["Value"] >= row["Target"]
                    else "Yellow" if row["Value"] >= 0.8*row["Target"]
                    else "Red",
                    axis=1
                )

            # Save CSV with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(OUTPUT_FOLDER, f"kri_standardized_{timestamp}.csv")
            standard_df.to_csv(output_path, index=False)
            st.success(f"CSV generated and saved to {output_path}")
            st.dataframe(standard_df)
        except Exception as e:
            st.error(f"Error generating CSV: {e}")
