LINKS_MAP = {
    "all-recipes": "https://www.allrecipes.com/search?q={query}",
    "simply-recipes": "https://www.simplyrecipes.com/search?q={query}",
    "serious-eats": "https://www.seriouseats.com/search?q={query}",
    "nyt-cooking": "https://cooking.nytimes.com/search?q={query}",
}

QUERY_FORMAT = {
    "all-recipes": lambda q: q.replace(' ', '+'),
    "simply-recipes": lambda q: q.replace(' ', '+'), 
    "serious-eats": lambda q: q.replace(' ', '+'), 
    "nyt-cooking": lambda q: q.replace(' ', '+'), 
}

def get_search_url(sitename, query):
    template = LINKS_MAP.get(sitename)
    if not template:
        raise ValueError(f"Unknown site: {sitename}")
    formatter = QUERY_FORMAT.get(sitename, lambda q: q)
    formatted_query = formatter(query)
    return template.format(query=formatted_query)