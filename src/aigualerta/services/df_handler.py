import pickle
from aigualerta import constants
import pandas as pd
from sklearn.calibration import LabelEncoder
import streamlit as st

model = pickle.load(open(constants.model_path, 'rb'))

def rename_columns(df):
    return df.rename(columns = constants.short_names)

def transform_columns(df):

    # Convert 'Data/Fecha/Date' column to datetime format
    df['DATETIME'] = pd.to_datetime(df['DATETIME'])

    df['WEEKDAY'] = df['DATETIME'].dt.dayofweek
    df['HOUR'] = df['DATETIME'].dt.hour

    # df = df.drop(columns=['HOUR/DATE'])

    # Add the flow (gradient of consumption) as a column.
    df['FLOW'] = df.groupby('POLICY')['CONSUMPTION'].diff()
    df = df.dropna(subset=["FLOW"])

    return df

def is_missing_columns(df):
    # Check if the required columns are present in the dataframe
    missing_columns = [col for col in constants.EXPECTED_COLUMNS if col not in df.columns]
    
    if missing_columns:
        # If there are missing columns, display the missing ones and the expected columns
        st.warning(f"The following columns are missing from the dataset: {', '.join(missing_columns)}")
        st.write("Expected columns in the dataset:")
        st.write(constants.EXPECTED_COLUMNS)
        return True

    return False

def drop_defective_rows(df):
    # Remove bad data (gradient is less than 0, it is impossible that water goes backwards)
    negative_policies = df[df['FLOW'] < 0]['POLICY'].values
    df = df[~df['POLICY'].isin(negative_policies)]

    # Null entries removal
    df = df.dropna(how='any')

    return df

def prepare_data(df):
    # Button to trigger transformation and cleaning for CSV data
    df = rename_columns(df)
    if not is_missing_columns(df):
        df = transform_columns(df)
        df = drop_defective_rows(df)
        return df
    return None
    
def setup_input(df, window_size = 4, output_path=None):
    # Create a generator to yield rows for each window
    def generate_rows():
        for policy, group in df.groupby('POLICY'):
            # Convert columns to NumPy arrays for efficient slicing
            flows = group['FLOW'].to_numpy()
            technology = group['TECHNOLOGY'].to_numpy()
            usage = group['USAGE'].to_numpy()
            housing = group['HOUSING'].to_numpy()
            consumption = group['CONSUMPTION'].to_numpy()
            hour_date = group['DATETIME'].to_numpy()
            weekday = group['WEEKDAY'].to_numpy()
            hours = group['HOUR'].to_numpy()

            # Generate sliding windows
            for i in range(len(flows) - window_size + 1):
                row = {
                    'POLICY': policy,
                    'TECHNOLOGY': technology[i],
                    'USAGE': usage[i],
                    'HOUSING': housing[i],
                    'CONSUMPTION': consumption[i],
                    'DATETIME': hour_date[i],
                    'WEEKDAY': weekday[i],
                    'START_HOUR': hours[i],
                }
                # Add flow values for the window
                for j in range(window_size):
                    row[f'FLOW_{j + 1}'] = flows[i + j]
                yield row

    # Write to file or return as DataFrame
    if output_path:
        pd.DataFrame.from_records(generate_rows()).to_parquet(output_path, index=False)
        print(f"Saved processed data to {output_path}")
        return None
    else:
        df = pd.DataFrame.from_records(generate_rows())
        return df

def predict(df):
    # Dynamically construct the FLOW column names
    flow_columns = [f"FLOW_{i}" for i in range(1, constants.WINDOW_SIZE + 1)]
    # Define the full feature list
    base_features = ['USAGE', 'HOUSING', 'WEEKDAY', 'START_HOUR']
    features = base_features + flow_columns

    # Select features and target
    X = df[features]
    label_encoders = {}

    for col in X.select_dtypes(include='object').columns:  # Select categorical columns
        le = LabelEncoder()
        X.loc[:, col] = le.fit_transform(X[col])  # Use .loc[] for explicit assignment
        label_encoders[col] = le

    y = model.predict(X)
    df['LEAK'] = y
    return df

def compute_results(df, loading_bar):
    df = prepare_data(df)
    st.session_state.setup_df = df

    loading_bar.progress(33 + 1, text="Setting up")
    df = setup_input(df)
    st.session_state.input_df = df
    
    loading_bar.progress(66, text="Predicting")
    df = predict(df)
    st.session_state.predicted_df = df

    loading_bar.progress(100, text="Done!")
    st.balloons()
    loading_bar.empty()
    return df