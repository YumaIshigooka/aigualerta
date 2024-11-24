import streamlit as st
from streamlit_theme import st_theme
from aigualerta.services.resource_handler import load_image_as_base64, load_file, get_theme

def load_page():
    """"
    Loads tab0, which contains the welcome page
    """
    markdown_content = load_file('resources/welcome_page.md')

    markdown_content = setup_welcome_page(markdown_content)

    st.markdown(markdown_content, unsafe_allow_html=True)

def setup_welcome_page(md):
    theme = get_theme()
    
    # Load images and encode them as base64
    aigualerta_logo = load_image_as_base64("resources/aigualerta_logo.png")
    upf_logo        = load_image_as_base64("resources/" + theme + "/upf_logo.png")
    ab_logo         = load_image_as_base64("resources/" + theme + "/ab_logo.png")

    # Replace placeholders in the Markdown with base64 image data
    md = md.replace("{aigualerta_logo}", aigualerta_logo)
    md = md.replace("{upf_logo}", upf_logo)
    md = md.replace("{ab_logo}", ab_logo)

    return md
