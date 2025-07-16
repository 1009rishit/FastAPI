# predict.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pandas as pd
from data import df  

gender_encoder = LabelEncoder()
df['gender'] = gender_encoder.fit_transform(df['gender'])

verdict_encoder = LabelEncoder()
df['verdict'] = verdict_encoder.fit_transform(df['verdict'])

X = df[['age', 'bmi', 'gender']]
y = df['verdict']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))


def predict_verdict(age: int, bmi: float, gender: str):
    gender_encoded = gender_encoder.transform([gender])[0]  
    input_df = pd.DataFrame([[age, bmi, gender_encoded]], columns=['age', 'bmi', 'gender'])
    prediction = model.predict(input_df)[0]
    return verdict_encoder.inverse_transform([prediction])[0]
