from bs4 import BeautifulSoup
from services.link_parsers.allrecipes import parse_links, get_next_page_url
from links_map import get_search_url
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_recipe_links(dish_name, url=None, max_links=20, collected=None, sitename="all-recipes"):
    # base cases
    if collected is None:
        collected = set()

    if len(collected) >= max_links:
        return list(collected)[:max_links]

    query = dish_name.replace(' ', '+')
    if not url:
        url = get_search_url(sitename, query)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    # get the important links
    links = parse_links(soup)
    collected.update(links)

    next_url = get_next_page_url(soup)
    if next_url:
        return find_recipe_links(dish_name, next_url, max_links, collected)
        
    return list(collected)[:max_links]