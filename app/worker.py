from celery import Celery
# from celery.schedules import crontab
from scipy.stats import ks_2samp
import json, numpy as np
from app.database import SessionLocal
from app.models import PredictionLog

celery_app = Celery(
    'drift_monitor',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.beat_schedule = {
    'check-drift-every-two-minutes': {
        'task': 'app.worker.check_drift',
        'schedule': 120,
    },
}
def compute_psi(train_sample,prod_values,bins=10):
    train_counts, train_bin_edges = np.histogram(train_sample, bins)
    prod_counts, prod_bin_edges = np.histogram(prod_values, bins=train_bin_edges)
    train_pct = train_counts / np.sum(train_counts)
    prod_pct = prod_counts / np.sum(prod_counts)
    train_pct = np.where(train_pct == 0, 1e-10, train_pct)
    prod_pct=np.where(prod_pct==0,1e-10,prod_pct)
    psi_values = (prod_pct - train_pct) * np.log(prod_pct / train_pct)
    psi = np.sum(psi_values)

    return psi

@celery_app.task
def check_drift():
    training_stats=json.load(open('model/training_stats.json'))
    
    db=SessionLocal()
    recent_logs=db.query(PredictionLog).order_by(PredictionLog.timestamp.desc()).limit(100).all()
    db.close()
    
    drift_report = {}

    for feature in training_stats:
        prod_values = [getattr(row, feature) for row in recent_logs]
    
        train_mean = training_stats[feature]['mean']
        train_std = training_stats[feature]['std']
        train_sample = np.random.normal(train_mean, train_std, 1000)
    
        stat, p_value = ks_2samp(train_sample, prod_values)
        psi=compute_psi(train_sample,prod_values,bins=10)
        
    
        drift_report[feature] = {
            'ks_stat': float(stat),
            'p_value': float(p_value),
            'drifted': bool(p_value<0.05),
            'psi'    : float(psi)
        }
    
    print(drift_report)
    return drift_report


