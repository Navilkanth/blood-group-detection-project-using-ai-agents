import os
from backend.config import Config

p = Config.MODEL_PATHS.get("agglutination_cnn")
try:
    with open('model_check.txt', 'w') as log:
        log.write(f"Path: {p}\n")
        log.write(f"Exists: {os.path.exists(p)}\n")
        if os.path.exists(p):
            size = os.path.getsize(p)
            log.write(f"Size: {size}\n")
            with open(p, 'rb') as f:
                header = f.read(100)
                log.write(f"Header: {header}\n")
except Exception as e:
    with open('model_check.txt', 'a') as log:
        log.write(f"Error: {str(e)}\n")
