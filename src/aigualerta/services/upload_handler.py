from aigualerta import constants
from pandas import read_parquet, read_csv
import streamlit as st

def upload_csv():    
    """
    Displays a file uploader for uploading a CSV file and loads the data into a DataFrame if uploaded.

    Returns:
    - pd.DataFrame or None: The uploaded CSV data as a DataFrame, or None if no file is uploaded.
    """
    csv_file = st.file_uploader("Upload a CSV file", type="csv")

    if csv_file is not None:
        return read_csv(csv_file)
    return None

def upload_parquet():
    """
    Displays a file uploader for uploading a Parquet file and loads the data into a DataFrame if uploaded.

    Returns:
    - pd.DataFrame or None: The uploaded Parquet data as a DataFrame, or None if no file is uploaded.
    """
    parquet_file = st.file_uploader("Upload a Parquet file", type="parquet")

    if parquet_file is not None:
        return read_parquet(parquet_file)
    return None

def upload_data():
    """
    Handles the data upload process for either CSV or Parquet files.

    Returns:
    - pd.DataFrame or None: The uploaded data as a DataFrame, or None if no file is uploaded.
    """
    st.header("Upload your data")

    df_csv = upload_csv()
    df_parquet = upload_parquet()

    return df_csv or df_parquet