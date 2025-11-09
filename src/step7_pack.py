# src/step7_pack.py
import json, shutil
from pathlib import Path
from labels import CLASS_MAP

ART = Path("artifacts")
MODELS = Path("models")
MODELS.mkdir(parents=True, exist_ok=True)  # ensure dest exists

meta = json.load(open(ART / "model_meta.json"))
best = meta["best"]
src = ART / f"best_{best}.joblib"
dst = MODELS / "model.joblib"

if not src.exists():
    avail = list(ART.glob("best_*.joblib"))
    raise FileNotFoundError(f"Missing {src}. Available: {[p.name for p in avail]}")

shutil.copyfile(src, dst)
(json.dumps({"k": meta["k"], "classes": CLASS_MAP}, indent=2) and
 open(MODELS / "metadata.json", "w").write(json.dumps({"k": meta["k"], "classes": CLASS_MAP}, indent=2)))

print("Saved models/model.joblib and models/metadata.json")

