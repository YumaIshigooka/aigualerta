from unittest import mock
import unittest

from aigualerta.tabs.tab1 import load_page
import streamlit as st

class TestLoadPage(unittest.TestCase):

    def test_load_page_no_data(self):
        """Tests the load_page function when no data is uploaded."""

        with mock.patch('streamlit.write') as mock_write, \
             mock.patch('streamlit.session_state') as mock_session_state:  # Mock session_state itself

            mock_session_state.user_df = None  # Set user_df within the mocked session_state
            load_page()
            mock_write.assert_called_with("If you are willing to **load your dataset from the data folder**, please refer to the *data from folder* tab.")


    # def test_load_page_with_data(self):
    #     """Tests the load_page function when data is uploaded."""

    #     with mock.patch('streamlit.subheader') as mock_subheader, \
    #          mock.patch('streamlit.write') as mock_write, \
    #          mock.patch('streamlit.session_state') as mock_session_state, \
    #          mock.patch('interface.utils.upload_data') as mock_upload_data, \
    #          mock.patch('interface.utils.setup_data') as mock_setup_data, \
    #          mock.patch('interface.utils.setup_input') as mock_setup_input, \
    #          mock.patch('interface.utils.predict') as mock_predict, \
    #          mock.patch('streamlit.button') as mock_button:

    #         load_page()

    #         # Assert that st.subheader was called with string arguments
    #         subheader_calls = [
    #             mock.call("Uploaded Dataset"),
    #             mock.call("Processed Dataset"),
    #             mock.call("Input that will be used"),
    #         ]
    #         mock_subheader.assert_has_calls(subheader_calls, any_order=True)

    #         # ... (rest of the assertions) ...

    #         # Assert that utils functions were called with the correct arguments
    #         mock_setup_data.assert_called_once_with("mock_uploaded_data")
    #         mock_setup_input.assert_called_once_with("mock_processed_data")
    #         mock_predict.assert_called_once_with("mock_input_data")