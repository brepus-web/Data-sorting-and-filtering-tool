import streamlit as st
import pandas as pd
import numpy as np
import io
import re

st.set_page_config(page_title="Lead Risk Assesment", layout='wide')
st.title("Data sorting tool")

def Alphanumeric_key(series):
    def convert_single_value(value):
        if pd.isna(value) or value =="":
            return[""]
        def convert(text):
            return int(text) if text.isdigit() else text.lower()
        return [convert(c) for c in re.split('([0-9]+)', str(value))]
    return series.apply(convert_single_value)


#File upload
uploaded_file = st.file_uploader(
    "Upload data file(CSV or excel)",
    type=["csv", "xls", "xlsx"]
)
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, index_col=False)
        elif uploaded_file.name.endswith((".xls",".xlsx")):
            df = pd.read_excel(uploaded_file, engine="openpyxl", index_col=False)
        df = df.dropna(how='all')
    except Exception as e:
        st.error(f"Could not read the file. Please upload a valid CSV or excel file.: {e}")
        df = None
    col_options = list(df.columns)
    sort_col = st.selectbox("Select Column to Sort By", col_options, index = 0)
    sorted_df = pd.DataFrame()
        
    #Sorting
    sort_direction = st.radio("Sort Direction",["Ascending", "Descending"])
    ascending = sort_direction == "Ascending"
    sort_type = st.radio("Sort As",["Alphanumeric", "Text", "Number"])
    proceed_sort = True
    if sort_type == "Text":
        try:
            has_digits = df[sort_col].astype(str).str.contains(r'\d',na=False).any()
            numeric_values = pd.to_numeric(df[sort_col], errors="coerce")
            has_numbers = numeric_values.notna().any()
            if has_digits or has_numbers:
                st.warning("This column contains numeric values. Sorting may produce unexpected results.(example: '10' may come before '2')")
                col1,col2 = st.columns(2)
                with col1:
                    proceed_yes = st.button("Proceed anyway.")
                with col2:
                    proceed_no = st.button( "Do not proceed")
                if proceed_yes:
                    proceed_sort = True
                elif proceed_no:
                    proceed_sort = False
                    st.info("Choose a different sorting method.")
                else:
                    st.stop()
        except Exception as e:
            st.error("Error analysing column:", e)
    elif sort_type == "Number":
        try:
            numeric_test = pd.to_numeric(df[sort_col], errors='coerce')
            has_string = numeric_test.isna().any()
            if has_string:
                st.error("This column contains string values which cannot be sorted alphabetically.")
                st.info("Pleas use Alphanumeric or Text sorting method instead.")
                proceed_sort = False
                st.stop()
        except Exception as e:
            st.error("Error analysing column:", e)

    if proceed_sort:
        if sort_type == "Alphanumeric":
            sorted_df = df.sort_values(by=sort_col, ascending=ascending, key=Alphanumeric_key)
        elif sort_type == "Text":
            sorted_df = df.sort_values(by=sort_col, ascending=ascending, key=lambda x:x.astype(str).str.lower())
        elif sort_type == "Number":
            sorted_df = df.sort_values(by=sort_col, ascending=ascending, key=lambda x:pd.to_numeric(x,errors="coerce"))
            
        #Displaying Results
        st.subheader("Sorted Data")
        st.dataframe(sorted_df)

        #Downloading files in CSV
        csv_out = sorted_df.to_csv(index=False)
        st.download_button("Download results(CSV)", data=csv_out, file_name="Sorted_File.csv", mime="text/csv")

        #Downloading results in XLSX
        excel_buffer = io.BytesIO()
        sorted_df.to_excel(excel_buffer,index=False, engine="openpyxl")
        excel_buffer.seek(0)
        st.download_button("Download results(XLSX)", data = excel_buffer, file_name= "Sorted_File.xlsx", mime= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

