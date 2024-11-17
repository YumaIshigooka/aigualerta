import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, src_dir)

import streamlit as st
from interface import utils

def load_page():
    
    utils.dump_plot_example()