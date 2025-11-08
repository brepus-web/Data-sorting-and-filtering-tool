import streamlit as st
import pandas as pd
import numpy as np
import io

st.set_page_config(page_title="Lead Risk Assesment", layout='wide')
st.title("Data sorting tool")

#File upload
uploaded_file = st.file_uploader(
    "Upload data file(CSV or excel)",
    type=["csv", "xls", "xlsx"]
)
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls",".xlsx")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        
    except Exception as e:
        st.error(f"Could not read the file. Please upload a valid CSV or excel file.: {e}")
        df = None

    col_options = list(df.columns)
else:
    print("Upload a file!")

#Downloading files in CSV
csv_out = final_df.to_csv(index=False)
st.download_button("Download results(CSV)", data=csv_out, file_name="Risk_Results.csv", mime="text/csv")

#Downloading results in XLSX
excel_buffer = io.BytesIO()
final_df.to_excel(excel_buffer,index=False, engine="openpyxl")
excel_buffer.seek(0)

st.download_button("Download results(XLSX)", data = excel_buffer, file_name= "Risk_Results.xlsx", mime= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


