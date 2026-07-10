# PRD — DermIQ: AI Skincare Ingredient Analyzer

**Author:** Nandini Ranjan Sinha
**Status:** Shipped (v1) — [Live Demo](https://derm--iq.streamlit.app)
**Last updated:** 2026

---

## 1. Problem Statement

Skincare ingredient labels are long, use INCI (chemical) naming, and are effectively unreadable to the average consumer. Shoppers can't tell, in the moment of a purchase decision, whether a product contains irritants, comedogenic ingredients, or actives that actually suit their skin type — they either trust marketing copy or skip the check entirely.

**Who this is for:** consumers making a skincare purchase decision (in-store or online) who want a fast, ingredient-level safety read without manually researching each compound.

## 2. Goal

Let a user photograph or paste a product's ingredient list and get back, in seconds:
1. A **0–100 safety score** for that product
2. A **flagged breakdown** of irritant / comedogenic / harmful / beneficial ingredients
3. A **personalized compatibility score** against their own skin profile

## 3. Non-Goals (v1)

- Not a medical or dermatological diagnostic tool — scoring is rule-based + ML classification, not clinical.
- Not a product recommendation engine across a catalog — v1 scores one product at a time.
- No user accounts / saved history in v1.

## 4. Solution Overview

### 4.1 Ingredient Input
- **Manual paste** — user pastes a raw ingredient list.
- **OCR label scan** — user uploads a photo; image is preprocessed (grayscale, contrast/brightness enhancement, upscaling) and passed through Tesseract OCR, then parsed to strip storage/warning text and normalize ingredient names (e.g., "vitamin e acetate" → "tocopheryl acetate").

### 4.2 Ingredient Knowledge Base
A curated lookup table classifies each parsed ingredient into one of four categories:
- **Irritants** (e.g., fragrance, denatured alcohol, menthol)
- **Comedogenic** (e.g., coconut oil, isopropyl myristate)
- **Harmful** (e.g., parabens, formaldehyde-releasers, BHA/BHT)
- **Beneficial** (e.g., niacinamide, hyaluronic acid, retinol) — each mapped to a plain-language benefit description shown to the user.

### 4.3 Safety Score
A deterministic score starting at 100, penalized per irritant (-10), harmful ingredient (-15), and comedogenic ingredient (-8), and boosted per beneficial ingredient (+5), clamped to 0–100.

### 4.4 Skin-Type Suitability Model
A `MultiOutputClassifier` wrapping a `RandomForestClassifier` (100 estimators), trained on 13 engineered features (ingredient counts/ratios per category, binary flags for fragrance/alcohol/harmful/beneficial presence) derived from 2,286 skincare products (filtered from a base of 8,494). Predicts four independent binary labels: suitability for dry skin, oily skin, acne-prone skin, and fragrance-free status. Reached 80–90% classification accuracy across the four labels on a held-out test split.

### 4.5 Personalized Quiz & Compatibility Score
A short quiz captures the user's skin type, concerns, known allergies, sensitivity level, and age band. This is combined with the model's per-product predictions to compute a personalized compatibility score and generate tailored warnings/tips (e.g., flagging a fragrance-containing product for a user who marked high sensitivity).

## 5. Success Metrics (v1, self-evaluated)
- Model accuracy: 80–90% across all 4 skin-type labels (test split).
- OCR pipeline: qualitatively validated against real product label photos during manual usability testing; ingredient-parsing edge cases (multi-line labels, storage-text bleed) iterated on directly based on failures observed.

## 6. Key Risks / Open Questions Going In
- OCR accuracy varies significantly with photo quality/lighting — mitigated with a preprocessing pipeline (contrast, sharpening, upscaling) but not solved for all label types.
- Ingredient knowledge base is manually curated and static — does not scale to ingredients outside the curated lists without a manual update.
- Safety score weights (-10/-15/-8/+5) are heuristic, not derived from a validated dermatological severity scale — acceptable for v1 given the tool's non-clinical framing (see Non-Goals).

## 7. Shipped Scope (v1)
- ✅ OCR label scanning + manual paste input
- ✅ Ingredient classification against curated knowledge base
- ✅ 0–100 safety score
- ✅ ML-based skin-type suitability prediction (4 labels)
- ✅ Quiz-based personalized compatibility scoring
- ✅ Streamlit web app, publicly deployed
