from enum import Enum
from sqlalchemy.orm import Session
from .models import DriftAlert
import json

class Severity(Enum):
    LOW='low'
    MEDIUM='medium'
    HIGH='high'

def classify_severity(psi):
    if(psi<0.1):
        return Severity.LOW
    if(psi<0.2):
        return Severity.MEDIUM
    else:
        return Severity.HIGH

class AlertManager():
    def create_alert(self,feature_name,ks_stat,p_value,psi,db:Session):
        severity=classify_severity(psi).value

        alert_log=DriftAlert(
            feature_name= str(feature_name),
            ks_stat     = float(ks_stat),
            p_value     = float(p_value),
            severity    = str(severity),
        )

        db.add(alert_log)
        db.commit()
        return alert_log
    
    def send_notification(self,feature_name,severity,ks_stat):
        alert_dict={'feature_name':feature_name,
              'severity':severity,
              'ks_stat':ks_stat,
              'status':'DRIFT DETECTED'}
        print(json.dumps(alert_dict,indent=2))




