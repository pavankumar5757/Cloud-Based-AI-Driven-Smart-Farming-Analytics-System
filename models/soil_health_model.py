import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from config import Config
from utils.ml_utils import save_model, load_model

class SoilHealthAnalyzer:
    def __init__(self):
        self.model_path = Config.SOIL_HEALTH_MODEL_PATH
        self.model = None
        if os.path.exists(self.model_path):
            self.model = load_model(self.model_path)
        else:
            self._train_and_save_default()

    def _generate_data(self, n: int = 800) -> pd.DataFrame:
        rng = np.random.default_rng(7)
        ph = rng.normal(6.8, 0.8, n).clip(4.5, 8.5)
        n_val = rng.uniform(20, 120, n)
        p_val = rng.uniform(5, 60, n)
        k_val = rng.uniform(50, 300, n)
        om = rng.uniform(1.0, 6.0, n)
        moisture = rng.uniform(10, 60, n)
        health = []
        for i in range(n):
            score = 0
            score += 30 - abs(ph[i] - 6.5) * 10
            score += 0.2 * (n_val[i] - 60)
            score += 0.3 * (p_val[i] - 30)
            score += 0.1 * (k_val[i] - 150)
            score += 5 * (om[i] - 3)
            score += 0.1 * (moisture[i] - 30)
            health.append(score)
        health = np.array(health)
        cls = np.where(health > 10, 2, np.where(health > -10, 1, 0))  # 0=poor,1=fair,2=good
        return pd.DataFrame({
            "pH": ph,
            "nitrogen": n_val,
            "phosphorus": p_val,
            "potassium": k_val,
            "organic_matter": om,
            "moisture": moisture,
            "label": cls,
        })

    def _train_and_save_default(self) -> None:
        df = self._generate_data()
        X = df.drop(columns=["label"]) ; y = df["label"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
        clf = RandomForestClassifier(n_estimators=250, random_state=7)
        clf.fit(X_train, y_train)
        acc = accuracy_score(y_test, clf.predict(X_test))
        if acc < 0.9:
            clf.set_params(n_estimators=400, max_depth=None)
            clf.fit(X, y)
        save_model(clf, self.model_path)
        self.model = clf

    def analyze_from_json(self, payload: dict) -> dict:
        df = pd.DataFrame([payload])
        proba = self.model.predict_proba(df)[0]
        pred = int(self.model.predict(df)[0])
        health_score = int(round((proba[2] * 100) + (proba[1] * 70) + (proba[0] * 40)))
        status = ["poor", "fair", "good"][pred]
        recommendations = []
        if df.loc[0, "pH"] < 6.0:
            recommendations.append("Apply agricultural lime to raise pH towards 6.5.")
        if df.loc[0, "nitrogen"] < 50:
            recommendations.append("Apply nitrogen-rich fertilizer (urea) 60-90 kg/ha.")
        if df.loc[0, "organic_matter"] < 2.0:
            recommendations.append("Incorporate compost/green manure to increase organic matter.")
        return {
            "health_score": max(0, min(100, health_score)),
            "nutrient_status": status,
            "fertilizer_recommendations": recommendations,
            "probabilities": {"poor": float(proba[0]), "fair": float(proba[1]), "good": float(proba[2])},
        }

