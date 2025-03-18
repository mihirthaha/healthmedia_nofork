from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

class CancerModel:
    _instance = None

    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['age', 'year']
        self.target = 'status'
        self.cancer_data = pd.read_csv('datasets/haberman.csv', header=None, names=['age', 'year', 'nodes', 'status'])
        self.encoder = OneHotEncoder(handle_unknown='ignore')

    def _clean(self):
        self.cancer_data['age'] = pd.to_numeric(self.cancer_data['age'], errors='coerce')
        self.cancer_data['year'] = pd.to_numeric(self.cancer_data['year'], errors='coerce')
        self.cancer_data.drop(columns=['nodes'], inplace=True)
        self.cancer_data.dropna(inplace=True)

    def _train(self):
        X = self.cancer_data[self.features]
        y = self.cancer_data[self.target]
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict(self, patient_data):
        patient_df = pd.DataFrame(patient_data, index=[0])
        probabilities = self.model.predict_proba(patient_df)[0]
        return {'die': probabilities[1], 'survive': probabilities[0]}

    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)} 

def initCancer():
    CancerModel.get_instance()
