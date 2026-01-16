
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

class AcademicModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.train()

    def train(self):
        # Determine path to dataset
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_path, 'dataset', 'student_data.csv')
        
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found at {data_path}")

        df = pd.read_csv(data_path)
        
        # Features and Target
        X = df[['attendance', 'quiz_score', 'assignment_score', 'study_hours', 'midterm_score']]
        y = df['result'].apply(lambda x: 1 if x == 'Pass' else 0)

        self.model.fit(X, y)
        self.is_trained = True
        print("Model trained successfully on startup.")

    def predict_risk(self, attendance, quiz, assignment, hours, midterm):
        if not self.is_trained:
            self.train()
        
        input_data = pd.DataFrame([[attendance, quiz, assignment, hours, midterm]], 
                                 columns=['attendance', 'quiz_score', 'assignment_score', 'study_hours', 'midterm_score'])
        
        # Predict probability of class 1 (Pass)
        # Probabilities are [P(Fail), P(Pass)]
        probs = self.model.predict_proba(input_data)[0]
        pass_probability = probs[1]
        
        # Risk = 1 - P(Pass)
        risk_score = 1 - pass_probability
        return float(risk_score)
