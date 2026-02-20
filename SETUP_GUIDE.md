# 🩸 Blood Group Classification - Complete Setup Guide

## ⚠️ Python Version Issue Detected

**Your Python Version:** 3.14  
**Required Version:** 3.8 - 3.11 (for original requirements)

## 🎯 Two Solutions Available

---

## ✅ **SOLUTION 1: Use Python 3.11 (RECOMMENDED)**

### Step 1: Install Python 3.11
Download from: https://www.python.org/downloads/release/python-3110/

### Step 2: Create Virtual Environment with Python 3.11
```bash
# Navigate to project directory
cd "C:\Users\navin\Downloads\BLOOD GROUP CLASSIFIACTION"

# Create venv with Python 3.11
py -3.11 -m venv backend\venv

# Activate virtual environment
backend\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Step 3: Run the Backend
```bash
# Make sure you're in backend directory and venv is activated
python app.py
```

---

## ✅ **SOLUTION 2: Use Updated Packages for Python 3.14**

### Step 1: Clean Previous Installation
```bash
cd "C:\Users\navin\Downloads\BLOOD GROUP CLASSIFIACTION\backend"

# Remove existing venv if it exists
rmdir /s /q venv

# Create fresh virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### Step 2: Upgrade pip and Install Build Tools
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install build tools
pip install --upgrade setuptools wheel

# Install Microsoft C++ Build Tools (if needed for some packages)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### Step 3: Install Updated Dependencies
```bash
# Use the updated requirements file
pip install -r requirements-updated.txt
```

### Step 4: Verify Installation
```bash
# Check installed packages
pip list

# Test imports
python -c "import flask; import numpy; import PIL; print('✅ Core packages OK')"
python -c "import torch; import tensorflow; print('✅ ML packages OK')"
```

### Step 5: Run the Backend
```bash
python app.py
```

---

## 🚀 **Quick Start Commands (Copy & Paste)**

### For Python 3.11 (Recommended):
```bash
cd "C:\Users\navin\Downloads\BLOOD GROUP CLASSIFIACTION"
py -3.11 -m venv backend\venv
backend\venv\Scripts\activate
python -m pip install --upgrade pip
cd backend
pip install -r requirements.txt
python app.py
```

### For Python 3.14 (Updated Packages):
```bash
cd "C:\Users\navin\Downloads\BLOOD GROUP CLASSIFIACTION\backend"
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements-updated.txt
python app.py
```

---

## 📦 **Package Comparison**

| Package | Original (Py 3.8-3.11) | Updated (Py 3.14) |
|---------|------------------------|-------------------|
| TensorFlow | 2.13.0 | 2.18.0 |
| PyTorch | 2.0.1 | 2.5.1 |
| Pillow | 10.0.0 | 11.0.0 |
| NumPy | 1.24.3 | 2.1.3 |
| Flask | 2.3.3 | 3.0.3 |

---

## 🔧 **Troubleshooting**

### Issue: "Microsoft Visual C++ 14.0 is required"
**Solution:**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Restart terminal and try again

### Issue: "No module named 'torch'"
**Solution:**
```bash
# Install PyTorch separately
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Issue: "TensorFlow not found"
**Solution:**
```bash
# Install TensorFlow separately
pip install tensorflow==2.18.0
```

### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace <PID> with actual process ID)
taskkill /PID <PID> /F
```

### Issue: "sqlite3 module error"
**Solution:**
```bash
# sqlite3 is built-in, remove from requirements.txt
# Edit backend/requirements.txt and remove line 13: "sqlite3"
```

---

## ✅ **Verification Checklist**

After installation, verify:

- [ ] Virtual environment activated
- [ ] All packages installed without errors
- [ ] Python imports work: `python -c "import flask, torch, tensorflow"`
- [ ] Backend starts: `python app.py`
- [ ] API responds: Visit http://localhost:5000/api/health

---

## 🎯 **Expected Output When Running**

```
================================================================================
🩸 BLOOD GROUP CLASSIFICATION - BACKEND SERVER
================================================================================
Start time: 2026-02-17 11:35:00
================================================================================

✅ Python 3.11.0 detected
✅ CNN model found: agglutination_model.pth
✅ .env file already exists
✅ Database ready

================================================================================
🚀 Starting Backend Server
================================================================================

📍 API Base URL: http://localhost:5000
📍 Health Check: http://localhost:5000/api/health

💡 Tips:
   - Upload image: POST http://localhost:5000/api/upload
   - Get prediction: POST http://localhost:5000/api/predict
   - Press Ctrl+C to stop server

================================================================================

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

## 📞 **Need Help?**

If you still encounter issues:
1. Check Python version: `python --version`
2. Check pip version: `pip --version`
3. List installed packages: `pip list`
4. Check backend logs: `type backend\logs\app.log`

---

**Choose Solution 1 (Python 3.11) for maximum compatibility!** ✨
