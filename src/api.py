# src/api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json, joblib, numpy as np, re
from pathlib import Path

# import from the same folder (src)
from .labels import CLASS_MAP

# ----- config -----
ROOT = Path(__file__).resolve().parents[1]   # project root
MODELS = ROOT / "models"
MODEL_PATH = MODELS / "model.joblib"
META_PATH  = MODELS / "metadata.json"

# ----- utils -----
def clean(s: str) -> str:
    return re.sub(r"[^ACGT]", "", (s or "").upper())

def build_kmer_index(k: int):
    from itertools import product
    alphabet = "ACGT"
    return {"".join(p): i for i, p in enumerate(product(alphabet, repeat=k))}

def seq_to_vec(seq: str, idx: dict, k: int) -> np.ndarray:
    s = clean(seq)
    v = np.zeros(len(idx), dtype=np.float32)
    if len(s) >= k:
        for i in range(len(s) - k + 1):
            j = idx.get(s[i:i+k])
            if j is not None:
                v[j] += 1
    t = v.sum()
    if t: v /= t
    return v

# ----- app -----
app = FastAPI(title="Gene Classifier", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictIn(BaseModel):
    sequences: List[str]

# load model + metadata on startup
@app.on_event("startup")
def _load():
    if not MODEL_PATH.exists() or not META_PATH.exists():
        raise RuntimeError("Model not found. Run training and step7_pack.py first.")
    app.state.model = joblib.load(MODEL_PATH)
    meta = json.loads(META_PATH.read_text())
    app.state.k = int(meta["k"])
    app.state.idx = build_kmer_index(app.state.k)

@app.get("/status")
def status():
    return {"ok": True}

@app.get("/classes")
def classes():
    return {int(k): v for k, v in CLASS_MAP.items()}

@app.post("/predict")
def predict(inp: PredictIn):
    k = app.state.k
    idx = app.state.idx
    X = np.vstack([seq_to_vec(s, idx, k) for s in inp.sequences])
    try:
        ids = app.state.model.predict(X).astype(int).tolist()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    names = [CLASS_MAP[i] for i in ids]
    return {"pred": ids, "name": names}

@app.get("/")
def root():
    return {
        "service": "Gene Classifier API",
        "endpoints": ["/status", "/predict", "/docs"],
        "message": "Welcome to the Gene Classification API!"
    }
