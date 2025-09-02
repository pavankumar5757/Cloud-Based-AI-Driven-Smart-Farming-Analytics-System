from typing import Tuple, Dict, Any

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

