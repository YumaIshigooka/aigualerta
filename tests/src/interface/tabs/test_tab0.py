from unittest import mock
import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../../../..'))
sys.path.insert(0, src_dir)

from src.interface.tabs.tab0 import load_page
import streamlit as st


class TestLoadPage(unittest.TestCase):

    def test_load_page(self):
        """Tests that the load_page function calls Streamlit elements with the correct types of arguments."""

        with mock.patch('streamlit.title') as mock_title, \
             mock.patch('streamlit.subheader') as mock_subheader, \
             mock.patch('streamlit.write') as mock_write, \
             mock.patch('interface.utils.load_image') as mock_load_image: 

            load_page()

            # Assert that st.title was called with a string argument
            mock_title.assert_called_once()
            self.assertIsInstance(mock_title.call_args[0][0], str) 

            # Assert that utils.load_image was called with the correct argument types
            mock_load_image.assert_any_call(mock.ANY, width=mock.ANY, center=mock.ANY)
            mock_load_image.assert_any_call(mock.ANY, width=mock.ANY)
            mock_load_image.assert_any_call(mock.ANY, width=mock.ANY)

            # Assert that st.subheader was called multiple times with string arguments
            self.assertEqual(mock_subheader.call_count, 4)
            for call in mock_subheader.call_args_list:
                self.assertIsInstance(call[0][0], str)

            # Assert that st.write was called multiple times with string arguments
            self.assertGreaterEqual(mock_write.call_count, 5)
            for call in mock_write.call_args_list:
                self.assertIsInstance(call[0][0], str)