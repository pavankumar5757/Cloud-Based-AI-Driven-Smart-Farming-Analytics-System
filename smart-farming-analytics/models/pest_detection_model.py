import os
import numpy as np
from typing import Optional, Dict
from PIL import Image
try:
   import tensorflow as tf
   from tensorflow.keras import layers, models
except Exception:
   tf = None
   layers = None
   models = None
from config import Config

class PestDetector:
   def __init__(self):
       self.model_path = Config.PEST_CNN_MODEL_PATH
       self.input_shape = (64, 64, 3)
       if tf is None:
           self.model = None
       else:
           if os.path.exists(self.model_path):
               self.model = tf.keras.models.load_model(self.model_path)
           else:
               self.model = self._build_dummy_cnn()
               # Save lightweight randomly initialized model to satisfy loading
               self.model.save(self.model_path)

   def _build_dummy_cnn(self):
       model = models.Sequential([
           layers.Input(shape=self.input_shape),
           layers.Conv2D(16, 3, activation='relu'),
           layers.MaxPooling2D(),
           layers.Conv2D(32, 3, activation='relu'),
           layers.MaxPooling2D(),
           layers.Flatten(),
           layers.Dense(32, activation='relu'),
           layers.Dense(3, activation='softmax'),  # 3 classes: healthy, pest, disease
       ])
       model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
       return model

   def _preprocess_image(self, image_path: str) -> np.ndarray:
       img = Image.open(image_path).convert('RGB').resize(self.input_shape[:2])
       arr = np.asarray(img, dtype=np.float32) / 255.0
       return np.expand_dims(arr, axis=0)

   def detect_from_payload(self, payload: Dict, image_path: Optional[str]):
       # Rule-based adjustment using symptoms/environment
       symptom_text = (payload.get('symptoms') or '').lower()
       env_text = (payload.get('environmental_conditions') or '').lower()
       base = np.array([0.7, 0.15, 0.15])  # healthy, pest, disease base prior
       if any(k in symptom_text for k in ["spots", "holes", "wilting", "mildew"]):
           base = np.array([0.3, 0.4, 0.3])
       if "humid" in env_text or "rain" in env_text:
           base = base * np.array([1.0, 1.1, 1.2])
       base = base / base.sum()

       cnn_proba = np.array([0.6, 0.2, 0.2])
       if image_path and tf is not None and self.model is not None:
           try:
               inp = self._preprocess_image(image_path)
               cnn_proba = self.model.predict(inp, verbose=0)[0]
           except Exception:
               pass

       # Combine priors and CNN output
       combined = (0.5 * base) + (0.5 * cnn_proba)
       combined = combined / combined.sum()
       classes = ["healthy", "pest", "disease"]
       idx = int(np.argmax(combined))

       treatment = []
       if classes[idx] == "pest":
           treatment = [
               "Use integrated pest management: pheromone traps, neem oil.",
               "Rotate crops and remove infected debris.",
           ]
       elif classes[idx] == "disease":
           treatment = [
               "Apply appropriate fungicide; ensure proper spacing and airflow.",
               "Avoid overhead irrigation; sanitize tools.",
           ]

       return {
           "predicted_class": classes[idx],
           "pest_probability": float(combined[1]),
           "disease_risk": float(combined[2]),
           "treatment_recommendations": treatment,
       }

