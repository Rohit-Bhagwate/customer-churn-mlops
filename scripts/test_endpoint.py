import boto3
import json

runtime = boto3.client('sagemaker-runtime')

endpoint_name = "sagemaker-scikit-learn-2026-05-07-10-10-01-551"

payload = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "PaperlessBilling": "Yes",
    "MonthlyCharges": 70.5,
    "TotalCharges": 800.5,
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaymentMethod": "Electronic check"
}

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=json.dumps(payload)
)

result = response['Body'].read().decode()

print("Prediction:",result)