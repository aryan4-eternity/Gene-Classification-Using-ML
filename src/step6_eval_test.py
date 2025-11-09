# src/step6_eval_test.py
import numpy as np, joblib, json
from sklearn.metrics import classification_report, confusion_matrix
from labels import CLASS_MAP

meta = json.load(open("artifacts/model_meta.json"))
model = joblib.load(f"artifacts/best_{meta['best']}.joblib")
k = meta["k"]

Xte = np.load(f"artifacts/X_test_k{k}.npy")
yte = np.load("artifacts/y_test.npy")

yp = model.predict(Xte)

# 1) human-readable printout
print(classification_report(yte, yp, target_names=[CLASS_MAP[i] for i in sorted(CLASS_MAP)], digits=4))
cm = confusion_matrix(yte, yp)
print("Confusion matrix:\n", cm)

# 2) JSON-safe objects
report_dict = classification_report(
    yte, yp, target_names=[CLASS_MAP[i] for i in sorted(CLASS_MAP)], digits=4, output_dict=True
)
cm_list = cm.astype(int).tolist()   # <- convert numpy.int64 -> int

with open("artifacts/test_report.json", "w") as f:
    json.dump({"report": report_dict, "cm": cm_list}, f, indent=2)
