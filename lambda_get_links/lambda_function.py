import json
from scrape_links import find_recipe_links

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        dish = params.get("dish", "")
        max_pages = int(params.get("max_pages", 10))

        links = find_recipe_links(dish, max_pages=max_pages)

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps(links)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": str(e)})
        }
