"""
Test runner with comprehensive reporting
"""
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def run_tests():
    """Execute all tests with detailed reporting"""
    
    print("=" * 80)
    print("BLOOD GROUP CLASSIFICATION - BACKEND TEST SUITE")
    print("=" * 80)
    print(f"\nTest execution started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Run pytest with coverage and reporting
    test_dir = Path(__file__).parent
    
    cmd = [
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
        "--cov-report=term",
        "-x",  # Stop on first failure
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=str(test_dir.parent))
    
    print("\n" + "=" * 80)
    if result.returncode == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ TESTS FAILED")
    print("=" * 80)
    
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
