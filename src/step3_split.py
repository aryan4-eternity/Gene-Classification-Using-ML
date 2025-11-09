import pandas as pd
from sklearn.model_selection import train_test_split
from labels import SEED

df = pd.read_csv("artifacts/all_clean.csv")
trainval, test = train_test_split(df, test_size=0.20, stratify=df["class"], random_state=SEED)
train, val = train_test_split(trainval, test_size=0.20, stratify=trainval["class"], random_state=SEED)

train.to_csv("artifacts/train.csv", index=False)
val.to_csv("artifacts/val.csv", index=False)
test.to_csv("artifacts/test.csv", index=False)
print(train.shape, val.shape, test.shape)
