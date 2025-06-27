import json
from scrape_links import find_recipe_links

def lambda_handler(event, context):
    # get HTTP params
    params = event.get("queryStringParameters") or {}
    dish = params.get("dish", "")
    max_pages = int(params.get("max_pages", 10))

    # get list of links
    links = find_recipe_links(dish, max_pages=max_pages)

    # response
    return {
        "statusCode": 200,
        "body": json.dumps(links)
    }