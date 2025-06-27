import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RATING_DIV_ID = "mm-recipes-review-bar__rating_1-0"
RECIPE_DETAILS_CLASS = '.mm-recipes-details__item'
RECIPE_DETAILS_LABEL = '.mm-recipes-details__label'
RECIPE_DETAILS_VALUE = '.mm-recipes-details__value'
INGREDIENTS_LIST_CLASS = ".mm-recipes-structured-ingredients__list"
RECIPE_STEPS_ID = "mm-recipes-steps_1-0"
RECIPE_STEPS_TEXT = ".mntl-sc-block-html"

def find_recipe_data(url):
    if not url:
        return None

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove all script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # Remove the <head> section
    if soup.head:
        soup.head.decompose()

    # Parse rating
    rating_div = soup.find(id=RATING_DIV_ID)
    rating = rating_div.text if rating_div else None

    # Parse total time + servings
    total_time = None
    servings = None
    for item in soup.select(RECIPE_DETAILS_CLASS):
        label = item.select_one(RECIPE_DETAILS_LABEL)
        value = item.select_one(RECIPE_DETAILS_VALUE)
        if not label or not value:
            continue
        label_text = label.get_text(strip=True).lower()
        if label_text == "total time:":
            total_time = value.get_text(strip=True)
        elif label_text == "servings:":
            servings = value.get_text(strip=True)

    # Parse ingredients
    ingredients = []
    for list in soup.select(INGREDIENTS_LIST_CLASS):
        all_ingredients = list.find_all("li")
        for ingredient in all_ingredients:
            if ingredient:
                ingredients.append(ingredient.text.strip())

    # Parse directions
    directions = []
    steps = soup.find(id=RECIPE_STEPS_ID)
    if steps:
        step_text = steps.select(RECIPE_STEPS_TEXT)
        for step in step_text:
            if step:
                directions.append(step.text.strip())

    # return the recipe
    return {
        "total_time": total_time,
        "servings": servings,
        "rating": rating,
        "ingredients": ingredients,
        "directions": directions
    }