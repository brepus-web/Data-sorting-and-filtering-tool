import streamlit as st
import pandas as pd
import io
import re

st.set_page_config(page_title="Data sorting and filtering tool.", layout='wide')
st.title("Data sorting and filtering tool")

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
    except Exception as e:
        st.error(f"Could not read the file. Please upload a valid CSV or excel file.: {e}")
        df = None
    #Filtering
    if df is not None:
        #Filtering columns
        st.subheader("Column Filter")
        df = df.dropna(how='all')
        df = df.dropna(axis=1,how='all' )
        df = df.reset_index(drop=True)
        filter_option = st.radio("Do you want to filter columns?",["No.Don't Filter.","Yes.Filter."],index = 0)
        filtered_df = df.copy()
        if filter_option == "Yes.Filter.":
            st.write("Select desired columns")
            all_columns = list(df.columns)
            selected_columns = st.multiselect("Choose columns you want to include in your final dataset:", options=all_columns, default=all_columns)
            if selected_columns:
                filtered_df = df[selected_columns].copy()
                st.success(f"Selected {len(selected_columns)} out of {len(all_columns)}.")
        else:
            filtered_df = df.copy()
            st.info("Keeping all columns in original dataset.")
        #Filtering redundant values
        st.subheader("Redundant data filter")
        check_column = st.selectbox("Select column to analyse for redundant values:",options=filtered_df.columns)
        if check_column:
            value_number = filtered_df[check_column].value_counts()
            redundant_values = value_number[value_number > 1]
            if len(redundant_values) > 0:
                st.info(f"Found {len(redundant_values)} with duplicates in {check_column}.")
                st.write("Redundant values:")
                redundant_df = pd.DataFrame({'Value': redundant_values.index, 'Count':redundant_values.values})
                st.dataframe(redundant_df, use_container_width=True)
                removal_options = st.radio("Choose how to handle duplicates:", options=["Keep all rows", "Keep first occurence of each value",
                                                                                        "Keep last occurence of each value","Remove all duplicate rows entirely"],
                                                                                        index=0)
                if removal_options != "Keep all rows":
                    original_rows = len(filtered_df)
                    if removal_options == "Keep first occurence of each value":
                        filtered_df = filtered_df.drop_duplicates(subset=[check_column], keep='first')
                    elif removal_options == "Keep last occurence of each value":
                        filtered_df = filtered_df.drop_duplicates(subset=[check_column], keep='last')
                    elif removal_options == "Remove all duplicate rows entirely":
                        filtered_df = filtered_df.drop_duplicates(subset=[check_column], keep=False)
                    removed_rows = original_rows - len(filtered_df)
                    st.info(f"Removed {removed_rows} rows. Dataset now has {len(filtered_df)} rows.")
            else:
                st.info("No redundant values found.")
        #Character Filtering
        st.subheader("Character Based Filtering")
        char_filter_column = st.selectbox("Select column for character filtering.", options=filtered_df.columns,key='char_filter')
        if char_filter_column:
            filter_type = st.radio("Filter type:", ["Removed characters","Keep only the characters","Keep all the rows with the character"], key='filter_type')
            characters = st.text_input("Enter characters to filter")
            if characters:
                if filter_type == "Removed characters":
                    filtered_df[char_filter_column] = filtered_df[char_filter_column].astype(str)
                    for c in characters:
                        filtered_df[char_filter_column] = filtered_df[char_filter_column].str.replace(c,'',regex=False)
                    st.success(f"Removed {characters}  from column {char_filter_column}")
                elif filter_type == "Keep only the characters":
                    filtered_df[char_filter_column] = filtered_df[char_filter_column].astype(str)
                    pattern = f'[^{re.escape(characters)}]'
                    filtered_df[char_filter_column] = filtered_df[char_filter_column].str.replace(pattern,'',regex=True)
                    st.success(f"Kept only the characters , {characters} in column {char_filter_column}")
                else:
                    includes_char = filtered_df[char_filter_column].astype(str).apply(lambda x: any (c in x for c in characters))
                    filtered_df = filtered_df[includes_char].reset_index(drop=True)
                    st.success(f"Kept only rows containg characters {characters} in column {char_filter_column}.")
                    
        #Sorting
        column_options = list(filtered_df.columns)
        sort_column = st.selectbox("Select Column to Sort By", column_options, index = 0)
        sorted_df = pd.DataFrame()
        sort_direction = st.radio("Sort Direction",["Ascending", "Descending"])
        if sort_direction == 'Ascending':
            ascending = True
        else:
            ascending = False
        sort_type = st.radio("Sort As",["Alphanumeric", "Text", "Number"])
        sort = True
        if sort_type == "Text":
            try:
                has_digits = filtered_df[sort_column].astype(str).str.contains(r'\d',na=False).any()
                numeric_values = pd.to_numeric(filtered_df[sort_column], errors="coerce")
                has_numbers = numeric_values.notna().any()
                if has_digits or has_numbers:
                    st.warning("This column contains numeric values. Sorting may produce unexpected results.(example: '10' may come before '2')")
                    button1,button2 = st.columns(2)
                    with button1:
                        yes = st.button("Proceed anyway.")
                    with button2:
                        no = st.button( "Do not proceed")
                    if yes:
                        sort = True
                    elif no:
                        sort = False
                        st.info("Choose a different sorting method.")
                    else:
                        st.stop()
            except Exception as e:
                st.error("Error analysing column:", e)
        elif sort_type == "Number":
            try:
                numeric_test = pd.to_numeric(filtered_df[sort_column], errors='coerce')
                has_string = numeric_test.isna().any()
                if has_string:
                    st.error("This column contains string values which cannot be sorted alphabetically.")
                    st.info("Pleas use Alphanumeric or Text sorting method instead.")
                    sort = False
                    st.stop()
            except Exception as e:
                st.error(f"Error analysing column: {e}")

        if sort:
            if sort_type == "Alphanumeric":
                sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending, key=Alphanumeric_key).reset_index(drop=True)
            elif sort_type == "Text":
                sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending, key=lambda x:x.astype(str).str.lower()).reset_index(drop=True)
            elif sort_type == "Number":
                sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending, key=lambda x:pd.to_numeric(x,errors="coerce")).reset_index(drop=True)
                
            #Displaying Results
            st.subheader("Sorted Data")
            st.dataframe(sorted_df)

            #Data Visualisation
            st.subheader("Two-column comparision")
            col1,col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("Select X-axis column.",filtered_df.columns,key='x-axis')
            with col2:
                y_axis = st.selectbox("Select Y-axis column.", filtered_df.columns,key='y-axis')
            if x_axis and y_axis:
                try:
                    comparison_data = pd.DataFrame({'X':filtered_df[x_axis],'Y':filtered_df[y_axis]}).dropna()
                    if len(comparison_data) > 0:
                        tab1,tab2,tab3 = st.tabs(["Line Graph","Scatter Plot","Bar Chart"])
                        with tab1:
                            st.line_chart(comparison_data.set_index('X')['Y'])
                            st.caption(f"Line graph: {y_axis} vs {x_axis}")
                        with tab2:
                            st.scatter_chart(comparison_data, x='X',y="Y")
                            st.caption(f"Scatter Plot: {y_axis} vs {x_axis}")
                        with tab3:
                            st.bar_chart(comparison_data.set_index('X')['Y'])
                            st.caption(f"Bar Chart: {y_axis} vs {x_axis}")
                    else:
                        st.warning("No valid data points for comparison")
                except Exception as e:
                    st.error(f"Could nor create comparison chart: {e}")
            #Downloading files in CSV
            csv_out = sorted_df.to_csv(index=False)
            st.download_button("Download results(CSV)", data=csv_out, file_name="Sorted_File.csv", mime="text/csv")

            #Downloading results in XLSX
            excel_buffer = io.BytesIO()
            sorted_df.to_excel(excel_buffer,index=False, engine="openpyxl")
            excel_buffer.seek(0)
            st.download_button("Download results(XLSX)", data = excel_buffer, file_name= "Sorted_File.xlsx", mime= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    

