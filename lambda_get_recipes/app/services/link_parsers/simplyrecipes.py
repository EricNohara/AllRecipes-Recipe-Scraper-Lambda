RECIPE_CARD = ".comp.card-list__item.mntl-block"
NEXT_LINK_BUTTON = ".pagination__item-link--next"

def parse_links(soup):
    links = set()
    for card in soup.select(RECIPE_CARD):
        a = card.find("a", href=True)
        href = a["href"] if a else None
        if href and "/recipes/" in href:
            links.add(href)
    return list(links)

def get_next_page_url(soup):
    next_el = soup.select_one(NEXT_LINK_BUTTON)
    href = next_el.get("href") if next_el else None
    return href if href else None
