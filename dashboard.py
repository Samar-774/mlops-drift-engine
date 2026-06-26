import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
from app.database import engine

st.title("Drift Detection Dashboard")

st.header("Recent Predictions")
read_pred=pd.read_sql("SELECT * FROM prediction_logs",engine)
st.dataframe(read_pred)

st.header("Drift Alerts")
read_alerts=pd.read_sql("SELECT * FROM drift_alerts",engine)
st.dataframe(read_alerts)

st.header("Distribution Comparison")
features=json.load(open('model/training_stats.json'))
selected=st.selectbox('Select a feature',features.keys())
st.write(f'the selected feature is {selected}')




