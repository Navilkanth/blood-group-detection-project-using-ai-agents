import sys
import os
# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from model_loader import BloodGroupClassifier
from config import Config

print("-" * 50)
print("DIAGNOSTIC TEST")
print("-" * 50)

model_path = Config.MODEL_PATHS.get("agglutination_cnn")
label_path = Config.MODEL_PATHS.get("labels")

print(f"Model Path: {model_path}")
print(f"Label Path: {label_path}")

try:
    classifier = BloodGroupClassifier(model_path, label_path)
    print(f"\nFinal Blood Groups Used: {classifier.BLOOD_GROUPS}")
    if classifier.model:
        print("✅ SUCCESS: Model and Labels loaded perfectly!")
    else:
        print("❌ FAILURE: Model could not be loaded into memory.")
except Exception as e:
    print(f"❌ ERROR: {e}")
print("-" * 50)
