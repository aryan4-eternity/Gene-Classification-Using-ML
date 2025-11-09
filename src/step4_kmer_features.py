import itertools, numpy as np, pandas as pd

ALPH = "ACGT"
def build_vocab(k): 
    return {"".join(p): i for i,p in enumerate(itertools.product(ALPH, repeat=k))}

def kmer_vec(seq, k, idx):
    v = np.zeros(len(idx), dtype=np.float32)
    if len(seq) < k: return v
    for i in range(len(seq)-k+1):
        j = idx.get(seq[i:i+k])
        if j is not None: v[j]+=1
    s=v.sum()
    if s: v/=s
    return v

def transform(series, k):
    idx = build_vocab(k)
    return np.vstack([kmer_vec(s, k, idx) for s in series])

if __name__ == "__main__":
    k=4
    tr=pd.read_csv("artifacts/train.csv"); va=pd.read_csv("artifacts/val.csv"); te=pd.read_csv("artifacts/test.csv")
    Xtr, Xva, Xte = transform(tr.sequence,k), transform(va.sequence,k), transform(te.sequence,k)
    np.save(f"artifacts/X_train_k{k}.npy", Xtr)
    np.save(f"artifacts/X_val_k{k}.npy",   Xva)
    np.save(f"artifacts/X_test_k{k}.npy",  Xte)
    np.save("artifacts/y_train.npy", tr["class"].to_numpy())
    np.save("artifacts/y_val.npy",   va["class"].to_numpy())
    np.save("artifacts/y_test.npy",  te["class"].to_numpy())
