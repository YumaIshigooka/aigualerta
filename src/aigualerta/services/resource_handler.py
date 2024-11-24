import base64
import os
import streamlit as st

def load_file(file_path: str):
    """
    Loads file and returns its reference
    """
    with open(get_absolute_path(file_path), "r") as f:
        return f.read()

def get_absolute_path(path: str):
    """
    Returns absolute path/to/src/aigualerta/
    """
    base_path = os.path.dirname(__file__)+'/../'  # path/to/src/aigualerta/
    absolute_path = os.path.join(base_path, path)
    return absolute_path

def load_image_as_base64(file_path):
    """
    Loads an image file and returns it as a base64 encoded string.
    """
    path = get_absolute_path(file_path)
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"

def get_theme():
    theme = st.session_state.theme
    if theme is None or theme['base'] != 'dark':
        return 'light'

    return 'dark'

def theme():
    return st.session_state.theme