import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(__file__), 'smart_farming.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

    # ML model artifact paths
    MODEL_DIR = os.path.join(os.path.dirname(__file__), "models_store")
    CROP_YIELD_MODEL_PATH = os.path.join(MODEL_DIR, "crop_yield_rf.pkl")
    SOIL_HEALTH_MODEL_PATH = os.path.join(MODEL_DIR, "soil_health_clf.pkl")
    PEST_CNN_MODEL_PATH = os.path.join(MODEL_DIR, "pest_cnn.h5")
    MARKET_ARIMA_PATH = os.path.join(MODEL_DIR, "market_arima.pkl")

    # External datasets (Kaggle-style) configuration
    EXTERNAL_DATA_DIR = os.environ.get(
        "EXTERNAL_DATA_DIR", os.path.join(os.path.dirname(__file__), "data", "external")
    )
    # Optional explicit filenames (if provided, they will be used)
    CROP_YIELD_CSV = os.environ.get("CROP_YIELD_CSV", "")
    SOIL_HEALTH_CSV = os.environ.get("SOIL_HEALTH_CSV", "")
    PEST_DATA_CSV = os.environ.get("PEST_DATA_CSV", "")
    MARKET_PRICE_CSV = os.environ.get("MARKET_PRICE_CSV", "")

    # Plotly config
    PLOTLY_RENDERER = os.environ.get("PLOTLY_RENDERER", "browser")

    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

os.makedirs(Config.MODEL_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.EXTERNAL_DATA_DIR, exist_ok=True)
