import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing import parse_ingredients, normalize_ingredient_names


def test_parse_ingredients_basic():
    text = "Water, Glycerin, Niacinamide, Fragrance"
    result = parse_ingredients(text)
    assert result == ['water', 'glycerin', 'niacinamide', 'fragrance']


def test_parse_ingredients_handles_parentheses():
    text = "Water (Aqua, Eau), Glycerin"
    result = parse_ingredients(text)
    assert 'water (aqua, eau)' in result
    assert 'glycerin' in result


def test_parse_ingredients_removes_asterisk():
    text = "Collagen (Vegan)*, Glycerin"
    result = parse_ingredients(text)
    assert 'collagen (vegan)' in result


def test_parse_ingredients_lowercase():
    text = "WATER, GLYCERIN"
    result = parse_ingredients(text)
    assert result == ['water', 'glycerin']


def test_normalize_ingredient_names():
    ingredients = ['vitamin e', 'aloe vera', 'vitamin c']
    result = normalize_ingredient_names(ingredients)
    assert 'tocopherol' in result
    assert 'aloe barbadensis leaf juice' in result
    assert 'ascorbic acid' in result


if __name__ == "__main__":
    test_parse_ingredients_basic()
    test_parse_ingredients_handles_parentheses()
    test_parse_ingredients_removes_asterisk()
    test_parse_ingredients_lowercase()
    test_normalize_ingredient_names()
    print("All tests passed!")
