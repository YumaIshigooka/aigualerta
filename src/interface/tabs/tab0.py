import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, src_dir)

import streamlit as st
from interface import utils

def load_page():

    st.title("Aigualerta")
    utils.load_image("aigualerta_logo.png", width=150, center=True)

    st.subheader("Project Summary")
    st.write("""
    The goal of this website is to efficiently detect potential water leaks and predict future issues in pipelines.
    By analyzing fluctuations in water flow, the system aims to identify pipes that may develop defects or other damages over time.
    Additionally, this tool helps in monitoring and regulating excessive water consumption, whether due to human error or leaks, ensuring the optimal and sustainable use of this precious resource.

    We have initially used the Aigües de Barcelona (AB) dataset to train our gradient boosting model and generate accurate predictions.

    In the following sections of this website, you can upload your own .csv or .parquet file containing relevant data, and our system will help you make predictions about potential water leaks or abnormal water consumption patterns in your data.
    """)

    st.subheader("Authors")
    st.write("""
        Jinsong Liu
              
        Marc Gutierrez
             
        Yuma Ishigooka
             
        Adrià León
             
        Suleyman Hasanov
    """)

    st.subheader("Acknowledgements")

    utils.load_image("upf_logo.png", width = 300)
    st.write("""
    To [Miquel Olvier](https://www.linkedin.com/in/miquel-oliver/) for his contributions and valuable insights into this project.
    """)

    utils.load_image("ab_logo.png", width = 350)
    st.write("""
    To [Aigües de Barcelona](https://www.aiguesdebarcelona.cat/ca/web/guest/) for providing their support and sharing their data with us.
    """)

    st.subheader("Feedback")
    st.write("""
        If you have any feedback, please reach out to us at yuma.ishigooka01@estudiant.upf.edu.
    """)

