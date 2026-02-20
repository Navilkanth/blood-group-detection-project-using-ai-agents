"""
Test runner with comprehensive reporting
"""
import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

def setup_environment():
    """Setup Python path and environment"""
    backend_path = Path(__file__).parent.parent
    sys.path.insert(0, str(backend_path))
    os.chdir(str(backend_path))

def run_tests():
    """Execute all tests with detailed reporting"""
    
    print("=" * 80)
    print("BLOOD GROUP CLASSIFICATION - BACKEND TEST SUITE")
    print("=" * 80)
    print(f"\nTest execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Setup environment
    setup_environment()
    
    # Run pytest with coverage and reporting
    test_dir = Path(__file__).parent
    
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(test_dir),
        "-v",
        "--tb=short",
        "--color=yes",
        "--cov=agents",
        "--cov=models",
        "--cov=routes",
        "--cov=utils",
        "--cov-report=html",
        "--cov-report=term-missing",
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=str(test_dir.parent))
    
    print("\n" + "=" * 80)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 80)
    print(f"\nTest execution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
