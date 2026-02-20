"""
One-Click Backend Startup Script
Handles venv setup, dependencies, and server launch
"""
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def print_banner():
    """Print startup banner"""
    print("\n" + "=" * 80)
    print("🩸 BLOOD GROUP CLASSIFICATION - BACKEND SERVER")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

def check_python_version():
    """Verify Python 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def setup_venv():
    """Create and activate virtual environment"""
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    venv_path = backend_path / "venv"
    
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Virtual environment created")
    else:
        print("✅ Virtual environment already exists")
    
    return venv_path

def get_pip_executable(venv_path):
    """Get pip executable path"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def install_dependencies(pip_exe, backend_path):
    """Install required dependencies"""
    print("\n📥 Installing dependencies...")
    
    requirements_file = backend_path / "requirements.txt"
    if requirements_file.exists():
        print(f"   From: {requirements_file.name}")
        result = subprocess.run(
            [str(pip_exe), "install", "-r", str(requirements_file)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"⚠️  Installation warning: {result.stderr}")
        else:
            print("✅ Dependencies installed")
    else:
        print(f"⚠️  requirements.txt not found at {requirements_file}")
        sys.exit(1)

def check_model_file(backend_path):
    """Check if CNN model exists"""
    model_path = backend_path / "models" / "agglutination_model.pth"
    
    if not model_path.exists():
        print("\n⚠️  CNN Model Not Found!")
        print(f"   Expected location: {model_path}")
        print("   Please place your trained model file there")
        response = input("\n   Continue without model? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
        print("   ℹ️  Backend will use heuristic fallback for predictions")
    else:
        print(f"✅ CNN model found: {model_path.name}")

def check_database(backend_path):
    """Initialize database if needed"""
    print("\n🗄️  Initializing database...")
    
    sys.path.insert(0, str(backend_path))
    try:
        from utils.database import init_db
        init_db()
        print("✅ Database ready")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

def create_env_file(backend_path):
    """Create .env file if it doesn't exist"""
    env_file = backend_path / ".env"
    
    if not env_file.exists():
        print("\n📝 Creating .env configuration file...")
        env_content = """FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///./blood_group.db
AGGLUTINATION_MODEL_PATH=./models/agglutination_model.pth
USE_GPU=true
CNN_CONFIDENCE_THRESHOLD=0.5
CONFIDENCE_THRESHOLD=0.7
CONSENSUS_THRESHOLD=0.6
HIPAA_LOGGING=true
ENCRYPT_IMAGES=true
LOG_LEVEL=DEBUG
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created: {env_file}")
    else:
        print("✅ .env file already exists")

def start_server(backend_path):
    """Start Flask development server"""
    print("\n" + "=" * 80)
    print("🚀 Starting Backend Server")
    print("=" * 80)
    print("\n📍 API Base URL: http://localhost:5000")
    print("📍 Health Check: http://localhost:5000/api/health")
    print("\n💡 Tips:")
    print("   - Upload image: POST http://localhost:5000/api/upload")
    print("   - Get prediction: POST http://localhost:5000/api/predict")
    print("   - Press Ctrl+C to stop server")
    print("\n" + "=" * 80 + "\n")
    
    app_file = backend_path / "app.py"
    
    # Change to backend directory and run app
    os.chdir(str(backend_path))
    
    # Add backend to Python path
    env = os.environ.copy()
    env['PYTHONPATH'] = str(backend_path)
    
    subprocess.run([sys.executable, str(app_file)], env=env)

def main():
    """Main startup orchestration"""
    try:
        print_banner()
        
        project_root = Path(__file__).parent
        backend_path = project_root / "backend"
        
        # Checks
        check_python_version()
        check_model_file(backend_path)
        create_env_file(backend_path)
        
        # Setup
        venv_path = setup_venv()
        pip_exe = get_pip_executable(venv_path)
        install_dependencies(pip_exe, backend_path)
        
        # Initialize
        check_database(backend_path)
        
        # Start
        start_server(backend_path)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
