import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import json
import os

df=pd.read_csv('data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df=df.drop(columns='customerID')
df['TotalCharges']=pd.to_numeric(df['TotalCharges'],errors='coerce')
df=df.dropna()


df['Churn']=df['Churn'].map({'Yes':1,'No':0})
y=df['Churn']
X=df.drop(columns='Churn')

X=pd.get_dummies(X,dtype=int)

X.columns=(X.columns
    .str.replace(' ','_')
    .str.replace('(','')
    .str.replace(')','')
    .str.replace('-','_')
    )

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

pipe=Pipeline([
    ("scaler",StandardScaler()),
    ("clf",LogisticRegression(max_iter=1000)),

])

pipe.fit(X_train,y_train)

os.makedirs('model',exist_ok=True)
joblib.dump(pipe,'model/model.pkl')
print('Model saved')

stats=X_train.describe()
training_stats={}

for col in X_train.columns:
    training_stats[col]= {
        'mean': float(stats.loc['mean'][col]),
        'std':  float(stats.loc['std'][col]),
        'p25':  float(stats.loc['25%'][col]),
        'p75':  float(stats.loc['75%'][col]),
    }

json.dump(training_stats,open('model/training_stats.json','w'))
print("Training data saved")