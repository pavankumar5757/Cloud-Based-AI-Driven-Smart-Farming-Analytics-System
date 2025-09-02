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

    # Plotly config
    PLOTLY_RENDERER = os.environ.get("PLOTLY_RENDERER", "browser")

    # Security
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

os.makedirs(Config.MODEL_DIR, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
