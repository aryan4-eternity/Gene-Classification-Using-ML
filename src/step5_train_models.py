import numpy as np, joblib, json
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from labels import CLASS_MAP, SEED

def f1(model, X, y): return f1_score(y, model.predict(X), average="macro")

k=4
Xtr=np.load(f"artifacts/X_train_k{k}.npy"); ytr=np.load("artifacts/y_train.npy")
Xva=np.load(f"artifacts/X_val_k{k}.npy");   yva=np.load("artifacts/y_val.npy")

cands = {}

rf = RandomForestClassifier(n_estimators=600, n_jobs=-1, random_state=SEED)
rf.fit(Xtr, ytr); cands["rf"] = (rf, f1(rf, Xva, yva))

svm = CalibratedClassifierCV(LinearSVC(C=1.0, random_state=SEED), cv=5)
svm.fit(Xtr, ytr); cands["svm"] = (svm, f1(svm, Xva, yva))

xgb = XGBClassifier(
    n_estimators=600, max_depth=6, learning_rate=0.05,
    subsample=0.9, colsample_bytree=0.8,
    objective="multi:softmax", num_class=len(CLASS_MAP),
    eval_metric="mlogloss", tree_method="hist", random_state=SEED
)
xgb.fit(Xtr, ytr); cands["xgb"] = (xgb, f1(xgb, Xva, yva))

best_name, (best_model, best_score) = max(cands.items(), key=lambda kv: kv[1][1])
print("Val macro-F1:", {k: round(v[1],4) for k,v in cands.items()}, "->", best_name)

joblib.dump(best_model, f"artifacts/best_{best_name}.joblib")
json.dump({"k":k,"best":best_name,"val_macro_f1":float(best_score)}, open("artifacts/model_meta.json","w"), indent=2)
