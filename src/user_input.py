import streamlit as st 
import pandas as pd
import seaborn as sns
import numpy as np

# To execute this code you can use the command 'streamlit run user_input.py'

st.set_page_config(
    page_title="Aigualerta",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define the columns that are required for the transformation
EXPECTED_COLUMNS = [
    'Data/Fecha/Date',
    'Índex de lectura (L/h)/Índice de lectura (L/h)/Reading index (L/h)',
    'Pòlissa/Póliza/Policy',
    'Tecnologia/Tecnología/Technology',
    'Diàmetre comptador (cm)/Diámetro contador (cm)/Counter diameter (cm)',
    'Ús/Uso/Use',
    'Tipus d\'habitatge/Tipo de vivienda/Type of housing'
]

def load_csv(file):
    # Load the dataset using pandas from the uploaded file
    df = pd.read_csv(file)
    return df

def load_parquet(file):
    # Load the dataset using pandas from the uploaded file
    df = pd.read_parquet(file)
    return df

def transform_and_clean_data(df):
    # Check if the required columns are present in the dataframe
    missing_columns = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    
    if missing_columns:
        # If there are missing columns, display the missing ones and the expected columns
        st.warning(f"The following columns are missing from the dataset: {', '.join(missing_columns)}")
        st.write("Expected columns in the dataset:")
        st.write(EXPECTED_COLUMNS)
        return None

    # Proceed with the transformation if all columns are present
    # Convert 'Data/Fecha/Date' column to datetime format
    df['Data/Fecha/Date'] = pd.to_datetime(df['Data/Fecha/Date'])

    # Extract the date and hour separately
    df['Date'] = df['Data/Fecha/Date'].dt.date
    df['Hour'] = df['Data/Fecha/Date'].dt.hour

    # Pivot the table so that each hour is a separate column
    df_pivot = df.pivot_table(index='Date', columns='Hour', values='Índex de lectura (L/h)/Índice de lectura (L/h)/Reading index (L/h)')

    # Rename columns as hour0, hour1, ..., hour23
    df_pivot.columns = [f'hour{int(hour)}' for hour in df_pivot.columns]

    # Reset index to make Date a column
    df_pivot = df_pivot.reset_index()

    # Deduplicate rows based on 'Date' and keep relevant columns
    df_deduped = df.drop_duplicates(subset='Date')[['Date', 'Pòlissa/Póliza/Policy', 'Tecnologia/Tecnología/Technology',
                                                    'Diàmetre comptador (cm)/Diámetro contador (cm)/Counter diameter (cm)',
                                                    'Ús/Uso/Use', 'Tipus d\'habitatge/Tipo de vivienda/Type of housing']]

    # Merge the pivot table with the deduplicated columns
    df_final = pd.merge(df_pivot, df_deduped, on='Date', how='left')

    # Reorder columns
    cols = ['Pòlissa/Póliza/Policy', 'Date'] + [col for col in df_final.columns if col not in ['Pòlissa/Póliza/Policy', 'Date']]
    df_final = df_final[cols]

    # Drop rows with NaNs in any hourly column
    hour_columns = [f'hour{hour}' for hour in range(24)]
    df_cleaned = df_final.dropna(subset=hour_columns, how='any')

    # Display the cleaned data info
    st.write("Data Information after Cleaning:")
    st.write(df_cleaned.info())
    
    # Display the cleaned data preview
    st.write("Cleaned Data Preview:")
    st.write(df_cleaned.head())

    return df_cleaned

# Title and subtitle
st.title("Aigualerta")
st.subheader("Project developed by: Jinsong Liu, Mar Gutierrez, Yuma Ishigooka, Adrià León and Suleyman Hasanov")

# File upload section
st.header("Upload your data")

# Option to upload a CSV file
csv_file = st.file_uploader("Upload a CSV file", type="csv")
if csv_file is not None:
    df = load_csv(csv_file)
    st.write("CSV Data Preview:")
    st.write(df.head())  # Show initial preview of uploaded data
    
    # Button to trigger transformation and cleaning for CSV data
    if st.button("Transform and Clean CSV Data"):
        df_cleaned = transform_and_clean_data(df)

# Option to upload a Parquet file
parquet_file = st.file_uploader("Upload a Parquet file", type="parquet")
if parquet_file is not None:
    df = load_parquet(parquet_file)
    st.write("Parquet Data Preview:")
    st.write(df.head())  # Show initial preview of uploaded data
    
    # Button to trigger transformation and cleaning for Parquet data
    if st.button("Transform and Clean Parquet Data"):
        df_cleaned = transform_and_clean_data(df)
