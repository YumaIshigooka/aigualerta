import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# To execute this code you can use the command 'streamlit run main_page.py'

# Define the columns that are required for the transformation
EXPECTED_COLUMNS = [
    'DATETIME',
    'CONSUMPTION',
    'POLICY',
    'TECHNOLOGY',
    'DIAMETER',
    'USAGE',
    'HOUSING'
]

short_names = {
    'Pòlissa/Póliza/Policy': 'POLICY',
    'Tecnologia/Tecnología/Technology': 'TECHNOLOGY',
    'Diàmetre comptador (cm)/Diámetro contador (cm)/Counter diameter (cm)': 'DIAMETER',
    'Ús/Uso/Use': 'USAGE',
    "Tipus d'habitatge/Tipo de vivienda/Type of housing": 'HOUSING',
    'Data/Fecha/Date': 'DATETIME',
    'Índex de lectura (L/h)/Índice de lectura (L/h)/Reading index (L/h)': 'CONSUMPTION',
}

# Initialize session state for the toggle button
if "show_dump_plot" not in st.session_state:
    st.session_state["show_dump_plot"] = False  # Default is hidden

def load_csv(file):
    # Load the dataset using pandas from the uploaded file
    df = pd.read_csv(file)
    df = df.rename(columns=short_names)
    return df

def load_parquet(file):
    # Load the dataset using pandas from the uploaded file
    df = pd.read_parquet(file)
    df = df.rename(columns=short_names)
    return df

def dump_plot():
    #Example
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    st.pyplot(fig, use_container_width=False)

    #Seaborn: Seaborn builds on top of a Matplotlib figure so you can display the charts in the same way
    penguins = sns.load_dataset("penguins")
    st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))

    # Create Figure beforehand
    fig = plt.figure(figsize=(9, 7))
    sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
    plt.title("Hello Penguins!")
    st.pyplot(fig, use_container_width=False)

    # st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))


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
    df['DATETIME'] = pd.to_datetime(df['DATETIME'])

    # Extract the date and hour separately
    df['Date'] = df['DATETIME'].dt.date
    df['Hour'] = df['DATETIME'].dt.hour

    # Pivot the table so that each hour is a separate column
    df_pivot = df.pivot_table(index='Date', columns='Hour', values='CONSUMPTION')

    # Rename columns as hour0, hour1, ..., hour23
    df_pivot.columns = [f'hour{int(hour)}' for hour in df_pivot.columns]

    # Reset index to make Date a column
    df_pivot = df_pivot.reset_index()

    # Deduplicate rows based on 'Date' and keep relevant columns
    df_deduped = df.drop_duplicates(subset='Date')[['Date', 'POLICY', 'TECHNOLOGY', 'DIAMETER', 'USAGE', 'HOUSING']]


    # Merge the pivot table with the deduplicated columns
    df_final = pd.merge(df_pivot, df_deduped, on='Date', how='left')

    # Reorder columns
    cols = ['POLICY', 'Date'] + [col for col in df_final.columns if col not in ['POLICY', 'Date']]
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

def load_page():
    st.set_page_config(
    page_title="Aigualerta",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

    # Title and subtitle
    st.title("Aigualerta")
    st.subheader("Project developed by: Jinsong Liu, Marc Gutierrez, Yuma Ishigooka, Adrià León and Suleyman Hasanov")

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
            st.write(df_cleaned.head())

    # Option to upload a Parquet file
    parquet_file = st.file_uploader("Upload a Parquet file", type="parquet")
    if parquet_file is not None:
        df = load_parquet(parquet_file)
        st.write("Parquet Data Preview:")
        st.write(df.head())  # Show initial preview of uploaded data
        
        # Button to trigger transformation and cleaning for Parquet data
        if st.button("Transform and Clean Parquet Data"):
            df_cleaned = transform_and_clean_data(df)
            st.write(df_cleaned.head())
    
    # Toggle button to show/hide dump_plot
    if st.button("Toggle dump plot"):
        # Toggle the visibility state
        st.session_state["show_dump_plot"] = not st.session_state["show_dump_plot"]

    # Conditionally display dump_plot based on session state
    if st.session_state["show_dump_plot"]:
        dump_plot()
    
load_page()