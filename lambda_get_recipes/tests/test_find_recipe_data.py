import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio

from app.services.find_recipe_data import find_recipe_data

class TestFindRecipeData(unittest.TestCase):

    def setUp(self):
        self.sample_html = """
        <html>
            <body>
                <div id="mm-recipes-review-bar__rating_1-0">4.5 stars</div>
                <div class="mm-recipes-details__item">
                    <div class="mm-recipes-details__label">Total Time:</div>
                    <div class="mm-recipes-details__value">1 hr 30 mins</div>
                </div>
                <div class="mm-recipes-details__item">
                    <div class="mm-recipes-details__label">Servings:</div>
                    <div class="mm-recipes-details__value">4 servings</div>
                </div>
                <ul class="mm-recipes-structured-ingredients__list">
                    <li>1 cup sugar</li>
                    <li>2 eggs</li>
                </ul>
                <div id="mm-recipes-steps_1-0">
                    <div class="mntl-sc-block-html">Step 1: Preheat the oven.</div>
                    <div class="mntl-sc-block-html">Step 2: Mix ingredients.</div>
                </div>
            </body>
        </html>
        """

    @patch("app.services.find_recipe_data.fetch", new_callable=AsyncMock)
    def test_full_recipe_parsing(self, mock_fetch):
        # Arrange
        mock_fetch.return_value = self.sample_html

        async def run_test():
            session = MagicMock()
            result = await find_recipe_data(session, "https://example.com/fake-recipe")

            # Assert
            self.assertEqual(result["rating"], "4.5 stars")
            self.assertEqual(result["total_time"], "1 hr 30 mins")
            self.assertEqual(result["servings"], "4 servings")
            self.assertEqual(result["ingredients"], ["1 cup sugar", "2 eggs"])
            self.assertEqual(result["directions"], ["Step 1: Preheat the oven.", "Step 2: Mix ingredients."])

        asyncio.run(run_test())

    @patch("app.services.find_recipe_data.fetch", new_callable=AsyncMock)
    def test_missing_elements(self, mock_fetch):
        minimal_html = "<html><body></body></html>"
        mock_fetch.return_value = minimal_html

        async def run_test():
            session = MagicMock()
            result = await find_recipe_data(session, "https://example.com/empty")

            self.assertIsNone(result["rating"])
            self.assertIsNone(result["total_time"])
            self.assertIsNone(result["servings"])
            self.assertEqual(result["ingredients"], [])
            self.assertEqual(result["directions"], [])

        asyncio.run(run_test())

    @patch("app.services.find_recipe_data.fetch", new_callable=AsyncMock)
    def test_no_link_returns_none(self, mock_fetch):
        async def run_test():
            session = MagicMock()
            result = await find_recipe_data(session, None)
            self.assertIsNone(result)

        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
