import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score

SEED = 42
DATA_PATH = r"C:\Users\mtahr\OneDrive\Desktop\python 2\heart_disease_uci.csv"
MODEL_DIR = r"C:\Users\mtahr\OneDrive\Desktop\python 2\ml_project\ml_model"

df = pd.read_csv(DATA_PATH)
df.columns = [c.lower().strip() for c in df.columns]
df['target'] = (df['num'] > 0).astype(int)

exclude = ['target', 'num', 'id', 'dataset']
feature_cols = [c for c in df.columns if c not in exclude]
X = df[feature_cols].copy()
y = df['target'].copy()

cat_cols = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
num_cols = X.select_dtypes(include=[np.number]).columns.tolist()

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, num_cols),
    ('cat', categorical_transformer, cat_cols)
])

model = GradientBoostingClassifier(
    n_estimators=50,
    max_depth=3,
    learning_rate=0.1,
    random_state=SEED
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', model)
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)

print(f"Accuracy:  {acc:.4f}")
print(f"ROC-AUC:   {auc:.4f}")
print()
print(classification_report(y_test, y_pred, target_names=['Healthy', 'Disease']))

os.makedirs(MODEL_DIR, exist_ok=True)
pickle.dump(pipeline, open(os.path.join(MODEL_DIR, "full_pipeline.pkl"), "wb"))
pickle.dump(feature_cols, open(os.path.join(MODEL_DIR, "feature_names.pkl"), "wb"))
pickle.dump(cat_cols, open(os.path.join(MODEL_DIR, "cat_cols.pkl"), "wb"))
pickle.dump(num_cols, open(os.path.join(MODEL_DIR, "num_cols.pkl"), "wb"))

print(f"\nModel saved to {MODEL_DIR}")
