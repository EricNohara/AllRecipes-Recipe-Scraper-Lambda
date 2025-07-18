RECIPE_LINK = "a.comp.card"
NEXT_LINK_BUTTON = ".pagination__item-link--next"

def parse_links(soup):
    links = set()

    for a in soup.select(RECIPE_LINK):
        href = a.get('href', '')
        if 'recipe' not in href or 'recipes' in href:
            continue
        links.add(href)
    return list(links)

def get_next_page_url(soup):
    next_el = soup.select_one(NEXT_LINK_BUTTON)
    href = next_el.get("href") if next_el else None
    return href if href else None
