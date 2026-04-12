import os

folders = [ "data/raw",
    "data/processed",
    "data/knowledge_base",
    "notebooks",
    "src",
    "models",
    "app",
    "tests",]

files = ["src/__init__.py",
    "src/preprocessing.py",
    "src/features.py",
    "src/model.py",
    "src/similarity.py",
    "app/streamlit_app.py",
    "tests/test_preprocessing.py",
    "models/.gitkeep",
    "requirements.txt",
    "README.md",
    ".gitignore",]

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print("Folders Created")

for file in files:
    with open(file, "w") as f:
        pass
    print("Files Created")

print("Project structure successfully created")