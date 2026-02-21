#!/usr/bin/env python3
"""Test script to verify JWT authentication is working"""
import requests
import json
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8001/api/v1"

print("=" * 60)
print("Testing JWT Authentication Flow")
print("=" * 60)

# Step 1: Login
print("\n1. Testing login...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"email": "demo@example.com", "password": "Password123!"}
)

print(f"   Status: {login_response.status_code}")
if login_response.status_code == 200:
    login_data = login_response.json()
    print(f"   [OK] Login successful")
    print(f"   User ID: {login_data.get('user_id')}")
    print(f"   Token: {login_data.get('access_token')[:30]}...")

    token = login_data.get('access_token')

    # Step 2: Test tasks endpoint with JWT
    print("\n2. Testing tasks endpoint with JWT token...")
    tasks_response = requests.get(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"   Status: {tasks_response.status_code}")
    if tasks_response.status_code == 200:
        print(f"   [OK] Tasks endpoint working with JWT!")
        tasks = tasks_response.json()
        print(f"   Found {len(tasks)} tasks")
    else:
        print(f"   [FAIL] Tasks endpoint failed!")
        print(f"   Error: {tasks_response.json()}")
else:
    print(f"   [FAIL] Login failed!")
    print(f"   Error: {login_response.json()}")

print("\n" + "=" * 60)
