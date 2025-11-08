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
