RECIPE_NAME_CLASS = ".recipe-decision-block__title"
TOTAL_TIME_DIV = ".total-time.project-meta__total-time"
SERVINGS_DIV = ".recipe-serving.project-meta__recipe-serving"
TEXT_META = ".meta-text__data"
INGREDIENT_ITEM = ".structured-ingredients__list-item"
DIRECTIONS_SECTION = ".comp.section--instructions.section"
DIRECTIONS_TEXT = ".comp.mntl-sc-block.mntl-sc-block-html"

def parse_recipe_data(soup):
    if not soup:
        return {}

    # Parse name
    name_header = soup.select_one(RECIPE_NAME_CLASS)
    name = process_text(name_header.text) if name_header else None

    # Parse rating
    rating = None

    # Parse total time + servings
    total_time_div = soup.select_one(TOTAL_TIME_DIV)
    total_time_span = total_time_div.select_one(TEXT_META)
    total_time = process_text(total_time_span.text) if total_time_span else None

    servings_div = soup.select_one(SERVINGS_DIV)
    servings_span = servings_div.select_one(TEXT_META)
    servings = process_text(servings_span.text) if servings_span else None

    # Parse ingredients
    ingredients = []
    for item in soup.select(INGREDIENT_ITEM):
        if item:
            ingredients.append(process_text(item.text))

    # # Parse directions
    directions = []
    directions_section = soup.select_one(DIRECTIONS_SECTION)
    if directions_section:
        step_texts = directions_section.select(DIRECTIONS_TEXT)
        for step in step_texts:
            if step.text:
                directions.append(process_text(step.text))

    # return the recipe
    return {
        "name": name,
        "total_time": total_time,
        "servings": servings,
        "rating": rating,
        "ingredients": ingredients,
        "directions": directions
    }

def process_text(text):
    return text.replace('\n', ' ').strip() if text else None
