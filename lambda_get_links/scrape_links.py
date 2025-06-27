import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_recipe_links(dish_name, url=None, max_pages=3, page=1, collected=None):
    # base cases
    if collected is None:
        collected = []
    if page > max_pages:
        return collected

    query = dish_name.replace(' ', '+')
    if not url:
        url = f"https://www.allrecipes.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove all script and style elements
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()

    # get the important links
    next_link = None
    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text(strip=True)
        if href and "/recipe/" in href and text:
            collected.append(href)

        span = a.find("span")
        if span and span.get_text(strip=True).lower() == "next":
            next_link = a

    # recurse
    if next_link and next_link.get("href"):
        return find_recipe_links(dish_name, next_link.get("href"), max_pages, page + 1, collected)
    return collected