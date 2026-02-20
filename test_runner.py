"""
Main Test Runner - Execute from project root
Usage: python test_runner.py
"""
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    """Run backend tests from project root"""
    
    # Get paths
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    tests_path = backend_path / "tests"
    
    print("\n" + "=" * 80)
    print("🧪 BLOOD GROUP CLASSIFICATION - BACKEND TEST SUITE")
    print("=" * 80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project root: {project_root}")
    print(f"Backend: {backend_path}")
    print("=" * 80 + "\n")
    
    # Check if venv exists, if not create it
    venv_path = backend_path / "venv"
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Virtual environment created\n")
    
    # Determine pip executable
    if sys.platform == "win32":
        pip_exe = venv_path / "Scripts" / "pip.exe"
        pytest_exe = venv_path / "Scripts" / "pytest.exe"
    else:
        pip_exe = venv_path / "bin" / "pip"
        pytest_exe = venv_path / "bin" / "pytest"
    
    # Install dependencies
    print("📥 Installing dependencies...")
    requirements = [
        str(backend_path / "requirements.txt"),
        str(backend_path / "requirements-dev.txt"),
    ]
    
    for req_file in requirements:
        if Path(req_file).exists():
            print(f"   Installing from {Path(req_file).name}...")
            subprocess.run([str(pip_exe), "install", "-q", "-r", req_file], check=True)
    
    print("✅ Dependencies installed\n")
    
    # Run tests
    print("▶️  Running tests...\n")
    
    cmd = [
        str(pytest_exe),
        str(tests_path),
        "-v",
        "--tb=short",
        "--cov=agents",
        "--cov=models",
        "--cov=routes",
        "--cov=utils",
        "--cov-report=html",
        "--cov-report=term-missing",
    ]
    
    result = subprocess.run(cmd, cwd=str(backend_path))
    
    print("\n" + "=" * 80)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED!")
        print(f"📊 Coverage report: {backend_path}/htmlcov/index.html")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Run with -v flag for more details")
    print("=" * 80)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return result.returncode

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
