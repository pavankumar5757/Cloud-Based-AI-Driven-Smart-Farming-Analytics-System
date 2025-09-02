import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
csrf = CSRFProtect()

def create_app() -> Flask:
   app = Flask(__name__, static_folder="static", template_folder="templates")
   app.config.from_object(Config)

   db.init_app(app)
   csrf.init_app(app)

   # Register blueprints
   from routes.main import main_bp
   from routes.analytics import analytics_bp

   app.register_blueprint(main_bp)
   app.register_blueprint(analytics_bp, url_prefix="/api")
   # Exempt API from CSRF since requests are AJAX; UI forms are protected
   csrf.exempt(analytics_bp)

   # Error handlers
   @app.errorhandler(404)
   def not_found(error):
       return ("Page not found", 404)

   @app.errorhandler(413)
   def too_large(error):
       return ("File too large", 413)

   @app.errorhandler(Exception)
   def handle_exception(error):
       app.logger.exception("Unhandled exception: %s", error)
       return ("An unexpected error occurred", 500)

   # Logging
   if not app.debug:
       log_dir = os.path.join(os.path.dirname(__file__), "logs")
       os.makedirs(log_dir, exist_ok=True)
       file_handler = RotatingFileHandler(
           os.path.join(log_dir, "app.log"), maxBytes=1_000_000, backupCount=3
       )
       file_handler.setLevel(logging.INFO)
       formatter = logging.Formatter(
           "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
       )
       file_handler.setFormatter(formatter)
       app.logger.addHandler(file_handler)
       app.logger.setLevel(logging.INFO)
       app.logger.info("Smart Farming Analytics startup")

   return app

# Database models (ORM) -----------------------------------------------------
# Keeping ORM models here for simplicity. In a larger app, place in dedicated module.
class Crop(db.Model):
   __tablename__ = "crops"
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64), nullable=False)
   season = db.Column(db.String(32))
   location = db.Column(db.String(128))

class SoilData(db.Model):
   __tablename__ = "soil_data"
   id = db.Column(db.Integer, primary_key=True)
   ph = db.Column(db.Float, nullable=False)
   nitrogen = db.Column(db.Float, nullable=False)
   phosphorus = db.Column(db.Float, nullable=False)
   potassium = db.Column(db.Float, nullable=False)
   organic_matter = db.Column(db.Float, nullable=False)
   moisture = db.Column(db.Float, nullable=False)

class PestRecord(db.Model):
   __tablename__ = "pest_records"
   id = db.Column(db.Integer, primary_key=True)
   crop_type = db.Column(db.String(64), nullable=False)
   symptoms = db.Column(db.String(256))
   environmental_conditions = db.Column(db.String(256))
   image_path = db.Column(db.String(256))
   label = db.Column(db.String(64))

class MarketPrice(db.Model):
   __tablename__ = "market_prices"
   id = db.Column(db.Integer, primary_key=True)
   crop_type = db.Column(db.String(64), nullable=False)
   date = db.Column(db.Date, nullable=False)
   price = db.Column(db.Float, nullable=False)
   location = db.Column(db.String(128))

class Prediction(db.Model):
   __tablename__ = "predictions"
   id = db.Column(db.Integer, primary_key=True)
   type = db.Column(db.String(64), nullable=False)
   input_json = db.Column(db.Text, nullable=False)
   output_json = db.Column(db.Text, nullable=False)

