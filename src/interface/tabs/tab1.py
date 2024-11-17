import streamlit as st
import utils

def load_page():

    df = utils.upload_data()

    if df is not None:
        df = utils.setup_data(df)
        st.subheader("This is the adapted dataset")
        st.write(df.head())
        if df is not None:
            df = utils.setup_input(df)
            if df is not None:
                if st.button("Predict"):
                    df = utils.predict(df)
        
    else: 
        st.write("If you are willing to **load your dataset from the data folder** please refer to the *data from folder* tab")