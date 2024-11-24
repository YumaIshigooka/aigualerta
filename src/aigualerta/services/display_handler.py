import streamlit as st
from aigualerta.services.upload_handler import upload_manager, is_user_df_loaded
from aigualerta.services.df_handler import compute_results
from aigualerta.services.utils_plot import plot_durations

def show_df(df, message=""):
    """
    Writes some text, and then prints the df
    """
    if message != "":
        st.write(message)
    st.write(df)

def display_input_data():
    show_df(st.session_state.user_df)

def display_predicted_results():
    show_df(st.session_state.predicted_df)

def display_leak_rows():
    predicted_df = st.session_state.predicted_df
    st.write(predicted_df[predicted_df['LEAK']])

def subtab_handler():
    subtab1, subtab2, subtab3, subtab4 = st.tabs(["Input Data", "Predicted Results", "Rows that have leak", "Statistics"])

    with subtab1:
        display_input_data()

    with subtab2:
        display_predicted_results()

    with subtab3:
        display_leak_rows()

    with subtab4:
        plot_durations(st.session_state.predicted_df)


def is_process_data_button_pressed():
    if is_user_df_loaded():
        return st.button('Process data')
    
def user_df_has_been_uploaded():
    """
    Applies upload logic and returns whether a df has been
    uploaded correctly
    """
    upload_manager()
    return is_user_df_loaded()

def show_results():
    loading_bar = st.progress(1, text="Preparing")
    compute_results(st.session_state.user_df, loading_bar)
    subtab_handler()
