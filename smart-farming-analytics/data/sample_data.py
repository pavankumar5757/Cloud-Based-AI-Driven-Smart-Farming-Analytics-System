import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.dirname(__file__)

def generate_crop_yield(n: int = 1200) -> pd.DataFrame:
    rng = np.random.default_rng(1)
    soil_types = ["sandy", "loamy", "clay", "silt"]
    soil_type = rng.choice(soil_types, n)
    temperature = rng.normal(24, 6, n)
    humidity = rng.uniform(35, 95, n)
    rainfall = rng.gamma(2.0, 35.0, n)
    fertilizer_amount = rng.uniform(40, 260, n)
    irrigation_frequency = rng.integers(1, 12, n)
    base = 2 + 0.1 * (temperature - 20) + 0.03 * humidity + 0.015 * rainfall
    base += 0.02 * fertilizer_amount + 0.2 * irrigation_frequency
    soil_factor = np.array([1.0 if s == "loamy" else 0.9 if s == "silt" else 0.8 if s == "sandy" else 0.85 for s in soil_type])
    noise = rng.normal(0, 2.5, n)
    yield_tons = (base * soil_factor) + noise
    return pd.DataFrame({
        "soil_type": soil_type,
        "temperature": temperature,
        "humidity": humidity,
        "rainfall": rainfall,
        "fertilizer_amount": fertilizer_amount,
        "irrigation_frequency": irrigation_frequency,
        "yield": yield_tons,
    })

def generate_soil_health(n: int = 600) -> pd.DataFrame:
    rng = np.random.default_rng(2)
    ph = rng.normal(6.7, 0.9, n).clip(4.5, 8.8)
    n_val = rng.uniform(15, 130, n)
    p_val = rng.uniform(4, 65, n)
    k_val = rng.uniform(40, 320, n)
    om = rng.uniform(0.8, 6.5, n)
    moisture = rng.uniform(8, 65, n)
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
    cls = np.where(health > 10, 2, np.where(health > -10, 1, 0))
    return pd.DataFrame({
        "pH": ph,
        "nitrogen": n_val,
        "phosphorus": p_val,
        "potassium": k_val,
        "organic_matter": om,
        "moisture": moisture,
        "label": cls,
    })

def generate_pest_records(n: int = 350) -> pd.DataFrame:
    rng = np.random.default_rng(3)
    crops = ["wheat", "rice", "maize", "soybean", "cotton"]
    symptoms = ["spots", "holes", "wilting", "mildew", "yellowing", "healthy"]
    env = ["humid", "dry", "rain", "hot", "cool"]
    crop_type = rng.choice(crops, n)
    symptom = rng.choice(symptoms, n)
    environmental_conditions = rng.choice(env, n)
    label = np.where(symptom == "healthy", "healthy", rng.choice(["pest", "disease"], n))
    return pd.DataFrame({
        "crop_type": crop_type,
        "symptoms": symptom,
        "environmental_conditions": environmental_conditions,
        "label": label,
    })

def generate_market_prices(days: int = 730) -> pd.DataFrame:
    rng = np.random.default_rng(4)
    t = np.arange(days)
    seasonal = 10 * np.sin(2 * np.pi * t / 365.0)
    trend = 0.02 * t
    noise = rng.normal(0, 1.8, days)
    price = 50 + trend + seasonal + noise
    idx = pd.date_range(end=pd.Timestamp.today(), periods=days, freq='D')
    crop = np.random.choice(["wheat", "rice", "maize"], size=days)
    location = np.random.choice(["North", "South", "East", "West"], size=days)
    return pd.DataFrame({"date": idx, "crop_type": crop, "location": location, "price": price})

def ensure_sample_data():
    files = {
        "crop_yield.csv": generate_crop_yield,
        "soil_health.csv": generate_soil_health,
        "pest_records.csv": generate_pest_records,
        "market_prices.csv": generate_market_prices,
    }
    for fname, fn in files.items():
        path = os.path.join(DATA_DIR, fname)
        if not os.path.exists(path):
            df = fn()
            df.to_csv(path, index=False)

