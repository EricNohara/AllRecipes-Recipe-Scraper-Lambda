import unittest
from unittest.mock import patch, Mock
from scrape_recipes import find_recipe_data

class TestFindRecipeData(unittest.TestCase):
    @patch("scrape_recipes.requests.get")
    def test_full_recipe(self, mock_get):
        html = """
        <html>
            <head></head>
            <body>
                <div id="mm-recipes-review-bar__rating_1-0">4.5 stars</div>
                <div class="mm-recipes-details__item">
                    <div class="mm-recipes-details__label">Total Time:</div>
                    <div class="mm-recipes-details__value">1 hr</div>
                </div>
                <div class="mm-recipes-details__item">
                    <div class="mm-recipes-details__label">Servings:</div>
                    <div class="mm-recipes-details__value">8</div>
                </div>
                <ul class="mm-recipes-structured-ingredients__list">
                    <li>1 cup flour</li>
                    <li>2 eggs</li>
                </ul>
                <div id="mm-recipes-steps_1-0">
                    <div class="mntl-sc-block-html">Mix ingredients.</div>
                    <div class="mntl-sc-block-html">Bake for 30 minutes.</div>
                </div>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response

        url = "http://fake-recipe-url.com"
        result = find_recipe_data(url)
        self.assertEqual(result["total_time"], "1 hr")
        self.assertEqual(result["servings"], "8")
        self.assertEqual(result["rating"], "4.5 stars")
        self.assertEqual(result["ingredients"], ["1 cup flour", "2 eggs"])
        self.assertEqual(result["directions"], ["Mix ingredients.", "Bake for 30 minutes."])

    @patch("scrape_recipes.requests.get")
    def test_missing_fields(self, mock_get):
        html = """
        <html>
            <body>
                <ul class="mm-recipes-structured-ingredients__list">
                    <li>1 cup flour</li>
                </ul>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response

        url = "http://fake-recipe-url.com"
        result = find_recipe_data(url)
        self.assertIsNone(result["total_time"])
        self.assertIsNone(result["servings"])
        self.assertIsNone(result["rating"])
        self.assertEqual(result["ingredients"], ["1 cup flour"])
        self.assertEqual(result["directions"], [])

    @patch("scrape_recipes.requests.get")
    def test_no_url(self, mock_get):
        result = find_recipe_data(None)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()