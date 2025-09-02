import json
import os
from flask import Blueprint, request, jsonify, current_app, send_file
from werkzeug.utils import secure_filename
from models.crop_yield_model import CropYieldPredictor
from models.soil_health_model import SoilHealthAnalyzer
from models.pest_detection_model import PestDetector
from models.market_price_model import MarketPricePredictor
from utils.ml_utils import model_cache
from utils.data_preprocessing import validate_crop_yield_input, validate_soil_input, validate_market_price_input

analytics_bp = Blueprint("analytics", __name__)

def get_or_init_model(key: str, factory):
   if key not in model_cache:
       model_cache[key] = factory()
   return model_cache[key]

@analytics_bp.route("/predict/crop-yield", methods=["POST"])
def predict_crop_yield():
   try:
       data = request.get_json(force=True)
       valid, errors = validate_crop_yield_input(data)
       if not valid:
           return jsonify({"error": "Invalid input", "details": errors}), 400
       model = get_or_init_model("crop_yield", CropYieldPredictor)
       result = model.predict_from_json(data)
       return jsonify(result)
   except Exception as exc:
       current_app.logger.exception("Crop yield prediction failed: %s", exc)
       return jsonify({"error": "Prediction failed"}), 500

@analytics_bp.route("/analyze/soil-health", methods=["POST"])
def analyze_soil_health():
   try:
       data = request.get_json(force=True)
       valid, errors = validate_soil_input(data)
       if not valid:
           return jsonify({"error": "Invalid input", "details": errors}), 400
       model = get_or_init_model("soil_health", SoilHealthAnalyzer)
       result = model.analyze_from_json(data)
       return jsonify(result)
   except Exception as exc:
       current_app.logger.exception("Soil health analysis failed: %s", exc)
       return jsonify({"error": "Analysis failed"}), 500

@analytics_bp.route("/detect/pest", methods=["POST"])
def detect_pest():
   try:
       # Handle optional file
       image_path = None
       if "image" in request.files and request.files["image"].filename:
           f = request.files["image"]
           filename = secure_filename(f.filename)
           ext = filename.rsplit(".", 1)[-1].lower()
           if ext not in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
               return jsonify({"error": "Unsupported file type"}), 400
           upload_dir = current_app.config["UPLOAD_FOLDER"]
           image_path = os.path.join(upload_dir, filename)
           f.save(image_path)

       payload = request.form.to_dict() if request.form else request.get_json(silent=True) or {}
       model = get_or_init_model("pest_detector", PestDetector)
       result = model.detect_from_payload(payload, image_path)
       return jsonify(result)
   except Exception as exc:
       current_app.logger.exception("Pest detection failed: %s", exc)
       return jsonify({"error": "Detection failed"}), 500

@analytics_bp.route("/forecast/market-price", methods=["POST"])
def forecast_market_price():
   try:
       data = request.get_json(force=True)
       valid, errors = validate_market_price_input(data)
       if not valid:
           return jsonify({"error": "Invalid input", "details": errors}), 400
       model = get_or_init_model("market_price", MarketPricePredictor)
       result = model.forecast_from_json(data)
       return jsonify(result)
   except Exception as exc:
       current_app.logger.exception("Market price forecast failed: %s", exc)
       return jsonify({"error": "Forecast failed"}), 500

@analytics_bp.route("/data/export/<dtype>", methods=["GET"])
def export_data(dtype: str):
   try:
       # Provide paths to generated CSVs
       base = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
       mapping = {
           "crop": os.path.join(base, "crop_yield.csv"),
           "soil": os.path.join(base, "soil_health.csv"),
           "pest": os.path.join(base, "pest_records.csv"),
           "price": os.path.join(base, "market_prices.csv"),
       }
       path = mapping.get(dtype)
       if not path or not os.path.exists(path):
           return jsonify({"error": "Data not found"}), 404
       return send_file(path, as_attachment=True)
   except Exception as exc:
       current_app.logger.exception("Data export failed: %s", exc)
       return jsonify({"error": "Export failed"}), 500
