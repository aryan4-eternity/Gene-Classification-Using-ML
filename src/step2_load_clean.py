import re, pandas as pd, pathlib
from labels import SEED

DATA = ["data/human_data.txt", "data/chimp_data.txt"]  # CSV or TSV with columns: sequence,class

def clean_sequence(s: str) -> str:
    s = (s or "").upper()
    return re.sub(r"[^ACGT]", "", s)

def load(paths):
    frames = []
    for p in paths:
        df = pd.read_csv(p, sep=None, engine="python")
        assert {"sequence","class"}.issubset(df.columns), f"Missing columns in {p}"
        df["sequence"] = df["sequence"].map(clean_sequence)
        df = df[df["sequence"].str.len() > 0].copy()
        df["class"] = df["class"].astype(int)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

if __name__ == "__main__":
    df = load(DATA)
    pathlib.Path("artifacts").mkdir(exist_ok=True)
    df.to_csv("artifacts/all_clean.csv", index=False)
    print(df.head())
