import unittest
from unittest import mock
import pandas as pd

from aigualerta.services import display_handler

class TestDisplayHandler(unittest.TestCase):

    def setUp(self):
        # Set up some dummy data for testing
        self.dummy_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        self.mock_st_session_state = mock.patch('aigualerta.services.display_handler.st.session_state').start()
        self.mock_st_session_state.user_df = self.dummy_df
        self.mock_st_session_state.predicted_df = self.dummy_df.copy()
        self.mock_st_session_state.predicted_df['LEAK'] = [True, False, True]

        # Initialize mocks
        self.mock_st_write    = mock.patch('aigualerta.services.display_handler.st.write').start()
        self.mock_st_tabs     = mock.patch('aigualerta.services.display_handler.st.tabs').start()
        self.mock_st_button   = mock.patch('aigualerta.services.display_handler.st.button').start()
        self.mock_st_progress = mock.patch('aigualerta.services.display_handler.st.progress').start()

    def tearDown(self):
        # Reset mocks after each test
        self.mock_st_write.reset_mock()
        self.mock_st_tabs.reset_mock()
        self.mock_st_button.reset_mock()
        self.mock_st_progress.reset_mock()

    def testShowDfWritesDfWithMessage(self):
        message = "Test message"
        display_handler.show_df(self.dummy_df, message)
        self.mock_st_write.assert_has_calls([
            mock.call(message),
            mock.call(self.dummy_df)
        ])

    def testShowDfWritesDfWithoutMessage(self):
        display_handler.show_df(self.dummy_df)
        self.mock_st_write.assert_called_once_with(self.dummy_df)

    def testDisplayInputDataWritesUserDf(self):
        display_handler.display_input_data()
        self.mock_st_write.assert_called_once_with(self.mock_st_session_state.user_df)

    def testDisplayPredictedResultsWritesPredictedDf(self):
        display_handler.display_predicted_results()
        self.mock_st_write.assert_called_once_with(self.mock_st_session_state.predicted_df)

    def testDisplayLeakRowsWritesFilteredDf(self):
        display_handler.display_leak_rows()
        self.mock_st_write.assert_called_once()

    @mock.patch('aigualerta.services.display_handler.display_input_data')
    @mock.patch('aigualerta.services.display_handler.display_predicted_results')
    @mock.patch('aigualerta.services.display_handler.display_leak_rows')
    @mock.patch('aigualerta.services.display_handler.plot_durations')
    def testSubtabHandlerCallsDisplayFunctions(self, mock_plot, mock_leaks, mock_predict, mock_input):
        # Configure mock_st_tabs to return a 4-tuple
        self.mock_st_tabs.return_value = (mock.MagicMock(), mock.MagicMock(), mock.MagicMock(), mock.MagicMock())  
        
        display_handler.subtab_handler()
        mock_input.assert_called_once()
        mock_predict.assert_called_once()
        mock_leaks.assert_called_once()
        mock_plot.assert_called_once_with(self.mock_st_session_state.predicted_df)

    @mock.patch('aigualerta.services.display_handler.is_user_df_loaded')
    def testIsProcessDataButtonPressedReturnsButtonWhenDfLoaded(self, df_loaded_mock):
        df_loaded_mock.return_value = True
        display_handler.is_process_data_button_pressed()
        self.mock_st_button.assert_called_once_with('Process data')

    @mock.patch('aigualerta.services.display_handler.is_user_df_loaded')
    def testIsProcessDataButtonPressedReturnsNoneWhenDfNotLoaded(self, df_loaded_mock):
        df_loaded_mock.return_value = False
        result = display_handler.is_process_data_button_pressed()
        self.mock_st_button.assert_not_called()
        self.assertIsNone(result)

    @mock.patch('aigualerta.services.display_handler.is_user_df_loaded')
    @mock.patch('aigualerta.services.display_handler.upload_manager')
    def testUserDfHasBeenUploadedCallsUploadManagerAndReturnsIsUserDfLoaded(self, upload_manager_mock, df_loaded_mock):
        df_loaded_mock.return_value = True
        result = display_handler.user_df_has_been_uploaded()
        upload_manager_mock.assert_called_once()
        df_loaded_mock.assert_called_once()
        self.assertTrue(result)

    @mock.patch('aigualerta.services.display_handler.compute_results')
    @mock.patch('aigualerta.services.display_handler.subtab_handler')
    def testShowResultsCallsComputeResultsAndSubtabHandler(self, subtab_handler_mock, compute_results_mock):
        display_handler.show_results()
        self.mock_st_progress.assert_called_once_with(1, text="Preparing")
        compute_results_mock.assert_called_once_with(self.mock_st_session_state.user_df, mock.ANY)
        subtab_handler_mock.assert_called_once()
