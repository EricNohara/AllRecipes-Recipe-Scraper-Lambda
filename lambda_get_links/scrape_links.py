import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_recipe_links(dish_name, url=None, max_pages=3, page=1, collected=None):
    # base cases
    if collected is None:
        collected = set()
    if page > max_pages:
        return collected

    query = dish_name.replace(' ', '+')
    if not url:
        url = f"https://www.allrecipes.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "lxml")

    # get the important links
    for link in soup.select(".mntl-card-list-card--extendable"):
        collected.add(link.get("href"))

    el = soup.select_one(".mntl-pagination__next")

    if (el):
        href = el.find_next("a").get("href")
        return find_recipe_links(dish_name, href, max_pages, page + 1, collected)
        
    return list(collected)