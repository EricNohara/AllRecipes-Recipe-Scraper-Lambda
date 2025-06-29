import unittest
from unittest.mock import patch, MagicMock
from app.services.find_recipe_links import find_recipe_links

class TestFindRecipeLinks(unittest.TestCase):

    @patch('app.services.find_recipe_links.requests.get')
    def test_collects_correct_number_of_links(self, mock_get):
        html = """
        <html>
        <body>
            <a class="mntl-card-list-card--extendable" href="https://example.com/recipe1"></a>
            <a class="mntl-card-list-card--extendable" href="https://example.com/recipe2"></a>
            <a class="mntl-card-list-card--extendable" href="https://example.com/recipe3"></a>
        </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("pasta", max_links=2)
        self.assertEqual(len(links), 2)
        self.assertTrue(all(link.startswith("https://example.com/recipe") for link in links))

    @patch('app.services.find_recipe_links.requests.get')
    def test_returns_empty_if_no_links(self, mock_get):
        html = "<html><body>No results</body></html>"
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("nonexistentdish", max_links=5)
        self.assertEqual(links, [])

    @patch('app.services.find_recipe_links.requests.get')
    def test_stops_recursing_when_max_links_reached(self, mock_get):
        def generate_html_with_links(n):
            return "<html><body>" + "".join(
                f'<a class="mntl-card-list-card--extendable" href="https://example.com/recipe{i}"></a>'
                for i in range(n)
            ) + '</body></html>'

        # Simulate a page with 10 links and a "next" page
        html = generate_html_with_links(10) + """
        <a class="mntl-pagination__next" href="/page2"><a href="https://example.com/page2"></a></a>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("chicken", max_links=5)
        self.assertEqual(len(links), 5)

    @patch('app.services.find_recipe_links.requests.get')
    def test_duplicates_are_ignored(self, mock_get):
        html = """
        <html>
        <body>
            <a class="mntl-card-list-card--extendable" href="https://example.com/recipe1"></a>
            <a class="mntl-card-list-card--extendable" href="https://example.com/recipe1"></a>
            <a class="mntl-card-list-card--extendable" href="https://example.com/recipe2"></a>
        </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.text = html
        mock_get.return_value = mock_response

        links = find_recipe_links("bread", max_links=5)
        self.assertEqual(len(links), 2)
        self.assertIn("https://example.com/recipe1", links)
        self.assertIn("https://example.com/recipe2", links)

if __name__ == '__main__':
    unittest.main()
