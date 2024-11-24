from unittest import mock
import unittest
from aigualerta.tabs import tab0

class TestLoadPage(unittest.TestCase):

    @mock.patch('aigualerta.tabs.tab0.get_theme')
    @mock.patch('aigualerta.tabs.tab0.load_image_as_base64')
    def test_setup_welcome_page(self, mock_load_image, mock_theme):
        """Test that setup_welcome_page correctly processes the markdown file."""

        mock_theme.return_value = 'dark'
        mock_load_image.side_effect = [
            "mock_aigualerta_logo",
            "mock_upf_logo",
            "mock_ab_logo"
        ]
        md = "{aigualerta_logo} some text {upf_logo} more text {ab_logo}"
        result = tab0.setup_welcome_page(md)
        print(result)
        assert result == "mock_aigualerta_logo some text mock_upf_logo more text mock_ab_logo"

    @mock.patch('aigualerta.tabs.tab0.setup_welcome_page')
    @mock.patch('aigualerta.tabs.tab0.load_file')
    @mock.patch('streamlit.markdown') 
    def test_load_page(self, mock_markdown, mock_load_file, mock_setup_welcome_page):
        """Test that load_page correctly loads and displays the welcome page."""

        # Mock load_file to return some test markdown content
        mock_load_file.return_value = "Test markdown content {aigualerta_logo}"

        # Mock setup_welcome_page to return processed markdown
        mock_setup_welcome_page.return_value = "Processed markdown with logo"

        tab0.load_page()

        # Assert that the functions were called with the expected arguments
        mock_load_file.assert_called_once_with('resources/welcome_page.md')
        mock_setup_welcome_page.assert_called_once_with("Test markdown content {aigualerta_logo}")
        mock_markdown.assert_called_once_with("Processed markdown with logo", unsafe_allow_html=True)
