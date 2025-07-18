from bs4 import BeautifulSoup
from services.data_parsers import allrecipes, simplyrecipes, seriouseats
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PARSERS = {
    "all-recipes": allrecipes.parse_recipe_data,
    "simply-recipes": simplyrecipes.parse_recipe_data,
    "serious-eats": seriouseats.parse_recipe_data,
}

headers = {"User-Agent": "Mozilla/5.0"}

async def fetch(session, link):
    async with session.get(link, ssl=False) as response:
        return await response.text()

async def find_recipe_data(session, link, sitename="all-recipes"):
    if not link:
        return None

    html = await fetch(session, link)
    soup = BeautifulSoup(html, "html.parser")

    # return parsed recipe data
    parser = PARSERS.get(sitename)
    return parser(soup)