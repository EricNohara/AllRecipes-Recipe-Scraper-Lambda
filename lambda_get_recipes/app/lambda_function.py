import json
import asyncio
import aiohttp
from app.services.find_recipe_data import find_recipe_data
from app.services.find_recipe_links import find_recipe_links

async def fetch_recipe(session, link):
    return await find_recipe_data(session, link)

async def main(dish, max_links):
    async with aiohttp.ClientSession() as session:
        links = find_recipe_links(dish_name=dish, max_links=max_links)
        tasks = [fetch_recipe(session, link) for link in links]
        recipes = await asyncio.gather(*tasks)
        return recipes

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        dish = params.get("dish", "")
        max_links = int(params.get("max_links", 20))

        recipes = asyncio.run(main(dish, max_links))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(recipes)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }