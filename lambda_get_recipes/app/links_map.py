LINKS_MAP = {
    "all-recipes": "https://www.allrecipes.com/search?q={query}",
    "food-network": "https://www.foodnetwork.com/search/{query}-",
    # "serious-eats": "https://www.seriouseats.com/search?q={query}"
}

def get_search_url(sitename, query):
    template = LINKS_MAP.get(sitename)
    if not template:
        raise ValueError(f"Unknown site: {sitename}")
    return template.format(query=query)