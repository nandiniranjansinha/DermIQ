import re
import ast


def parse_ingredients(text):
    """Parse raw ingredient string into a cleaned list."""
    text = text.strip().strip("'\"[]")
    ingredients = re.split(r',\s*(?![^()]*\))', text)
    cleaned = []
    for i in ingredients:
        i = i.strip()
        i = i.strip("'\"")
        i = i.rstrip('.')
        i = i.replace('*', '')
        i = i.lower()
        i = i.strip()
        if i:
            cleaned.append(i)
    return cleaned


def parse_highlights(text):
    """Parse highlights string into a list."""
    try:
        return ast.literal_eval(text)
    except:
        return []


def normalize_ingredient_names(ingredient_list):
    """Normalize common ingredient name variations."""
    name_map = {
        'vitamin e acetate':  'tocopheryl acetate',
        'vitamine acetate':   'tocopheryl acetate',
        'vitamin e':          'tocopherol',
        'aloe vera':          'aloe barbadensis leaf juice',
        'aloe barbadensis':   'aloe barbadensis leaf juice',
        'vitamin c':          'ascorbic acid',
        'pentasiloxane':      'cyclopentasiloxane',
        'hyaluronic acid':    'hyaluronic acid',
        'retinol':            'retinol',
    }
    return [name_map.get(i, i) for i in ingredient_list]
