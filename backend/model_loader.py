import numpy as np
import os
import logging
import json

logger = logging.getLogger(__name__)

# Try to import TensorFlow safely
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

class BloodGroupClassifier:
    def __init__(self, model_path=None, label_path=None):
        self.model_path = model_path
        self.label_path = label_path

        from backend.config import Config
        if not self.model_path or not os.path.exists(self.model_path):
            self.model_path = Config.get_model_path()
            
        if not self.label_path or not os.path.exists(self.label_path):
            self.label_path = Config.get_label_path()

        self.model = None
        self.BLOOD_GROUPS = self._load_labels()
        
        if TENSORFLOW_AVAILABLE:
            self._load_model()
        else:
            logger.error("Cannot load model: TensorFlow is not installed.")

    def _load_labels(self):
        default_labels = ['A', 'AB', 'B', 'O']
        if self.label_path and os.path.exists(self.label_path):
            try:
                with open(self.label_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading labels: {e}")
        return default_labels

    def _load_model(self):
        if not self.model_path or not os.path.exists(self.model_path):
            logger.error(f"Model file not found: {self.model_path}")
            return

        print(f"🔄 Applying Surgical Patch to Keras 3 Model: {self.model_path}...")
        
        try:
            # --- THE PERFECT FIX FOR BATCH_NORMALIZATION ---
            # We create a patched version of BatchNormalization that automatically
            # ignores the extra training tensor that causes the "2 input tensors" error.
            from tensorflow.keras.layers import BatchNormalization, InputLayer

            class PatchedBatchNormalization(BatchNormalization):
                def call(self, inputs, training=None, **kwargs):
                    # If we receive multiple tensors, only take the first one (the actual image data)
                    if isinstance(inputs, (list, tuple)) and len(inputs) > 1:
                        return super().call(inputs[0], training=training, **kwargs)
                    return super().call(inputs, training=training, **kwargs)

            class FlexibleInputLayer(InputLayer):
                def __init__(self, *args, **kwargs):
                    for key in ['batch_shape', 'sparse', 'ragged']:
                        kwargs.pop(key, None)
                    super().__init__(**kwargs)

            # Map both standard and patched names to our fixes
            custom_objects = {
                'BatchNormalization': PatchedBatchNormalization,
                'InputLayer': FlexibleInputLayer
            }

            # Attempt clean load with the patches
            self.model = tf.keras.models.load_model(
                self.model_path, 
                compile=False, 
                custom_objects=custom_objects,
                safe_mode=False
            )
            print(f"✅ SUCCESS: Model loaded and surgery successful.")

        except Exception as e:
            logger.error(f"❌ Critical Load Error: {e}")
            print(f"❌ Error: Model structure is still rejecting the load. Trying raw weight injection...")
            try:
                # Last resort: If the full load fails, we can usually still load via tf_keras
                import tf_keras
                self.model = tf_keras.models.load_model(self.model_path, compile=False)
                print(f"✅ SUCCESS: Loaded via tf-keras Fallback.")
            except Exception as e2:
                self.model = None

    def predict(self, image_path):
        if not TENSORFLOW_AVAILABLE or self.model is None:
            return {"error": "Model not available", "fallback": True}

        try:
            from tensorflow.keras.preprocessing import image
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
            
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            # Predict
            predictions = self.model.predict(img_array, verbose=0)
            
            # Extract scores and find winning index
            scores = predictions[0]
            predicted_idx = np.argmax(scores)
            confidence = float(scores[predicted_idx])
            
            return {
                'success': True,
                'blood_group': self.BLOOD_GROUPS[predicted_idx],
                'confidence': confidence,
                'probabilities': {
                    self.BLOOD_GROUPS[i]: float(scores[i])
                    for i in range(len(self.BLOOD_GROUPS))
                }
            }
        except Exception as e:
            logger.error(f"Prediction logic error: {e}")
            return {"error": str(e), "fallback": True}
