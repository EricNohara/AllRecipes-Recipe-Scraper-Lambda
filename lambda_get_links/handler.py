import json
from scrape_links import find_recipe_links

def lambda_handler(event, context):
    dish = event.get("dish", "")
    max_pages = int(event.get("max_pages", 10))
    links = find_recipe_links(dish, max_pages)

    return {
        "statusCode": 200,
        "body": json.dumps(links)
    }