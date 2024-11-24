import unittest
from unittest import mock
import os

from aigualerta.services import resource_handler

class TestResourceHandler(unittest.TestCase):

    @mock.patch('aigualerta.services.resource_handler.open', new_callable=mock.mock_open, read_data="test file content")
    @mock.patch('aigualerta.services.resource_handler.get_absolute_path')
    def testLoadFileReturnsFileContent(self, mock_get_absolute_path, mock_open):
        mock_get_absolute_path.return_value = "/path/to/file.txt"
        file_content = resource_handler.load_file("file.txt")
        self.assertEqual(file_content, "test file content")
        mock_open.assert_called_once_with("/path/to/file.txt", "r")

    @mock.patch('aigualerta.services.resource_handler.os.path.dirname')
    @mock.patch('aigualerta.services.resource_handler.os.path.join')
    def testGetAbsolutePathReturnsCorrectPath(self, mock_join, mock_dirname):
        mock_dirname.return_value = "/base/path"
        mock_join.return_value = "/base/path/test/file.txt"
        absolute_path = resource_handler.get_absolute_path("test/file.txt")
        self.assertEqual(absolute_path, "/base/path/test/file.txt")

    @mock.patch('aigualerta.services.resource_handler.open', new_callable=mock.mock_open, read_data=b"test image data")
    @mock.patch('aigualerta.services.resource_handler.get_absolute_path')
    @mock.patch('aigualerta.services.resource_handler.base64.b64encode')
    def testLoadImageAsBase64ReturnsEncodedString(self, mock_b64encode, mock_get_absolute_path, mock_open):
        mock_get_absolute_path.return_value = "/path/to/image.png"
        mock_b64encode.return_value = b"encoded_image_data"
        encoded_string = resource_handler.load_image_as_base64("image.png")
        self.assertEqual(encoded_string, "data:image/png;base64,encoded_image_data")
        mock_open.assert_called_once_with("/path/to/image.png", "rb")
        mock_b64encode.assert_called_once_with(b"test image data")

    @mock.patch('aigualerta.services.resource_handler.st.session_state')
    def testGetThemeReturnsLightForLightTheme(self, mock_session_state):
        mock_session_state.theme = {'base': 'light'}
        theme = resource_handler.get_theme()
        self.assertEqual(theme, 'light')

    @mock.patch('aigualerta.services.resource_handler.st.session_state')
    def testGetThemeReturnsDarkForDarkTheme(self, mock_session_state):
        mock_session_state.theme = {'base': 'dark'}
        theme = resource_handler.get_theme()
        self.assertEqual(theme, 'dark')

    @mock.patch('aigualerta.services.resource_handler.st.session_state')
    def testThemeReturnsThemeFromSessionState(self, mock_session_state):
        mock_session_state.theme = {'base': 'dark', 'primaryColor': 'blue'}
        theme = resource_handler.theme()
        self.assertEqual(theme, {'base': 'dark', 'primaryColor': 'blue'})