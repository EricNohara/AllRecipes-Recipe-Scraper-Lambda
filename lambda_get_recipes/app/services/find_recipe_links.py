import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_recipe_links(dish_name, url=None, max_links=20, collected=None):
    # base cases
    if collected is None:
        collected = set()

    if len(collected) >= max_links:
        return list(collected)[:max_links]

    query = dish_name.replace(' ', '+')
    if not url:
        url = f"https://www.allrecipes.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    # get the important links
    for link in soup.select(".mntl-card-list-card--extendable"):
        collected.add(link.get("href"))

    next_el = soup.select_one(".mntl-pagination__next")

    if next_el:
        href = next_el.find_next("a").get("href")
        if (href):
            return find_recipe_links(dish_name, href, max_links, collected)
        
    return list(collected)[:max_links]