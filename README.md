Here’s clean, well-formatted content you can copy-paste directly into your `README.md`:

---

# 🧬 Gene Data Classification using Machine Learning

An end-to-end machine learning project for classifying **gene families** based on DNA sequence data.
This system predicts gene family types such as:

* G-protein coupled receptors
* Tyrosine kinase
* Tyrosine phosphatase
* Synthetase
* Synthase
* Ion channel
* Transcription factor

---

## 📁 Project Structure

```
gene-classification/
│
├── src/                     # Backend & ML pipeline
│   ├── step2_load_clean.py   # Load and clean DNA sequence data
│   ├── step3_split.py        # Train/validation/test split
│   ├── step4_kmer_features.py# Feature extraction (K-mer encoding)
│   ├── step5_train_models.py # Model training (RF, SVM, XGB)
│   ├── step6_eval_test.py    # Evaluation metrics
│   ├── step7_pack.py         # Save best model and metadata
│   └── api.py                # FastAPI app for predictions
│
├── models/                   # Trained model + metadata
│   ├── model.joblib
│   └── metadata.json
│
├── frontend_app.py           # Flask UI for interactive predictions
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd gene-classification
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1       # Windows
# or
source .venv/bin/activate          # Linux / Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🧠 Model Training Steps

1. **Load & clean data** → `python src/step2_load_clean.py`
2. **Split data** → `python src/step3_split.py`
3. **Generate K-mer features** → `python src/step4_kmer_features.py`
4. **Train models** → `python src/step5_train_models.py`
5. **Evaluate test results** → `python src/step6_eval_test.py`
6. **Package final model** → `python src/step7_pack.py`

Final chosen model → **XGBoost**, validation F1-score ≈ **0.89**.

---

## 🌐 Running the App

### 🧩 Start FastAPI Backend

```bash
uvicorn src.api:app --reload --port 8000
```

Backend runs at → **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### 🧭 Start Flask Frontend

```bash
python frontend_app.py
```

Frontend runs at → **[http://127.0.0.1:5500](http://127.0.0.1:5500)**

---

## 🧪 Example Prediction

**Input DNA sequences:**

```
ATGCCCACATAAATACCGTA
GTTACGGAAATCTGTTGCTTC
CCTGATAGCGTCTTAGGCTA
```

**Predicted Output:**

| Sequence              | Class ID | Class Name           |
| --------------------- | -------- | -------------------- |
| ATGCCCACATAAATACCGTA  | 1        | Tyrosine kinase      |
| GTTACGGAAATCTGTTGCTTC | 6        | Transcription factor |
| CCTGATAGCGTCTTAGGCTA  | 4        | Synthase             |

---

## 🧾 Notes

* Built with **Python**, **scikit-learn**, **xgboost**, **FastAPI**, and **Flask**.
* Model and metadata stored in `/models/`.
* `.gitignore` excludes large or temporary files.

---

## 🧑‍💻 Contributors

**Aryan Sahu** — Bangalore Institute of Technology
USN: 1BI23CD005
Dept: CSE (Data Science)

---

