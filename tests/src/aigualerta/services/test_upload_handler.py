import unittest
from unittest import mock
import pandas as pd

from aigualerta.services import upload_handler

class TestUploadHandler(unittest.TestCase):

    def setUp(self):
        # Mock Streamlit components
        self.mock_st_session_state = mock.patch('aigualerta.services.upload_handler.st.session_state').start()
        self.mock_st_file_uploader = mock.patch('aigualerta.services.upload_handler.st.file_uploader').start()
        self.mock_st_warning = mock.patch('aigualerta.services.upload_handler.st.warning').start()

        # Sample DataFrame for testing
        self.dummy_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

    def tearDown(self):
        self.mock_st_session_state.reset_mock()
        self.mock_st_file_uploader.reset_mock()
        self.mock_st_warning.reset_mock()

    def testIsUserDfLoadedReturnsTrueWhenDfLoaded(self):
        self.mock_st_session_state.user_df = self.dummy_df
        self.assertTrue(upload_handler.is_user_df_loaded())

    def testIsUserDfLoadedReturnsFalseWhenDfNotLoaded(self):
        self.mock_st_session_state.user_df = None
        self.assertFalse(upload_handler.is_user_df_loaded())

    def testIsPredictedDfLoadedReturnsTrueWhenDfLoaded(self):
        self.mock_st_session_state.predicted_df = self.dummy_df
        self.assertTrue(upload_handler.is_predicted_df_loaded())

    def testIsPredictedDfLoadedReturnsFalseWhenDfNotLoaded(self):
        self.mock_st_session_state.predicted_df = None
        self.assertFalse(upload_handler.is_predicted_df_loaded())

    @mock.patch('aigualerta.services.upload_handler.read_csv')
    def testUploadCsvReturnsDataFrameWhenFileUploaded(self, mock_read_csv):
        mock_read_csv.return_value = self.dummy_df
        self.mock_st_file_uploader.return_value = mock.MagicMock()
        df = upload_handler.upload_csv()
        self.assertIsNotNone(df)
        self.assertTrue(mock_read_csv.called)

    def testUploadCsvReturnsNoneWhenNoFileUploaded(self):
        self.mock_st_file_uploader.return_value = None
        df = upload_handler.upload_csv()
        self.assertIsNone(df)

    @mock.patch('aigualerta.services.upload_handler.read_parquet')
    def testUploadParquetReturnsDataFrameWhenFileUploaded(self, mock_read_parquet):
        mock_read_parquet.return_value = self.dummy_df
        self.mock_st_file_uploader.return_value = mock.MagicMock()
        df = upload_handler.upload_parquet()
        self.assertIsNotNone(df)
        self.assertTrue(mock_read_parquet.called)

    def testUploadParquetReturnsNoneWhenNoFileUploaded(self):
        self.mock_st_file_uploader.return_value = None
        df = upload_handler.upload_parquet()
        self.assertIsNone(df)

    @mock.patch('aigualerta.services.upload_handler.upload_csv')
    @mock.patch('aigualerta.services.upload_handler.upload_parquet')
    def testUploadDataReturnsDataFrameFromCsv(self, mock_upload_parquet, mock_upload_csv):
        mock_upload_csv.return_value = self.dummy_df
        mock_upload_parquet.return_value = None
        
        df = upload_handler.upload_data()

        self.assertTrue(df.equals(self.dummy_df))  
        mock_upload_csv.assert_called_once()
        mock_upload_parquet.assert_called_once()

    @mock.patch('aigualerta.services.upload_handler.upload_csv')
    @mock.patch('aigualerta.services.upload_handler.upload_parquet')
    def testUploadDataReturnsDataFrameFromParquet(self, mock_upload_parquet, mock_upload_csv):
        mock_upload_csv.return_value = None
        mock_upload_parquet.return_value = self.dummy_df

        df = upload_handler.upload_data()

        self.assertTrue(df.equals(self.dummy_df))
        mock_upload_csv.assert_called_once()
        mock_upload_parquet.assert_called_once()

    @mock.patch('aigualerta.services.upload_handler.upload_csv')
    @mock.patch('aigualerta.services.upload_handler.upload_parquet')
    def testUploadDataReturnsNone(self, mock_upload_parquet, mock_upload_csv):
        mock_upload_csv.return_value = None
        mock_upload_parquet.return_value = None

        df = upload_handler.upload_data()

        self.assertIsNone(df)
        mock_upload_csv.assert_called_once()
        mock_upload_parquet.assert_called_once()

    @mock.patch('aigualerta.services.upload_handler.upload_data')
    def testUploadManagerSetsUserDfWhenNewDfLoaded(self, mock_upload_data):
        mock_upload_data.return_value = self.dummy_df

        upload_handler.upload_manager()
        
        self.assertTrue(self.mock_st_session_state.user_df.equals(self.dummy_df))

    @mock.patch('aigualerta.services.upload_handler.upload_data')
    def testUploadManagerShowsWarningWhenNoNewDfLoaded(self, mock_upload_data):
        self.mock_st_session_state.user_df = self.dummy_df
        mock_upload_data.return_value = None

        upload_handler.upload_manager()
        
        self.assertTrue(self.mock_st_warning.called)