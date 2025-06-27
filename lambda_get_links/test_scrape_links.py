import unittest
from unittest.mock import patch, Mock
from scrape_links import find_recipe_links

class TestFindRecipeLinks(unittest.TestCase):
    @patch("scrape_links.requests.get")
    def test_single_page(self, mock_get):
        # Mock HTML with one recipe link and no "Next"
        html = """
        <html>
            <body>
                <a href="/recipe/12345/test-recipe">Test Recipe</a>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("pizza", max_pages=1)
        self.assertEqual(links, ["/recipe/12345/test-recipe"])

    @patch("scrape_links.requests.get")
    def test_pagination(self, mock_get):
        # First page with a recipe and a "Next" link
        html1 = """
        <html>
            <body>
                <a href="/recipe/12345/test-recipe">Test Recipe</a>
                <a href="http://nextpage.com"><span>Next</span></a>
            </body>
        </html>
        """
        # Second page with another recipe, no "Next"
        html2 = """
        <html>
            <body>
                <a href="/recipe/67890/another-recipe">Another Recipe</a>
            </body>
        </html>
        """
        mock_response1 = Mock()
        mock_response1.text = html1
        mock_response2 = Mock()
        mock_response2.text = html2
        mock_get.side_effect = [mock_response1, mock_response2]

        links = find_recipe_links("pizza", max_pages=2)
        self.assertEqual(links, ["/recipe/12345/test-recipe", "/recipe/67890/another-recipe"])

    @patch("scrape_links.requests.get")
    def test_non_recipe_links_ignored(self, mock_get):
        # Page with a mix of recipe and non-recipe links
        html = """
        <html>
            <body>
                <a href="/recipe/12345/test-recipe">Test Recipe</a>
                <a href="/about">About Us</a>
                <a href="https://external.com">External</a>
                <a href="/recipe/67890/another-recipe">Another Recipe</a>
                <a href="#">Empty Link</a>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("pizza", max_pages=1)
        self.assertEqual(links, ["/recipe/12345/test-recipe", "/recipe/67890/another-recipe"])

    @patch("scrape_links.requests.get")
    def test_no_recipe_links(self, mock_get):
        # Page with no recipe links
        html = """
        <html>
            <body>
                <a href="/about">About Us</a>
                <a href="https://external.com">External</a>
                <a href="#">Empty Link</a>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("pizza", max_pages=1)
        self.assertEqual(links, [])

if __name__ == "__main__":
    unittest.main()