import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
from app.database import engine
from simulate import generate_random_customer
import requests
from concurrent.futures import ThreadPoolExecutor

st.title("Drift Detection Dashboard")

read_pred=pd.read_sql("SELECT * FROM prediction_logs",engine)
read_alerts=pd.read_sql("SELECT * FROM drift_alerts",engine)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total predictions", len(read_pred))
with col2:
    st.metric("High Severity Features", read_alerts[read_alerts['severity'] == 'high']['feature_name'].nunique())
with col3:
    st.metric("Latest Alert Severity", read_alerts.iloc[0]['severity'].upper())

st.info("Note: Sending 50 predictions may take up to 15 seconds. Please wait.")
if st.button("Send 50 Random Predictions"):
    with st.spinner("Sending predictions..."):        
        def send_request(_):                          
            customer = generate_random_customer()     
            requests.post("http://localhost:8000/predict", json=customer)  

        with ThreadPoolExecutor(max_workers=10) as executor:  
            executor.map(send_request, range(50)) 

    st.success("50 predictions sent!")
    st.rerun()


left, right = st.columns(2)

with left:
    st.header("Recent Predictions")
    st.dataframe(read_pred[['id','timestamp','prediction','probability']].tail(10), use_container_width=True)

with right:
    st.header("Drift Alerts")
    st.dataframe(read_alerts[['feature_name','severity','ks_stat','timestamp']].head(20), use_container_width=True)

st.header("Distribution Comparison")
features=json.load(open('model/training_stats.json'))
selected=st.selectbox('Select a feature',features.keys())
mean = features[selected]['mean']
std  = features[selected]['std']

train_values=np.random.normal(mean,std,1000)
prod_values=read_pred[selected]

fig = go.Figure()
fig.update_layout(
    barmode='overlay',
    title=f'Distribution: {selected}'
    )
fig.add_trace(go.Histogram(x=train_values, name="Training", opacity=0.7))
fig.add_trace(go.Histogram(x=prod_values, name="Production", opacity=0.7))
fig.update_layout(barmode='overlay')
st.plotly_chart(fig)


