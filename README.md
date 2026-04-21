# 🌸 DermIQ — AI Skincare Ingredient Analyzer

> Decode your skincare products instantly. Know what's beneficial, harmful, or risky for your unique skin.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-red?style=flat-square)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-Sephora-pink?style=flat-square)

---

## 📌 Overview

**DermIQ** is an end-to-end Machine Learning application that analyzes skincare product ingredients and provides personalized safety insights. Users can either paste an ingredient list or upload a photo of a product label — DermIQ does the rest.

### What DermIQ Does

- 🌿 **Ingredient Analysis** — Detects beneficial, irritating, harmful, and comedogenic ingredients using a curated knowledge base
- 🛡️ **Safety Score** — Generates a 0–100 safety score based on the full ingredient profile
- 👤 **Skin Type Prediction** — ML model predicts suitability for dry, oily, and acne-prone skin
- 🎯 **Personalized Match Score** — Quiz-based compatibility score tailored to your skin profile
- 📷 **OCR Image Upload** — Extracts ingredients directly from product label photos using Tesseract OCR

---

## 🗂️ Project Structure

```
DermIQ/
│
├── app/
│   └── streamlit_app.py              ← Main web application
│
├── data/
│   ├── raw/                          ← Original Sephora dataset (not tracked)
│   ├── processed/                    ← Cleaned & feature-engineered data (not tracked)
│   └── knowledge_base/               ← Ingredient category definitions
│
├── notebooks/
│   ├── 01_data_exploration.ipynb     ← EDA on Sephora dataset
│   ├── 02_preprocessing.ipynb        ← Data cleaning & parsing
│   ├── 03_knowledge_base.ipynb       ← Building ingredient knowledge base
│   ├── 04_feature_engineering.ipynb  ← Feature creation & label engineering
│   └── 05_model_training.ipynb       ← Model training & evaluation
│
├── src/
│   ├── preprocessing.py              ← Data cleaning functions
│   ├── features.py                   ← Feature engineering functions
│   ├── model.py                      ← Training and prediction logic
│   └── similarity.py                 ← Ingredient similarity search (v2)
│
├── models/                           ← Saved trained models (not tracked)
├── tests/                            ← Unit tests
├── requirements.txt
├── setup_project.py                  ← Project skeleton setup script
└── README.md
```

---

## 🧠 ML Pipeline

```
Sephora Dataset (8,494 products)
         ↓
Filtering & Cleaning → 2,286 skincare products
         ↓
Ingredient Knowledge Base
(irritants / harmful / comedogenic / beneficial)
         ↓
Feature Engineering
(13 features: counts, ratios, binary flags)
         ↓
Random Forest Classifier (MultiOutputClassifier)
         ↓
Streamlit Web App + OCR Image Upload
```

---

## 📊 Dataset

| Property | Detail |
|---|---|
| Source | [Sephora Products & Skincare Reviews — Kaggle](https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews) |
| Total products | 8,494 |
| Skincare products used | 2,286 |
| Missing ingredients dropped | 134 (5.5%) |
| Key columns | `ingredients`, `highlights`, `primary_category`, `secondary_category` |

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌿 Ingredient Detection | Flags beneficial, irritant, harmful & comedogenic ingredients |
| 🛡️ Safety Score | 0–100 score computed from ingredient risk/benefit profile |
| 👤 Skin Type Prediction | Random Forest predicts dry, oily, acne-prone suitability |
| 🎯 Personalized Match | Quiz captures skin type, concerns, allergies, sensitivity & age |
| 📷 OCR Label Upload | Tesseract OCR reads ingredient text from product photos |
| ✍️ Manual Paste | Paste any ingredient list for instant analysis |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10
- Tesseract OCR Engine — [Download for Windows](https://github.com/UB-Mannheim/tesseract/wiki)

### Installation

```bash
# Clone the repository
git clone https://github.com/nandiniranjansinha/DermIQ.git
cd DermIQ

# Create virtual environment
py -3.10 -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app/streamlit_app.py
```

### Retrain the Model (Optional)

Run the notebooks in order:
```
01_data_exploration.ipynb
02_preprocessing.ipynb
03_knowledge_base.ipynb
04_feature_engineering.ipynb
05_model_training.ipynb
```

---

## 🔬 Model Details

| Property | Detail |
|---|---|
| Algorithm | Random Forest (MultiOutputClassifier) |
| Number of estimators | 100 |
| Training samples | 1,828 (80%) |
| Test samples | 458 (20%) |
| Input features | 13 engineered features |
| Output labels | `is_for_dry_skin`, `is_for_oily_skin`, `is_good_for_acne`, `is_fragrance_free` |
| Overall accuracy | ~80–88% depending on label |

### Feature List

| Feature | Type | Description |
|---|---|---|
| `total_ingredients` | Count | Total number of ingredients |
| `irritants_count` | Count | Number of known irritants detected |
| `beneficial_count` | Count | Number of beneficial ingredients |
| `harmful_count` | Count | Number of harmful ingredients |
| `comedogenic_count` | Count | Number of pore-clogging ingredients |
| `irritants_ratio` | Ratio | Irritants / total ingredients |
| `beneficial_ratio` | Ratio | Beneficial / total ingredients |
| `harmful_ratio` | Ratio | Harmful / total ingredients |
| `comedogenic_ratio` | Ratio | Comedogenic / total ingredients |
| `has_fragrance` | Binary | Contains fragrance or parfum |
| `has_alcohol` | Binary | Contains alcohol denat |
| `has_harmful` | Binary | Any harmful ingredient present |
| `has_beneficial` | Binary | Any beneficial ingredient present |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10 | Core language |
| Pandas & NumPy | Data processing |
| Scikit-learn | ML model training & evaluation |
| Streamlit | Web application framework |
| Pytesseract | OCR for ingredient label photos |
| Pillow | Image preprocessing |
| Matplotlib & Seaborn | Data visualization |
| Regex | Ingredient text parsing |
| ast.literal_eval | Parsing list-formatted strings from CSV |

---

## 📋 Roadmap

- [x] Data collection & EDA
- [x] Data cleaning & preprocessing
- [x] Ingredient knowledge base
- [x] Feature engineering
- [x] ML model training
- [x] Streamlit web app
- [x] OCR image upload
- [x] Skin profile quiz
- [ ] Address class imbalance with SMOTE
- [ ] TF-IDF vectorization on full ingredient text
- [ ] Ingredient similarity search (NLP)
- [ ] SHAP explainability layer
- [ ] Deploy on Streamlit Cloud
- [ ] Expand knowledge base

---

## ⚠️ Known Limitations

- The ML model has class imbalance — minority class recall is lower than majority class. This is a known limitation to be addressed in v2 with SMOTE oversampling.
- OCR accuracy depends heavily on image quality. Works best with flat, well-lit, cropped label photos.
- Knowledge base covers common ingredients — rare or proprietary ingredients may not be flagged.

---

## 👩‍💻 Author

**Nandini Ranjan Sinha**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/nandiniranjansinha)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/nandiniranjansinha)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Sephora Products & Skincare Reviews Dataset](https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews) by Nadya Inkyu on Kaggle
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) by Google
- [Streamlit](https://streamlit.io) for the web framework
