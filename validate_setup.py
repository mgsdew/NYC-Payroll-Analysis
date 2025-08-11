#!/usr/bin/env python3
"""
NYC Payroll ETL - Setup Validation Script
Validates that all components are properly configured
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def check_docker_setup():
    """Check if Docker and Docker Compose are available"""
    print("🐳 Checking Docker setup...")
    try:
        # Check Docker
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
        else:
            print("❌ Docker not found")
            return False
            
        # Check Docker Compose
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose: {result.stdout.strip()}")
        else:
            print("❌ Docker Compose not found")
            return False
            
        return True
    except FileNotFoundError:
        print("❌ Docker commands not found")
        return False

def check_api_connectivity():
    """Check if NYC Open Data API is accessible"""
    print("\n🌐 Checking API connectivity...")
    try:
        url = "https://data.cityofnewyork.us/resource/k397-673e.csv?$limit=1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ NYC Open Data API is accessible")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ API connection failed: {str(e)}")
        return False

def check_project_structure():
    """Check if all required files are present"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'docker-compose.yml',
        'Dockerfile',
        'requirements.txt',
        'app/main.ipynb',
        '.env'
    ]
    
    all_present = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_present = False
    
    # Check if data directory exists
    data_dir = Path('app/data')
    if data_dir.exists():
        print(f"✅ {data_dir}/")
    else:
        print(f"📁 Creating {data_dir}/")
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ {data_dir}/ - CREATED")
    
    return all_present

def check_requirements():
    """Check Python requirements"""
    print("\n📦 Checking Python requirements...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        key_packages = ['pyspark', 'pandas', 'requests', 'jupyter']
        
        for package in key_packages:
            found = any(package in req.lower() for req in requirements)
            if found:
                print(f"✅ {package} listed in requirements")
            else:
                print(f"❌ {package} missing from requirements")
        
        return True
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def main():
    """Run all validation checks"""
    print("🔍 NYC Payroll ETL - Setup Validation")
    print("=" * 50)
    
    checks = [
        check_project_structure(),
        check_requirements(),
        check_docker_setup(),
        check_api_connectivity()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 All validation checks passed!")
        print("✅ Ready to run: docker-compose up --build")
        print("✅ Then access: http://localhost:8888")
        return 0
    else:
        print("❌ Some validation checks failed")
        print("🔧 Please fix the issues above before running the pipeline")
        return 1

if __name__ == "__main__":
    sys.exit(main())
