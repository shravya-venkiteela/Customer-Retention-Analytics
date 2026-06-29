from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
import pandas as pd
import matplotlib.pyplot as plt
rfm = pd.read_csv(
    "rfm_customer_segments.csv"
)
print(rfm.head())

X = rfm[["Frequency", "Monetary"]]
y = rfm["Churn"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify = y
)
print(rfm["Segment"].value_counts())
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf.fit(X_train, y_train)

rf_pred = rf.predict(X_test)
rf_prob = rf.predict_proba(X_test)[:,1]

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:,1]
print("Accuracy:", accuracy_score(y_test, rf_pred))
print("Precision:", precision_score(y_test, rf_pred))
print("Recall:", recall_score(y_test, rf_pred))
print("F1-Score:", f1_score(y_test, rf_pred))
print("ROC-AUC:", roc_auc_score(y_test, rf_prob))

cm = confusion_matrix(y_test, pred)
print("Confusion Matrix:")
print(cm)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

fpr, tpr, _ = roc_curve(y_test, prob)
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], "--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Logistic Regression")
plt.show()
plt.savefig("roc_curve.png")

coef_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_[0]
})
print(coef_df)
results = pd.DataFrame({
    "Model": ["Logistic Regression", "Random Forest"],
    "Accuracy": [accuracy_score(y_test, pred), accuracy_score(y_test, rf_pred)],
    "Precision": [precision_score(y_test, pred), precision_score(y_test, rf_pred)],
    "Recall": [recall_score(y_test, pred), recall_score(y_test, rf_pred)],
    "F1": [f1_score(y_test, pred), f1_score(y_test, rf_pred)],
    "ROC-AUC": [roc_auc_score(y_test, prob), roc_auc_score(y_test, rf_prob)]
})
print(results)

customer_dashboard = (
    rfm.merge(
        df.groupby("CustomerID")["Country"].first().reset_index(),
        on="CustomerID",
        how="left"
    )
)

customer_dashboard.to_csv(
    "customer_dashboard.csv",
    index=False
)

