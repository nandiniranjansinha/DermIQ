import streamlit as st
import pandas as pd
import pickle
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re

# ── Config ─────────────────────────────────────────────────────────────────
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(
    page_title="DermIQ",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Knowledge Base ─────────────────────────────────────────────────────────
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

ingredient_info = {
    'niacinamide':              'Brightening, pore-minimizing, barrier repair',
    'retinol':                  'Anti-aging, cell turnover, wrinkle reduction',
    'hyaluronic acid':          'Deep hydration, plumping',
    'sodium hyaluronate':       'Deep hydration, moisture retention',
    'glycerin':                 'Humectant, draws moisture to skin',
    'ceramide np':              'Barrier repair, moisture lock',
    'ceramide ap':              'Barrier repair, moisture lock',
    'ceramide eop':             'Barrier repair, moisture lock',
    'squalane':                 'Lightweight moisturizing, non-comedogenic',
    'tocopherol':               'Vitamin E, antioxidant protection',
    'tocopheryl acetate':       'Vitamin E, antioxidant protection',
    'ascorbic acid':            'Vitamin C, brightening, antioxidant',
    'vitamin c':                'Brightening, antioxidant',
    'panthenol':                'Vitamin B5, soothing, hydrating',
    'allantoin':                'Soothing, healing, anti-irritant',
    'centella asiatica':        'Calming, healing, anti-inflammatory',
    'salicylic acid':           'BHA, exfoliant, acne-fighting',
    'lactic acid':              'AHA, gentle exfoliant, brightening',
    'glycolic acid':            'AHA, exfoliant, anti-aging',
    'azelaic acid':             'Acne, rosacea, brightening',
    'caffeine':                 'Depuffs, antioxidant',
    'collagen':                 'Firming, anti-aging',
    'aloe barbadensis leaf juice': 'Soothing, hydrating, calming',
    'retinyl palmitate':        'Gentle retinol, anti-aging',
    'peptides':                 'Firming, anti-aging, collagen stimulation',
}

# ── Load Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    with open("models/skincare_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ── Helper Functions ───────────────────────────────────────────────────────
def preprocess_image(image):
    image = image.convert('L')
    image = image.filter(ImageFilter.SHARPEN)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    enhancer2 = ImageEnhance.Brightness(image)
    image = enhancer2.enhance(1.2)
    image = image.resize(
        (image.width * 2, image.height * 2),
        Image.Resampling.LANCZOS
    )
    return image

def extract_text_from_image(image):
    processed = preprocess_image(image)
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed, config=config)
    return text

def parse_ingredients(text):
    # Cut at storage/warning sections line by line
    lines = text.split('\n')
    ingredient_lines = []
    for line in lines:
        low = line.lower()
        if any(w in low for w in ['storage', 'directions', 'warning',
                                   'caution', 'manufactured', 'keep out',
                                   'avoid', 'store below']):
            break
        ingredient_lines.append(line)
    text = ' '.join(ingredient_lines)

    # Cut at last period
    last_period = text.rfind('.')
    if last_period != -1:
        text = text[:last_period]

    # Remove INGREDIENTS: header
    text = re.sub(r'(?i)ingredients\s*:', '', text)
    text = text.strip().strip("'\"[]")

    ingredients = re.split(r',\s*(?![^()]*\))', text)
    cleaned = []
    for i in ingredients:
        i = i.strip().strip("'\"").rstrip('.').replace('*', '').lower().strip()
        i = re.sub(r'\n', ' ', i)
        i = re.sub(r'\s+', ' ', i).strip()
        if i and len(i) > 2 and not i.isdigit():
            cleaned.append(i)
    return cleaned

def normalize_ingredient_names(ingredient_list):
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

def analyze(ingredient_list):
    return {
        'irritants':   [i for i in irritants   if i in ingredient_list],
        'comedogenic': [i for i in comedogenic if i in ingredient_list],
        'harmful':     [i for i in harmful     if i in ingredient_list],
        'beneficial':  [i for i in beneficial  if i in ingredient_list],
    }

def build_features(ingredient_list, analysis):
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
    if total == 0:
        return 50
    score = 100
    score -= len(analysis['irritants'])   * 10
    score -= len(analysis['harmful'])     * 15
    score -= len(analysis['comedogenic']) * 8
    score += len(analysis['beneficial'])  * 5
    return max(0, min(100, score))

def quiz_compatibility_score(quiz, predictions):
    score    = 100
    warnings = []
    tips     = []

    skin_type   = quiz['skin_type']
    concerns    = quiz['concerns']
    allergies   = quiz['allergies']
    sensitivity = quiz['sensitivity']
    age         = quiz['age']

    dry_pred  = predictions[0]
    oily_pred = predictions[1]
    acne_pred = predictions[2]
    ff_pred   = predictions[3]

    if skin_type == 'Oily' and dry_pred == 1 and oily_pred == 0:
        score -= 20
        warnings.append("⚠️ Formulated for dry skin — may feel heavy on oily skin")
    if skin_type == 'Dry' and oily_pred == 1 and dry_pred == 0:
        score -= 20
        warnings.append("⚠️ Formulated for oily skin — may not moisturize enough")
    if skin_type in ['Oily', 'Combination'] and acne_pred == 1:
        score += 10
        tips.append("✅ Good match — product is flagged as acne-friendly")
    if 'Acne' in concerns and acne_pred == 0:
        score -= 15
        warnings.append("⚠️ Not specifically flagged for acne — look for salicylic acid or niacinamide")
    if 'Acne' in concerns and acne_pred == 1:
        score += 15
        tips.append("✅ Great for acne concerns")
    if 'Pigmentation' in concerns or 'Hyperpigmentation' in concerns:
        tips.append("💡 Look for niacinamide, vitamin C, azelaic acid and kojic acid")
    if 'Dullness' in concerns:
        tips.append("💡 AHAs (lactic/glycolic acid) and vitamin C help with dullness")
    if 'Dehydration' in concerns:
        tips.append("💡 Hyaluronic acid and glycerin are key for dehydrated skin")
    if 'Dark Circles' in concerns:
        tips.append("💡 Caffeine and vitamin K help reduce dark circles")
    if 'Firmness / Elasticity' in concerns:
        tips.append("💡 Peptides, retinol and collagen support skin firmness")
    if 'Uneven Texture' in concerns:
        tips.append("💡 Chemical exfoliants like AHAs/BHAs smooth uneven texture")
    if 'Oiliness' in concerns and oily_pred == 0:
        warnings.append("⚠️ Product may not be ideal for oily/combination skin")
    if 'Fragrance' in allergies and ff_pred == 0:
        score -= 25
        warnings.append("🚨 You have a fragrance allergy — this product may contain fragrance")
    if 'Fragrance' in allergies and ff_pred == 1:
        score += 15
        tips.append("✅ Fragrance-free — safe for your fragrance allergy")
    if sensitivity == 'High' and ff_pred == 0:
        score -= 10
        warnings.append("⚠️ High sensitivity — fragrance may cause reactions")
    if sensitivity == 'High':
        tips.append("💡 Always patch test first given your high sensitivity")
    if age in ['40s', '50+'] and 'Anti-aging' in concerns:
        tips.append("💡 Look for retinol, peptides, and vitamin C for anti-aging")
    if age == 'Teens' and 'Acne' in concerns:
        tips.append("💡 Salicylic acid and niacinamide are great for teen acne")

    return max(0, min(100, score)), warnings, tips

def show_results(ingredient_list, analysis, predictions, score, quiz=None):
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        color = "green" if score >= 70 else "orange" if score >= 40 else "red"
        st.markdown("### 🛡️ Safety Score")
        st.markdown(f"<h2 style='color:{color}'>{score}/100</h2>",
                    unsafe_allow_html=True)
    with col2:
        st.markdown("### 🌿 Beneficial")
        st.markdown(f"<h2 style='color:green'>{len(analysis['beneficial'])}</h2>",
                    unsafe_allow_html=True)
    with col3:
        st.markdown("### ⚠️ Irritants")
        st.markdown(f"<h2 style='color:orange'>{len(analysis['irritants'])}</h2>",
                    unsafe_allow_html=True)
    with col4:
        st.markdown("### 🚨 Harmful")
        st.markdown(f"<h2 style='color:red'>{len(analysis['harmful'])}</h2>",
                    unsafe_allow_html=True)

    st.markdown("---")

    # Quiz compatibility
    if quiz:
        st.subheader("🎯 Personalized Match Score")
        compat, warnings, tips = quiz_compatibility_score(quiz, predictions)
        color = "green" if compat >= 70 else "orange" if compat >= 40 else "red"
        st.markdown(
            f"<h2 style='color:{color}'>{compat}% Match for Your Skin Profile</h2>",
            unsafe_allow_html=True
        )
        for w in warnings:
            st.warning(w)
        for t in tips:
            st.success(t)
        st.markdown("---")

    # Skin type suitability
    st.subheader("👤 Suitable For")
    labels = [
        ('Dry/Combo/Normal Skin', predictions[0]),
        ('Oily/Combo/Normal Skin', predictions[1]),
        ('Acne-Prone Skin',        predictions[2]),
        ('Fragrance Sensitive',    predictions[3]),
    ]
    cols = st.columns(4)
    for col, (label, pred) in zip(cols, labels):
        with col:
            if pred == 1:
                st.success(f"✅ {label}")
            else:
                st.error(f"➖ {label}")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("✅ Beneficial Ingredients")
        if analysis['beneficial']:
            for i in analysis['beneficial']:
                info = ingredient_info.get(i, '')
                st.success(f"**{i.title()}**" + (f" — {info}" if info else ""))
        else:
            st.info("None from our database detected")

        st.subheader("⚠️ Irritants")
        if analysis['irritants']:
            for i in analysis['irritants']:
                st.warning(f"• {i.title()}")
        else:
            st.success("✅ No irritants detected!")

    with col_b:
        st.subheader("🚨 Harmful Ingredients")
        if analysis['harmful']:
            for i in analysis['harmful']:
                st.error(f"• {i.title()}")
        else:
            st.success("✅ No harmful ingredients!")

        st.subheader("🧴 Comedogenic Ingredients")
        if analysis['comedogenic']:
            for i in analysis['comedogenic']:
                st.warning(f"• {i.title()}")
        else:
            st.success("✅ No comedogenic ingredients!")

    st.markdown("---")
    st.subheader(f"📋 Full Ingredient List ({len(ingredient_list)} detected)")
    st.write(", ".join([i.title() for i in ingredient_list]))

# ── Sidebar Quiz ───────────────────────────────────────────────────────────
st.sidebar.title("🧴 Skin Profile Quiz")
st.sidebar.markdown("Answer for a **personalized match score**")

with st.sidebar:
    skin_type = st.selectbox(
        "1. What is your skin type?",
        ["Select...", "Oily", "Dry", "Combination", "Normal", "Sensitive"]
    )
    concerns = st.multiselect(
        "2. Main skin concerns?",
        [
            "Acne",
            "Anti-aging",
            "Brightening",
            "Hydration",
            "Pigmentation",
            "Hyperpigmentation",
            "Pores",
            "Redness",
            "Dark Spots",
            "Dullness",
            "Dehydration",
            "Sensitivity",
            "Uneven Texture",
            "Firmness / Elasticity",
            "Dark Circles",
            "Blackheads / Whiteheads",
            "Oiliness",
            "Eczema / Psoriasis",
        ]
    )
    allergies = st.multiselect(
        "3. Known allergies?",
        ["Fragrance", "Alcohol", "Nuts", "Gluten", "None"]
    )
    sensitivity = st.selectbox(
        "4. Skin sensitivity level?",
        ["Select...", "Low", "Medium", "High"]
    )
    age = st.selectbox(
        "5. Age range?",
        ["Select...", "Teens", "20s", "30s", "40s", "50+"]
    )

    quiz_complete = all([
        skin_type   != "Select...",
        len(concerns) > 0,
        sensitivity != "Select...",
        age         != "Select..."
    ])

    if quiz_complete:
        st.success("✅ Quiz complete! Analyze a product to see your match score.")
    else:
        st.info("Complete the quiz for personalized results")

quiz = {
    'skin_type':   skin_type,
    'concerns':    concerns,
    'allergies':   allergies,
    'sensitivity': sensitivity,
    'age':         age,
} if quiz_complete else None

# ── Main App ───────────────────────────────────────────────────────────────
st.title("🌸 DermIQ")
st.markdown("Upload a product label or paste ingredients for an instant analysis.")

tab1, tab2 = st.tabs(["✍️ Paste Ingredients", "📷 Upload Label Photo"])

with tab1:
    ingredient_text = st.text_area(
        "Paste your ingredient list here:",
        placeholder="e.g. Water, Glycerin, Niacinamide, Fragrance...",
        height=150
    )
    if st.button("🔍 Analyze", key="analyze_text"):
        if ingredient_text.strip():
            ingredient_list = parse_ingredients(ingredient_text)
            ingredient_list = normalize_ingredient_names(ingredient_list)
            analysis        = analyze(ingredient_list)
            features        = build_features(ingredient_list, analysis)
            predictions     = model.predict(features)[0]
            score           = safety_score(analysis, len(ingredient_list))
            st.markdown("---")
            show_results(ingredient_list, analysis, predictions, score, quiz)
        else:
            st.warning("Please paste some ingredients first!")

with tab2:
    st.markdown("📸 **Tips for best results:**")
    st.markdown(
        "- Ensure label is **flat and well-lit**\n"
        "- Avoid blurry or angled shots\n"
        "- **Crop to just the ingredient list** for best accuracy\n"
        "- ⚠️ *Beta feature — accuracy depends on image quality*"
    )
    uploaded_file = st.file_uploader(
        "Upload ingredient label photo",
        type=["jpg", "jpeg", "png"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Label", use_container_width=True)
        with st.spinner("🔍 Reading ingredients from image..."):
            extracted_text  = extract_text_from_image(image)
            ingredient_list = parse_ingredients(extracted_text)
            ingredient_list = normalize_ingredient_names(ingredient_list)
            analysis        = analyze(ingredient_list)
            features        = build_features(ingredient_list, analysis)
            predictions     = model.predict(features)[0]
            score           = safety_score(analysis, len(ingredient_list))

        if len(ingredient_list) == 0:
            st.error("❌ Could not detect ingredients. Try a clearer image or use the paste option.")
        else:
            st.success(f"✅ Detected {len(ingredient_list)} ingredients")
            st.markdown("---")
            show_results(ingredient_list, analysis, predictions, score, quiz)