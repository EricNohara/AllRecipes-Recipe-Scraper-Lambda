RECIPE_CARD = ".o-RecipeResult"
LINK_H3 = ".m-MediaBlock__a-Headline"
NEXT_LINK_BUTTON = ".o-Pagination__a-NextButton"

def parse_links(soup):
    links = set()
    for card in soup.select(RECIPE_CARD):
        h3 = card.select_one(LINK_H3)
        if h3:
            a = h3.find("a", href=True)
            if a:
                links.add(f"https:{a["href"]}")
    return list(links)

def get_next_page_url(soup):
    next_el = soup.select_one(NEXT_LINK_BUTTON)
    href = next_el.get("href") if next_el else None
    if href:
        if href.startswith("http"):
            return href
        return f"https:{href}"
    return None
