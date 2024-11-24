from unittest import mock
import unittest

from aigualerta.tabs.tab1 import load_page

class TestLoadPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_show_results = mock.patch('aigualerta.tabs.tab1.show_results')
        cls.mock_df_uploaded = mock.patch('aigualerta.tabs.tab1.user_df_has_been_uploaded')
        cls.mock_button_pressed = mock.patch('aigualerta.tabs.tab1.is_process_data_button_pressed')
        cls.mock_show_results = cls.mock_show_results.start()
        cls.mock_df_uploaded = cls.mock_df_uploaded.start()
        cls.mock_button_pressed = cls.mock_button_pressed.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_show_results.stop()
        cls.mock_df_uploaded.stop()
        cls.mock_button_pressed.stop()

    def setUp(self):  # Add setUp method
        self.mock_show_results.reset_mock()
        self.mock_df_uploaded.reset_mock()
        self.mock_button_pressed.reset_mock()

    def testLoadPageBothFalse(self):
        """
        Tests with both user_df not uploaded and button not pressed
        """
        self.mock_df_uploaded.return_value = False
        self.mock_button_pressed.return_value = False
        load_page()
        self.mock_show_results.assert_not_called()

    def testLoadPageUserDfTrue(self):
        """
        Tests with user_df uploaded and button not pressed
        """
        self.mock_df_uploaded.return_value = True
        self.mock_button_pressed.return_value = False
        load_page()
        self.mock_show_results.assert_not_called()

    def testLoadPageButtonPressedTrue(self):
        """
        Tests with user_df not uploaded and button pressed
        """
        self.mock_df_uploaded.return_value = False
        self.mock_button_pressed.return_value = True
        load_page()
        self.mock_show_results.assert_not_called()

    def testLoadPageBothTrue(self):  # Renamed to avoid duplicate function name
        """
        Tests with both user_df uploaded and button pressed
        """
        self.mock_df_uploaded.return_value = True
        self.mock_button_pressed.return_value = True
        load_page()
        self.mock_show_results.assert_called_once()