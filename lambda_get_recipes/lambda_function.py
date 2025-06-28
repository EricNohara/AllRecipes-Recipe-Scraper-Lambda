import json
import asyncio
import aiohttp
from scrape_recipes import find_recipe_data

GET_LINKS_URL = "https://ii6hupokihiu6p37z4ogqw2qha0rspel.lambda-url.us-east-2.on.aws/"

async def get_recipe_links_from_http_async(session, dish, max_pages):
    params = {"dish": dish, "max_pages": max_pages}
    async with session.get(GET_LINKS_URL, params=params) as response:
        response.raise_for_status()
        return await response.json()

async def fetch_recipe(session, link):
    # call your async recipe data fetcher here
    return await find_recipe_data(session, link)

async def main(dish, max_pages):
    async with aiohttp.ClientSession() as session:
        links = await get_recipe_links_from_http_async(session, dish, max_pages)
        tasks = [fetch_recipe(session, link) for link in links]
        recipes = await asyncio.gather(*tasks)
        return recipes

def lambda_handler(event, context):
    try:
        if isinstance(event, str):
            event = json.loads(event)

        raw_params = event.get("queryStringParameters") or {}
        if isinstance(raw_params, str):
            params = json.loads(raw_params)
        else:
            params = raw_params

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