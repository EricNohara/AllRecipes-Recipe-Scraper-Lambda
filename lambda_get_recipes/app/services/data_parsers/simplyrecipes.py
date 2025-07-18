ARTICLE_HEADER = ".loc.article-header"
ARTICLE_TITLE = ".heading__title"
RATING_DIV = ".aggregate-star-rating__stars"
RECIPE_TOTAL_TIME_DIV = ".total-time.project-meta__total-time"
RECIPE_DATA = ".meta-text__data"
RECIPE_SERVINGS_DIV = ".recipe-serving.project-meta__recipe-serving"
INGREDIENT_LIST_ITEM = ".structured-ingredients__list-item"
INSTRUCTIONS_DIV = ".comp.section--instructions.section"
INSTRUCTION_ITEM = ".comp.mntl-sc-block.mntl-sc-block-startgroup.mntl-sc-block-group--LI"

def parse_recipe_data(soup):
    if not soup:
        return {}
    
    header = soup.select_one(ARTICLE_HEADER)

    # Parse name
    name_header = header.select_one(ARTICLE_TITLE)
    name = process_text(name_header.text)

    # Parse rating
    rating = parse_rating(soup)

    # Parse total time + servings
    total_time_container = soup.select_one(RECIPE_TOTAL_TIME_DIV)
    total_time = None
    if total_time_container:
        total_time_elem = total_time_container.select_one(RECIPE_DATA)
        total_time = process_text(total_time_elem.get_text(strip=True) if total_time_elem else None)

    servings_container = soup.select_one(RECIPE_SERVINGS_DIV)
    servings = None
    if servings_container:
        servings_elem = servings_container.select_one(RECIPE_DATA)
        servings = process_text(servings_elem.get_text(strip=True) if servings_elem else None)

    # Parse ingredients
    ingredients = []

    for item in soup.select(INGREDIENT_LIST_ITEM):
        p = item.find("p")
        if p:
            ingredient = process_text(p.get_text(" ", strip=True))
            ingredients.append(ingredient)

    # Parse directions
    directions = []
    instructions_section = soup.select_one(INSTRUCTIONS_DIV)
    if instructions_section:
        for item in instructions_section.select(INSTRUCTION_ITEM):
            for p in item.find_all("p"):
                step = process_text(p.get_text(" ", strip=True))
                if step:
                    directions.append(step)


    # return the recipe
    return {
        "name": name,
        "total_time": total_time,
        "servings": servings,
        "rating": rating,
        "ingredients": ingredients,
        "directions": directions
    }

def parse_rating(soup):
    rating_div = soup.select_one(RATING_DIV)
    if not rating_div:
        return None
    stars = rating_div.find_all("a")
    rating = 0
    for star in stars:
        if "active" in star.get("class", []):
            rating += 1
        elif "half" in star.get("class", []):
            rating += 0.5
    return rating

def process_text(text):
    return text.replace('\n', ' ').strip() if text else None