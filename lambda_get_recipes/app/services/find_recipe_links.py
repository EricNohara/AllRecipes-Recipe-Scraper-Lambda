from bs4 import BeautifulSoup
from services.link_parsers import allrecipes, simplyrecipes, seriouseats, nytcooking
from services.links_map import get_search_url
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PARSERS = {
    "all-recipes": {
        "parse_links": allrecipes.parse_links,
        "get_next_page_url": allrecipes.get_next_page_url
    },
    "simply-recipes": {
        "parse_links": simplyrecipes.parse_links,
        "get_next_page_url": simplyrecipes.get_next_page_url 
    },
    "serious-eats": {
        "parse_links": seriouseats.parse_links,
        "get_next_page_url": seriouseats.get_next_page_url 
    },
    "nyt-cooking": {
        "parse_links": nytcooking.parse_links,
        "get_next_page_url": nytcooking.get_next_page_url 
    }
}

def find_recipe_links(dish_name, url=None, max_links=20, collected=None, sitename="all-recipes"):
    if collected is None:
        collected = set()

    if len(collected) >= max_links:
        return list(collected)[:max_links]

    if not url:
        url = get_search_url(sitename, dish_name)
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")


    if not response.ok:
        return list(collected)[:max_links]

    # get the important links
    parser = PARSERS.get(sitename)
    if not parser:
        raise ValueError(f"No parser available for sitename: {sitename}")
    
    links = parser["parse_links"](soup)
    if not links:
        return list(collected)[:max_links]
    
    collected.update(links)

    next_url = parser["get_next_page_url"](soup)
    if next_url:
        return find_recipe_links(dish_name, next_url, max_links, collected, sitename)
            
    return list(collected)[:max_links]

# print(len(find_recipe_links(dish_name="pizza", max_links=200, sitename="nyt-cooking")))