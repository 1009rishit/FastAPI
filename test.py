# test_predict.py
from model import predict_verdict

# Example user input
age = 35
bmi = 26.4
gender = "male"

result = predict_verdict(age, bmi, gender)
print("Predicted Verdict:", result)
