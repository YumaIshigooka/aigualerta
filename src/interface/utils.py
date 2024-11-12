import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os # Library to auto-detect the tab files automatically
import importlib.util # Library to auto-detect the tab files automatically

TABS_DIR = os.path.join(os.path.dirname(__file__), "tabs")

def load_tabs_from_directory(directory):
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    tabs = {}
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename.startswith("tab"):
            tab_index = int(filename[3:-3])  # Extract the number from 'tabX.py'
            module_name = filename[:-3]
            module_spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, filename))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            tabs[tab_index] = module
    return tabs

tabs = load_tabs_from_directory(TABS_DIR)

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

def load_csv(file):

    """
    Loads a CSV file into a pandas DataFrame and renames the columns according to the short_names mapping.

    Args:
    - file: The CSV file to load.

    Returns:
    - pd.DataFrame: The loaded DataFrame with renamed columns.
    """

    df = pd.read_csv(file)
    df = df.rename(columns=short_names)
    return df

def load_parquet(file):

    """
    Loads a Parquet file into a pandas DataFrame and renames the columns according to the short_names mapping.

    Args:
    - file: The Parquet file to load.

    Returns:
    - pd.DataFrame: The loaded DataFrame with renamed columns.
    """

    df = pd.read_parquet(file)
    df = df.rename(columns=short_names)
    return df

def upload_csv():    

    """
    Displays a file uploader for uploading a CSV file and loads the data into a DataFrame if uploaded.

    Returns:
    - pd.DataFrame or None: The uploaded CSV data as a DataFrame, or None if no file is uploaded.
    """

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        df = load_csv(csv_file)
        st.write("CSV data preview:")
        st.write(df.head())
        return df
    return None

def upload_parquet():

    """
    Displays a file uploader for uploading a Parquet file and loads the data into a DataFrame if uploaded.

    Returns:
    - pd.DataFrame or None: The uploaded Parquet data as a DataFrame, or None if no file is uploaded.
    """

    parquet_file = st.file_uploader("Upload a Parquet file", type="parquet")
    if parquet_file is not None:
        df = load_parquet(parquet_file)
        st.write("Parquet Data Preview:")
        st.write(df.head())
        return df
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

    if df_csv is not None:
        df = df_csv
    elif df_parquet is not None:
        df = df_parquet
    else:
        df = None 

    if df is not None:
        return df

def init_session_attr(session_state):
    if "show_dump_plot" not in session_state:
        st.session_state["show_dump_plot"] = False  # Default is hidden
        
def adapt_data(df):

    def transform_and_clean_data(df):
        # TODO
        return df
    
    # Button to trigger transformation and cleaning for CSV data
    if st.button("Transform and clean uploaded data"):
        df = transform_and_clean_data(df)
        st.write(df.head())
        return df

def dump_plot_example():
    def dump_plot_generation():
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
    # Toggle button to show/hide dump_plot
    if st.button("Toggle dump plot"):
        # Toggle the visibility state
        st.session_state["show_dump_plot"] = not st.session_state["show_dump_plot"]

    # Conditionally display dump_plot based on session state
    if st.session_state["show_dump_plot"]:
        dump_plot_generation()

def load_page(i):
    
    init_session_attr(st.session_state)
    tabs[i].load_page()