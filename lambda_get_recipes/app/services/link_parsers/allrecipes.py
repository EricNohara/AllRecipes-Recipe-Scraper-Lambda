LINK_CARD = ".mntl-card-list-card--extendable"
NEXT_LINK_CARD = ".mntl-pagination__next"

def parse_links(soup):
    links = set()
    for link in soup.select(LINK_CARD):
        href = link.get("href")
        if href:
            links.add(href)
    return list(links)

def get_next_page_url(soup):
    next_el = soup.select_one(NEXT_LINK_CARD)
    if next_el:
        a_tag = next_el.find_next("a")
        if a_tag and a_tag.get("href"):
            return a_tag.get("href")
    return None