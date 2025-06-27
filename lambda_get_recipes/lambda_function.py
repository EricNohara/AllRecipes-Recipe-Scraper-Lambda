import json
import requests
from scrape_recipes import find_recipe_data

GET_LINKS_URL = "https://ii6hupokihiu6p37z4ogqw2qha0rspel.lambda-url.us-east-2.on.aws/"

def get_recipe_links_from_http(dish, max_pages):
    params = {"dish": dish, "max_pages": max_pages}
    response = requests.get(GET_LINKS_URL, params=params)
    response.raise_for_status()
    return json.loads(response.json()["body"])

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        dish = params.get("dish", "")
        max_pages = int(params.get("max_pages", 10))

        # get the links from the other function
        links = get_recipe_links_from_http(dish, max_pages)

        recipes = [find_recipe_data(link) for link in links]

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps(recipes)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": str(e)})
        }