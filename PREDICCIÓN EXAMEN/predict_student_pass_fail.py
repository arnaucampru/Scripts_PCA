
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv('/Users/arnau/Documents/@PCA/student_prepared.csv')
print(df.head())
print(df.isna().sum())

print(df['Pass/Fail'].value_counts())

X = df[['age', 'studytime', 'failures', 'absences', 'G1', 'G2']] # qué usamos para predecir
y = df['Pass/Fail'] # qué queremos predecir

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(accuracy_score(y_test, y_pred))

print(classification_report(y_test, y_pred))