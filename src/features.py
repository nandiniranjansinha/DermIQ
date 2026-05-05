import pandas as pd


irritants = [
    'fragrance', 'parfum', 'alcohol denat', 'denatured alcohol',
    'limonene', 'linalool', 'citral', 'eugenol', 'geraniol',
    'cinnamal', 'benzyl alcohol', 'isopropyl alcohol',
    'menthol', 'sodium lauryl sulfate', 'citronellol'
]

comedogenic = [
    'coconut oil', 'cocoa butter', 'isopropyl myristate',
    'isopropyl palmitate', 'acetylated lanolin', 'wheat germ oil',
    'flaxseed oil', 'soybean oil', 'cottonseed oil'
]

harmful = [
    'parabens', 'methylparaben', 'propylparaben', 'butylparaben',
    'formaldehyde', 'dmdm hydantoin', 'quaternium-15',
    'triclosan', 'sodium lauryl sulfate', 'polyethylene',
    'butylated hydroxyanisole', 'bha', 'bht'
]

beneficial = [
    'niacinamide', 'retinol', 'retinyl palmitate', 'hyaluronic acid',
    'sodium hyaluronate', 'glycerin', 'ceramide np', 'ceramide ap',
    'ceramide eop', 'squalane', 'tocopherol', 'tocopheryl acetate',
    'ascorbic acid', 'vitamin c', 'panthenol', 'allantoin',
    'centella asiatica', 'salicylic acid', 'lactic acid',
    'glycolic acid', 'azelaic acid', 'caffeine', 'peptides',
    'collagen', 'aloe barbadensis leaf juice'
]


def analyze_ingredients(ingredient_list):
    """Categorize ingredients into irritants, comedogenic, harmful, beneficial."""
    return {
        'irritants':   [i for i in irritants   if i in ingredient_list],
        'comedogenic': [i for i in comedogenic if i in ingredient_list],
        'harmful':     [i for i in harmful     if i in ingredient_list],
        'beneficial':  [i for i in beneficial  if i in ingredient_list],
    }


def build_features(ingredient_list, analysis):
    """Build a feature DataFrame from ingredient list and analysis dict."""
    total = len(ingredient_list)
    ic = len(analysis['irritants'])
    cc = len(analysis['comedogenic'])
    hc = len(analysis['harmful'])
    bc = len(analysis['beneficial'])
    return pd.DataFrame([{
        'total_ingredients':  total,
        'irritants_count':    ic,
        'comedogenic_count':  cc,
        'harmful_count':      hc,
        'beneficial_count':   bc,
        'irritants_ratio':    ic / total if total else 0,
        'comedogenic_ratio':  cc / total if total else 0,
        'harmful_ratio':      hc / total if total else 0,
        'beneficial_ratio':   bc / total if total else 0,
        'has_fragrance':  1 if 'fragrance' in ingredient_list or 'parfum' in ingredient_list else 0,
        'has_alcohol':    1 if 'alcohol denat' in ingredient_list else 0,
        'has_harmful':    1 if hc > 0 else 0,
        'has_beneficial': 1 if bc > 0 else 0,
    }])


def safety_score(analysis, total):
    """Compute a 0-100 safety score from ingredient analysis."""
    if total == 0:
        return 50
    score = 100
    score -= len(analysis['irritants'])   * 10
    score -= len(analysis['harmful'])     * 15
    score -= len(analysis['comedogenic']) * 8
    score += len(analysis['beneficial'])  * 5
    return max(0, min(100, score))
