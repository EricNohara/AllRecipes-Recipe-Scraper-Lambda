import json
import asyncio
import aiohttp
from scrape_recipes import find_recipe_data
from scrape_links import find_recipe_links

async def fetch_recipe(session, link):
    # call your async recipe data fetcher here
    return await find_recipe_data(session, link)

async def main(dish, max_pages):
    async with aiohttp.ClientSession() as session:
        links = find_recipe_links(dish, max_pages)
        tasks = [fetch_recipe(session, link) for link in links]
        recipes = await asyncio.gather(*tasks)
        return recipes

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        dish = params.get("dish", "")
        max_pages = int(params.get("max_pages", 10))

        recipes = asyncio.run(main(dish, max_pages))

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