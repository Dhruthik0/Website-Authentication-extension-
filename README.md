# Phishing Website Detector (Python)

This project detects phishing URLs using **two different models**:

- 🧠 **Random Forest** on handcrafted URL features  
- 🔤 **Character-level CNN** on raw URL strings  

It also includes a **FastAPI** backend and an optional **Streamlit UI** for easy interaction.

---

## 🚀 Features

- Extracts meaningful features from URLs (length, special chars, TLD, etc.)
- Trains:
  - A **Random Forest** model on engineered URL features
  - A **CharCNN** model on raw character sequences
- Unified evaluation script for both models
- **FastAPI** endpoint to serve predictions
- Optional **Streamlit** web interface for demo / visualization

---

## 🛠 Tech Stack

- Python
- scikit-learn
- PyTorch (for CharCNN)
- FastAPI
- Uvicorn
- Streamlit
- Pandas, NumPy

---
.
├── api.py
├── app.py                  # (optional) Streamlit app
├── requirements.txt
├── data
│   └── raw
│       └── phishing.csv
├── models                  # saved RF / CNN models
├── src
│   ├── train_rf.py
│   ├── train_cnn.py
│   ├── evaluate.py
│   ├── features.py
│   └── dataset.py
└── README.md

