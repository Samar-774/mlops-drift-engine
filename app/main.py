from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from .database import engine,get_db
from .models import PredictionLog,Base
from .models import DriftAlert
from pydantic import BaseModel
import joblib
import numpy as np


Base.metadata.create_all(bind=engine)
app=FastAPI()
model=joblib.load('model/model.pkl')

class PredictionRequest(BaseModel):
    SeniorCitizen: float
    tenure: float
    MonthlyCharges: float
    TotalCharges: float
    gender_Female: float
    gender_Male: float
    Partner_No: float
    Partner_Yes: float
    Dependents_No: float
    Dependents_Yes: float
    PhoneService_No: float
    PhoneService_Yes: float
    MultipleLines_No: float
    MultipleLines_No_phone_service: float
    MultipleLines_Yes: float
    InternetService_DSL: float
    InternetService_Fiber_optic: float
    InternetService_No: float
    OnlineSecurity_No: float
    OnlineSecurity_No_internet_service: float
    OnlineSecurity_Yes: float
    OnlineBackup_No: float
    OnlineBackup_No_internet_service: float
    OnlineBackup_Yes: float
    DeviceProtection_No: float
    DeviceProtection_No_internet_service: float
    DeviceProtection_Yes: float
    TechSupport_No: float
    TechSupport_No_internet_service: float
    TechSupport_Yes: float
    StreamingTV_No: float
    StreamingTV_No_internet_service: float
    StreamingTV_Yes: float
    StreamingMovies_No: float
    StreamingMovies_No_internet_service: float
    StreamingMovies_Yes: float
    Contract_Month_to_month: float
    Contract_One_year: float
    Contract_Two_year: float
    PaperlessBilling_No: float
    PaperlessBilling_Yes: float
    PaymentMethod_Bank_transfer_automatic: float
    PaymentMethod_Credit_card_automatic: float
    PaymentMethod_Electronic_check: float
    PaymentMethod_Mailed_check: float

@app.post('/predict')
def predict(request:PredictionRequest, db: Session=Depends(get_db)):
    X=np.array([list(request.model_dump().values())])
    pred=model.predict(X)[0]
    prob=model.predict_proba(X)[0][1]

    log=PredictionLog(
        prediction=int(pred),
        probability=float(prob),

        **request.model_dump()
    )

    db.add(log)
    db.commit()
    return {"prediction": int(pred), "probability": (prob)}

@app.get('/logs')
def get_logs(limit: int= 100 , db:Session=Depends(get_db)):
    logs=db.query(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(limit).all()
    return logs

@app.get('/alerts')
def get_alerts(limit: int=100,db:Session=Depends(get_db)):
    alerts=db.query(DriftAlert).order_by(DriftAlert.timestamp.desc()).limit(limit).all()
    return alerts

@app.get('/alerts/latest')
def get_latest(db:Session=Depends(get_db)):
    latest=db.query(DriftAlert).order_by(DriftAlert.timestamp.desc()).first()
    return latest