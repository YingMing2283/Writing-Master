import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Initialize GPT API
client = st.secrets["API_KEY"]

# Target folder to save CSVs
OUTPUT_FOLDER = "kri_csv_output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

st.title("KRI Risk Management - Excel Upload & Auto CSV")

# Step 1: Upload Excel
uploaded_file = st.file_uploader("Upload your KRI Excel file", type=["xlsx"])
if uploaded_file:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    st.subheader("Original Data Preview")
    st.dataframe(df)

    # Step 2: GPT API to identify columns
    st.info("AI is identifying the relevant KRI columns...")

    prompt = f"""
    You are a data mapping assistant. I have an Excel file with these columns:
    {df.columns.tolist()}

    Map the columns to the following required KRI fields:
    Department, KRI Name, Value, Target, Status, Entry Date, Responsible Person.

    Reply with a JSON mapping like:
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    mapping_text = response.choices[0].message.content
    st.subheader("GPT Suggested Column Mapping")
    st.text(mapping_text)

    # Step 3: Let user confirm mapping (simplified)
    st.subheader("Verify / Correct Mapping")
    import json
    try:
        mapping = json.loads(mapping_text)
    except:
        st.warning("Failed to parse GPT response. Please edit manually.")
        mapping = {col: col for col in df.columns}

    # Display editable mapping
    edited_mapping = {}
    for field, col in mapping.items():
        edited_col = st.text_input(f"{field} column:", value=col)
        edited_mapping[field] = edited_col

    # Step 4: Generate standardized CSV
    if st.button("Generate CSV"):
        try:
            standard_df = pd.DataFrame()
            for field, col in edited_mapping.items():
                standard_df[field] = df[col]

            # Optional: calculate Status automatically if missing
            if "Status" in standard_df.columns:
                standard_df["Status"] = standard_df.apply(
                    lambda row: "Green" if row["Value"] >= row["Target"]
                    else "Yellow" if row["Value"] >= 0.8*row["Target"]
                    else "Red",
                    axis=1
                )

            # Save CSV to folder
            output_path = os.path.join(OUTPUT_FOLDER, "kri_standardized.csv")
            standard_df.to_csv(output_path, index=False)
            st.success(f"CSV generated and saved to {output_path}")
            st.dataframe(standard_df)
        except Exception as e:
            st.error(f"Error generating CSV: {e}")
