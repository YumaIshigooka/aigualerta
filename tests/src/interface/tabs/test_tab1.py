from unittest import mock
import unittest

from aigualerta.tabs.tab1 import load_page
import streamlit as st

class TestLoadPage(unittest.TestCase):
    def testLoadPage(self):
        print('a')