import json
from urllib.parse import urlencode

NEXT_LINK_BUTTON = ".pagination__item-link--next"

def parse_links(soup):
    links = set()

    script = soup.find("script", id="__NEXT_DATA__")
    if not script:
        return []
    
    data = json.loads(script.string)

    results = data.get("props", {}).get("pageProps", {}).get("results", [])
    for item in results:
        url = item.get("url")
        if url and url.startswith("/recipes/"):
            url_without_query = url.split("?")[0]
            links.add("https://cooking.nytimes.com" + url_without_query)
    return list(links)

def get_next_page_url(soup):
    script = soup.find("script", id="__NEXT_DATA__")
    if not script:
        return None
    data = json.loads(script.string)
    page_props = data.get("props", {}).get("pageProps", {})
    search_params = page_props.get("searchParams", {})
    current_page = search_params.get("page", 1)
    # Prefer originalQuery, fallback to query, fallback to empty string
    query = page_props.get("originalQuery") or page_props.get("query") or ""
    params = {'page': current_page + 1, 'q': query}
    return f"https://cooking.nytimes.com/search?{urlencode(params)}"
