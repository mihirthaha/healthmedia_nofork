from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

class AccidentModel:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = []
        self.target = 'Survived'
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self._load_data()
    
    def _load_data(self):
        file_path = "datasets/accident.csv"
        df = pd.read_csv(file_path)
        df.drop(columns=['Age'], inplace=True)
        df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
        onehot = self.encoder.fit_transform(df[['Helmet_Used', 'Seatbelt_Used']]).toarray()
        cols = list(self.encoder.get_feature_names_out(['Helmet_Used', 'Seatbelt_Used']))
        onehot_df = pd.DataFrame(onehot, columns=cols)
        df = pd.concat([df.drop(columns=['Helmet_Used', 'Seatbelt_Used']), onehot_df], axis=1)
        df.dropna(inplace=True)
        
        self.features = ['Gender', 'Speed_of_Impact'] + cols
        X = df[self.features]
        y = df[self.target]
        
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def predict(self, accident):
        accident_df = pd.DataFrame([accident])
        accident_df['Gender'] = 1 if accident_df['Gender'][0].lower() == 'male' else 0
        onehot = self.encoder.transform(accident_df[['Helmet_Used', 'Seatbelt_Used']]).toarray()
        cols = list(self.encoder.get_feature_names_out(['Helmet_Used', 'Seatbelt_Used']))
        onehot_df = pd.DataFrame(onehot, columns=cols)
        accident_df = pd.concat([accident_df.drop(columns=['Helmet_Used', 'Seatbelt_Used']), onehot_df], axis=1)
        
        for col in self.features:
            if col not in accident_df:
                accident_df[col] = 0
        accident_df = accident_df[self.features]
        
        die, survive = np.squeeze(self.model.predict_proba(accident_df))
        return {'die': die, 'survive': survive}

    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}
