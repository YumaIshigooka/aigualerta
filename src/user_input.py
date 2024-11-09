import streamlit as st 
import numpy as np 
import pandas as pd
import seaborn as sns

# To execute this code you can use the command 'streamlit run user_input.py'

st.set_page_config(
page_title="Aigualerta",
page_icon="🧊",
layout="wide",
initial_sidebar_state="expanded",
)

# Title and subtitle
st.title("Aigualerta")
st.subheader("Project developed by: Jinsong Liu, Mar Gutierrez, Yuma Ishigooka, Adrià León and Suleyman Hasanov")

# File upload section
st.header("Upload your data")

# Option to upload a CSV file
csv_file = st.file_uploader("Upload a CSV file", type="csv")
if csv_file is not None:
    csv_data = pd.read_csv(csv_file)
    st.write("CSV Data Preview:")
    st.write(csv_data)

# Option to upload a Parquet file
parquet_file = st.file_uploader("Upload a Parquet file", type="parquet")
if parquet_file is not None:
    parquet_data = pd.read_parquet(parquet_file)
    st.write("Parquet Data Preview:")
    st.write(parquet_data)