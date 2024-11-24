import streamlit as st
from aigualerta.services.upload_handler import upload_data
from aigualerta.services.df_handler import is_df_loaded

def show_df(df, message=""):
    if message != "":
        st.write(message)
    st.write(df)

def is_process_data():
    if is_df_loaded():
        return st.button('Process data')
    
def show_uploader():
    if not is_df_loaded():
        st.session_state.user_df = upload_data()
        return False
    return True