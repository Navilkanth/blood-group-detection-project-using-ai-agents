# Quick Start Guide

## 30-Second Setup

### Windows, Mac, or Linux:
```bash
python start_backend.py
```

Done! 🎉

Backend is running at: **http://localhost:5000**

## Test It

### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

### 2. Upload Image
```bash
curl -X POST -F "file=@blood_sample.jpg" http://localhost:5000/api/upload
```

### 3. Get Prediction
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"file_id":"<file_id_from_step_2>"}' \
  http://localhost:5000/api/predict
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | System status |
| `/api/upload` | POST | Upload blood image |
| `/api/predict` | POST | Analyze and predict |
| `/api/results/<id>` | GET | Get results |

## Troubleshooting

**"ModuleNotFoundError"?**
```bash
cd backend
pip install -r requirements.txt
```

**"No model file found"?**
Place your CNN model at:
```
backend/models/agglutination_model.pth
```

**"Port 5000 already in use"?**
Edit `app.py` line 48:
```python
app.run(host="0.0.0.0", port=5001, debug=app.debug)
```

## Full Documentation

See `RUN_BACKEND.md` for detailed guide
