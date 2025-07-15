from bs4 import BeautifulSoup
from services.data_parsers.allrecipes import parse_recipe_data
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {"User-Agent": "Mozilla/5.0"}

async def fetch(session, link):
    async with session.get(link, ssl=False) as response:
        return await response.text()

async def find_recipe_data(session, link):
    if not link:
        return None

    html = await fetch(session, link)
    soup = BeautifulSoup(html, "html.parser")

    # return parsed recipe data
    return parse_recipe_data(soup)