import numpy as np
import requests

API_URL='http://localhost:8000/predict'

def genrate_random_customer():
    return{
        'SeniorCitizen': float(np.random.uniform(0,1)),
        'tenure': float(np.random.uniform(0,72)),
        'MonthlyCharges': float(np.random.uniform(18,118)),
        'TotalCharges': float(np.random.uniform(0,8000)),
        'gender_Female': float(np.random.uniform(0,1)),
        'gender_Male': float(np.random.uniform(0,1)),
        'Partner_No': float(np.random.uniform(0,1)),
        'Partner_Yes': float(np.random.uniform(0,1)),
        'Dependents_No': float(np.random.uniform(0,1)),
        'Dependents_Yes': float(np.random.uniform(0,1)),
        'PhoneService_No': float(np.random.uniform(0,1)),
        'PhoneService_Yes': float(np.random.uniform(0,1)),
        'MultipleLines_No': float(np.random.uniform(0,1)),
        'MultipleLines_No_phone_service': float(np.random.uniform(0,1)),
        'MultipleLines_Yes': float(np.random.uniform(0,1)),
        'InternetService_DSL': float(np.random.uniform(0,1)),
        'InternetService_Fiber_optic': float(np.random.uniform(0,1)),
        'InternetService_No': float(np.random.uniform(0,1)),
        'OnlineSecurity_No': float(np.random.uniform(0,1)),
        'OnlineSecurity_No_internet_service': float(np.random.uniform(0,1)),
        'OnlineSecurity_Yes': float(np.random.uniform(0,1)),
        'OnlineBackup_No': float(np.random.uniform(0,1)),
        'OnlineBackup_No_internet_service': float(np.random.uniform(0,1)),
        'OnlineBackup_Yes': float(np.random.uniform(0,1)),
        'DeviceProtection_No': float(np.random.uniform(0,1)),
        'DeviceProtection_No_internet_service': float(np.random.uniform(0,1)),
        'DeviceProtection_Yes': float(np.random.uniform(0,1)),
        'TechSupport_No': float(np.random.uniform(0,1)),
        'TechSupport_No_internet_service': float(np.random.uniform(0,1)),
        'TechSupport_Yes': float(np.random.uniform(0,1)),
        'StreamingTV_No': float(np.random.uniform(0,1)),
        'StreamingTV_No_internet_service': float(np.random.uniform(0,1)),
        'StreamingTV_Yes': float(np.random.uniform(0,1)),
        'StreamingMovies_No': float(np.random.uniform(0,1)),
        'StreamingMovies_No_internet_service': float(np.random.uniform(0,1)),
        'StreamingMovies_Yes': float(np.random.uniform(0,1)),
        'Contract_Month_to_month': float(np.random.uniform(0,1)),
        'Contract_One_year': float(np.random.uniform(0,1)),
        'Contract_Two_year': float(np.random.uniform(0,1)),
        'PaperlessBilling_No': float(np.random.uniform(0,1)),
        'PaperlessBilling_Yes': float(np.random.uniform(0,1)),
        'PaymentMethod_Bank_transfer_automatic': float(np.random.uniform(0,1)),
        'PaymentMethod_Credit_card_automatic': float(np.random.uniform(0,1)),
        'PaymentMethod_Electronic_check': float(np.random.uniform(0,1)),
        'PaymentMethod_Mailed_check': float(np.random.uniform(0,1)),
    }

for i in range(50):
    customer=genrate_random_customer()
    response=requests.post(API_URL,json=customer)
    print(f'Request {i+1}:{response.json()}')