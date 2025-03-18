from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

class EstoniaModel:
    """A class used to represent the Estonia Model for passenger survival prediction."""
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = []  # Dynamic feature list
        self.target = 'Survived'
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self._load_data()
    
    def _load_data(self):
        file_path = "datasets/estonia-passenger-list.csv"
        df = pd.read_csv(file_path)
        df.drop(columns=['PassengerId', 'Firstname', 'Lastname'], inplace=True)
        df['Sex'] = df['Sex'].apply(lambda x: 1 if x == 'M' else 0)
        onehot = self.encoder.fit_transform(df[['Category', 'Country']]).toarray()
        cols = list(self.encoder.get_feature_names_out(['Category', 'Country']))
        onehot_df = pd.DataFrame(onehot, columns=cols)
        df = pd.concat([df.drop(columns=['Category', 'Country']), onehot_df], axis=1)
        df.dropna(inplace=True)
        
        self.features = ['Sex', 'Age'] + cols
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
    
    def predict(self, passenger):
        passenger_df = pd.DataFrame([passenger])
        passenger_df['Sex'] = 1 if passenger_df['Sex'][0].lower() == 'male' else 0
        onehot = self.encoder.transform(passenger_df[['Category', 'Country']]).toarray()
        cols = list(self.encoder.get_feature_names_out(['Category', 'Country']))
        onehot_df = pd.DataFrame(onehot, columns=cols)
        passenger_df = pd.concat([passenger_df.drop(columns=['Category', 'Country']), onehot_df], axis=1)
        
        # Ensure all feature names match those used during training
        for col in self.features:
            if col not in passenger_df:
                passenger_df[col] = 0  # Add missing feature columns as 0
        passenger_df = passenger_df[self.features]  # Ensure correct order
        
        die, survive = np.squeeze(self.model.predict_proba(passenger_df))
        return {'die': die, 'survive': survive}

    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}
