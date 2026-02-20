import subprocess
import sys

def run_command(cmd):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Execution failed: {e}")
        return 1

print("--- REPAIRING TENSORFLOW INSTALLATION ---")
# Uninstall potentially conflicting versions
run_command("pip uninstall -y tensorflow tensorflow-intel numpy")
# Install with strict versions
print("--- INSTALLING TENSORFLOW AND COMPATIBLE NUMPY ---")
run_command("pip install tensorflow==2.18.0 numpy==2.0.2 --no-cache-dir")

print("--- VERIFYING ---")
try:
    import tensorflow as tf
    print(f"✅ Success! TensorFlow version: {tf.__version__}")
except Exception as e:
    print(f"❌ Still failing: {e}")
