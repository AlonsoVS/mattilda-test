#!/usr/bin/env python3
"""
Test runner script for mattilda-test project.
This script provides convenient commands to run different test suites.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n🔬 {description}")
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def run_domain_tests(verbose=False):
    """Run domain model unit tests"""
    cmd = ["python", "-m", "pytest", "tests/unit/domain/"]
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd, "Running Domain Model Unit Tests")


def run_all_tests(verbose=False):
    """Run all available tests"""
    cmd = ["python", "-m", "pytest", "tests/"]
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd, "Running All Tests")


def run_coverage_tests():
    """Run tests with coverage report"""
    cmd = [
        "python", "-m", "pytest", 
        "tests/unit/domain/",
        "--cov=app.domain",
        "--cov-report=term-missing",
        "--cov-report=html:htmlcov",
        "-v"
    ]
    
    success = run_command(cmd, "Running Tests with Coverage")
    if success:
        print("\n📊 Coverage report generated in htmlcov/ directory")
    return success


def run_specific_test(test_path, verbose=False):
    """Run a specific test file or test method"""
    cmd = ["python", "-m", "pytest", test_path]
    if verbose:
        cmd.append("-v")
    
    return run_command(cmd, f"Running Specific Test: {test_path}")


def main():
    parser = argparse.ArgumentParser(description="Test runner for mattilda-test project")
    parser.add_argument(
        "action", 
        choices=["domain", "all", "coverage", "specific"],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--test-path", 
        help="Path to specific test (for 'specific' action)"
    )
    
    args = parser.parse_args()
    
    # Change to project directory
    project_root = Path(__file__).parent
    import os
    os.chdir(project_root)
    
    print("🧪 Mattilda Test Runner")
    print(f"Project root: {project_root}")
    
    success = False
    
    if args.action == "domain":
        success = run_domain_tests(args.verbose)
    elif args.action == "all":
        success = run_all_tests(args.verbose)
    elif args.action == "coverage":
        success = run_coverage_tests()
    elif args.action == "specific":
        if not args.test_path:
            print("❌ --test-path is required for 'specific' action")
            sys.exit(1)
        success = run_specific_test(args.test_path, args.verbose)
    
    if success:
        print("\n✅ Tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
