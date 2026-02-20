# Backend API Test Guide

## ✅ Backend is Running!

Your backend is successfully running on: **http://localhost:5000**

## 🧪 Test the API

### Option 1: Run the test script
```bash
cd backend
python test_api.py
```

### Option 2: Test in browser
Visit: **http://localhost:5000/**

Should see:
```json
{
  "service": "Blood Group Classification API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": { ... }
}
```

### Option 3: Test health endpoint
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Blood Group Classification API",
  "version": "1.0.0"
}
```

## 📤 Upload and Predict

### Step 1: Upload blood sample image
```bash
curl -X POST -F "file=@blood_sample.jpg" http://localhost:5000/api/upload
```

Response:
```json
{
  "file_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "550e8400-e29b-41d4-a716-446655440000.jpg",
  "upload_time": "2024-01-15T10:30:00.000000",
  "message": "File uploaded successfully"
}
```

### Step 2: Get prediction
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"file_id":"550e8400-e29b-41d4-a716-446655440000"}' \
  http://localhost:5000/api/predict
```

Response:
```json
{
  "prediction_id": "pred-123456",
  "blood_group": "O",
  "confidence": 0.92,
  "consensus_met": true,
  "agent_votes": { "O": 3 },
  "reasoning": "3/3 agents (100%) agree...",
  "created_at": "2024-01-15T10:35:00.000000"
}
```

### Step 3: Get results
```bash
curl http://localhost:5000/api/results/pred-123456
```

## ✨ API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info & status |
| `/api/health` | GET | System health |
| `/api/upload` | POST | Upload image |
| `/api/predict` | POST | Analyze image |
| `/api/results/<id>` | GET | Get prediction results |

## 🔍 View Logs

```bash
# Windows
type backend\logs\app.log

# Mac/Linux
tail -f backend/logs/app.log
```

## ✅ Backend Status

- ✅ Backend running on http://localhost:5000
- ✅ Database initialized
- ✅ All API endpoints available
- ✅ Multi-agent system ready

## 🚀 Next Steps

1. Set up React frontend
2. Test complete workflow
3. Deploy to production

See `RUN_BACKEND.md` for more details.
