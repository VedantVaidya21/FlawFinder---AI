#!/usr/bin/env python3
"""
Simple test runner for FlawFinder backend.
Runs tests without pytest-cov dependency.
"""

import sys
import os
import subprocess

def run_tests():
    """Run the test suite."""
    # Add backend directory to Python path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    print("Running FlawFinder Backend Tests")
    print("=" * 40)

    try:
        # Run pytest without coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "--tb=short"
        ], cwd=backend_dir, capture_output=True, text=True)

        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        print(f"\nTest Result: {'PASSED' if result.returncode == 0 else 'FAILED'}")
        return result.returncode == 0

    except Exception as e:
        print(f"Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
