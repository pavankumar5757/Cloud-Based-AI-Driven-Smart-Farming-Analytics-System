from typing import Tuple, Dict, Any
import os
import pandas as pd
from config import Config

REQUIRED_CROP_FIELDS = [
    "soil_type",
    "temperature",
    "humidity",
    "rainfall",
    "fertilizer_amount",
    "irrigation_frequency",
]

REQUIRED_SOIL_FIELDS = [
    "pH",
    "nitrogen",
    "phosphorus",
    "potassium",
    "organic_matter",
    "moisture",
]

REQUIRED_MARKET_FIELDS = ["crop_type", "season", "location", "historical_data"]

def validate_crop_yield_input(data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    errors = {}
    for field in REQUIRED_CROP_FIELDS:
        if field not in data:
            errors[field] = "Missing"
    numeric_fields = [
        "temperature",
        "humidity",
        "rainfall",
        "fertilizer_amount",
        "irrigation_frequency",
    ]
    for nf in numeric_fields:
        try:
            float(data.get(nf, ""))
        except Exception:
            errors[nf] = "Must be numeric"
    return (len(errors) == 0, errors)

def validate_soil_input(data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    errors = {}
    for field in REQUIRED_SOIL_FIELDS:
        if field not in data:
            errors[field] = "Missing"
    numeric_fields = ["pH", "nitrogen", "phosphorus", "potassium", "organic_matter", "moisture"]
    for nf in numeric_fields:
        try:
            float(data.get(nf, ""))
        except Exception:
            errors[nf] = "Must be numeric"
    return (len(errors) == 0, errors)

def validate_market_price_input(data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
    errors = {}
    for field in REQUIRED_MARKET_FIELDS:
        if field not in data:
            errors[field] = "Missing"
    return (len(errors) == 0, errors)

def preprocess_data(df):
    return df.dropna().reset_index(drop=True)

# External dataset loaders ----------------------------------------------------
def _resolve_path(env_value: str, default_globs: list):
    if env_value and os.path.exists(env_value):
        return env_value
    for g in default_globs:
        candidate = os.path.join(Config.EXTERNAL_DATA_DIR, g)
        if os.path.exists(candidate):
            return candidate
    return None

def load_external_crop_yield() -> pd.DataFrame | None:
    path = _resolve_path(Config.CROP_YIELD_CSV, ["crop_yield.csv", "*yield*.csv"])
    if not path:
        return None
    df = pd.read_csv(path)
    # Heuristic column mapping
    colmap = {
        'soil_type': ['soil_type','soil','soiltype'],
        'temperature': ['temperature','temp','tavg','temp_c'],
        'humidity': ['humidity','rh'],
        'rainfall': ['rainfall','rain','precip','precipitation_mm'],
        'fertilizer_amount': ['fertilizer_amount','fertilizer','fertilizer_kg_ha','n_fert'],
        'irrigation_frequency': ['irrigation_frequency','irrigation','irrigations_per_week'],
        'yield': ['yield','yield_t_ha','production_t_ha']
    }
    norm = {}
    cols = {c.lower(): c for c in df.columns}
    for target, aliases in colmap.items():
        for a in aliases:
            if a in cols:
                norm[target] = df[cols[a]]
                break
    if len(norm) < 7:
        return None
    out = pd.DataFrame(norm)
    return preprocess_data(out)

def load_external_soil_health() -> pd.DataFrame | None:
    path = _resolve_path(Config.SOIL_HEALTH_CSV, ["soil_health.csv", "*soil*.csv"])
    if not path:
        return None
    df = pd.read_csv(path)
    colmap = {
        'pH': ['ph','pH'],
        'nitrogen': ['nitrogen','n'],
        'phosphorus': ['phosphorus','p'],
        'potassium': ['potassium','k'],
        'organic_matter': ['organic_matter','om','organicmatter'],
        'moisture': ['moisture','soil_moisture']
    }
    norm = {}
    cols = {c.lower(): c for c in df.columns}
    for target, aliases in colmap.items():
        for a in aliases:
            if a.lower() in cols:
                norm[target] = df[cols[a.lower()]]
                break
    # Optional label
    label_col = next((c for c in df.columns if c.lower() in ['label','class','status']), None)
    if label_col:
        norm['label'] = df[label_col]
    if len(norm) < 6:
        return None
    return preprocess_data(pd.DataFrame(norm))

def load_external_market_prices() -> pd.DataFrame | None:
    path = _resolve_path(Config.MARKET_PRICE_CSV, ["market_prices.csv", "*price*.csv"])
    if not path:
        return None
    df = pd.read_csv(path)
    # Expect date, price at least
    date_col = next((c for c in df.columns if c.lower() in ['date','day','timestamp']), None)
    price_col = next((c for c in df.columns if c.lower() in ['price','avg_price','close']), None)
    crop_col = next((c for c in df.columns if c.lower() in ['crop','crop_type']), None)
    loc_col = next((c for c in df.columns if c.lower() in ['location','market']), None)
    if not date_col or not price_col:
        return None
    out = pd.DataFrame({
        'date': pd.to_datetime(df[date_col]),
        'price': df[price_col].astype(float),
        'crop_type': df[crop_col] if crop_col else 'wheat',
        'location': df[loc_col] if loc_col else 'Unknown'
    })
    return preprocess_data(out.sort_values('date'))

