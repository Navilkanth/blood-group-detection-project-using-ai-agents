# How to Run the Blood Group Classification Backend

## Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- Your trained CNN model file (`.pth` file)

## Quick Start (Recommended)

### Windows
```bash
python start_backend.py
```

### Mac/Linux
```bash
python start_backend.py
```

The backend will be available at: **http://localhost:5000**

## Step-by-Step Manual Setup

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the `backend` directory:
```
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///./blood_group.db
AGGLUTINATION_MODEL_PATH=./models/agglutination_model.pth
USE_GPU=true
CONFIDENCE_THRESHOLD=0.7
HIPAA_LOGGING=true
ENCRYPT_IMAGES=true
LOG_LEVEL=DEBUG
```

### Step 5: Place Your CNN Model
Copy your trained CNN model to:
```
backend/models/agglutination_model.pth
```

### Step 6: Initialize Database
```bash
python -c "from utils.database import init_db; init_db(); print('✅ Database initialized')"
```

### Step 7: Run the Backend
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

## Backend File Structure

```
backend/
├── agents/              # Multi-agent system
│   ├── base_agent.py
│   ├── image_validation_agent.py
│   ├── agglutination_detection_agent.py
│   ├── medical_rules_agent.py
│   ├── confidence_assessment_agent.py
│   ├── safety_ethics_agent.py
│   └── consensus_engine.py
├── models/              # ML models
│   ├── model_manager.py
│   ├── model_config.py
│   └── agglutination_model.pth  # Your trained model
├── routes/              # API endpoints
│   ├── health_routes.py
│   ├── upload_routes.py
│   └── prediction_routes.py
├── utils/               # Utilities
│   ├── database.py
│   ├── image_encryption.py
│   └── logger.py
├── tests/               # Test suite
├── app.py               # Flask application
├── config.py            # Configuration
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

## API Endpoints

Once running, access these endpoints:

### 1. Health Check
```bash
GET http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Blood Group Classification API",
  "version": "1.0.0"
}
```

### 2. Upload Image
```bash
POST http://localhost:5000/api/upload
Content-Type: multipart/form-data

Body: file=<blood_sample.jpg>
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

### 3. Predict Blood Group
```bash
POST http://localhost:5000/api/predict
Content-Type: application/json

Body: {"file_id": "550e8400-e29b-41d4-a716-446655440000"}
```

Response:
```json
{
  "prediction_id": "pred-123456",
  "blood_group": "O",
  "confidence": 0.92,
  "consensus_met": true,
  "agent_votes": {
    "O": 3,
    "A": 0
  },
  "reasoning": "3/3 agents (100%) agree on blood type: O...",
  "created_at": "2024-01-15T10:35:00.000000"
}
```

### 4. Get Results
```bash
GET http://localhost:5000/api/results/<prediction_id>
```

Response:
```json
{
  "prediction_id": "pred-123456",
  "blood_group": "O",
  "confidence": 0.92,
  "consensus_met": true,
  "agent_votes": {"O": 3},
  "reasoning": "...",
  "created_at": "2024-01-15T10:35:00.000000"
}
```

## Testing the Backend

### Run All Tests
```bash
python test_runner.py
```

### Run Specific Tests
```bash
cd backend
pytest tests/test_agents.py -v
pytest tests/test_api_endpoints.py -v
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'agents'"
**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "CUDA out of memory" / GPU errors
**Solution:** Disable GPU in `.env`:
```
USE_GPU=false
```

### Issue: "No module named 'torch'"
**Solution:**
```bash
pip install torch torchvision
```

### Issue: Model file not found
**Solution:** Verify model location:
```bash
# Windows
dir backend\models\agglutination_model.pth

# Mac/Linux
ls -la backend/models/agglutination_model.pth
```

### Issue: "Address already in use" on port 5000
**Solution:** Change port in `app.py` or kill process on 5000:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue: Database locked error
**Solution:** Delete database and reinitialize:
```bash
cd backend
del blood_group.db
python -c "from utils.database import init_db; init_db()"
```

## Configuration Options

### Environment Variables (.env)

| Variable | Value | Purpose |
|----------|-------|---------|
| `FLASK_ENV` | `development` or `production` | App mode |
| `USE_GPU` | `true` or `false` | Enable GPU acceleration |
| `CONFIDENCE_THRESHOLD` | `0.7` | Min confidence for prediction |
| `HIPAA_LOGGING` | `true` or `false` | Enable audit logging |
| `ENCRYPT_IMAGES` | `true` or `false` | Encrypt stored images |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING` | Logging verbosity |

## Performance Tips

1. **GPU Acceleration**: Ensure CUDA is installed for GPU support
2. **Model Caching**: Model is cached after first load
3. **Batch Processing**: Can handle multiple simultaneous uploads
4. **Database**: SQLite suitable for dev; use PostgreSQL for production

## Production Deployment

For production, use a WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Or with Waitress:
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

## Logs

Backend logs are saved in:
```
backend/logs/app.log
backend/logs/agents.py
backend/logs/models.py
```

View logs:
```bash
# Windows
type backend\logs\app.log

# Mac/Linux
tail -f backend/logs/app.log
```

## Next Steps

1. ✅ Backend running
2. 🔜 Set up React frontend
3. 🔜 Test complete workflow
4. 🔜 Deploy to production

For frontend setup, see `RUN_FRONTEND.md`
