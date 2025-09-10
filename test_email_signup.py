#!/usr/bin/env python3
"""
Simple test script to demonstrate email signup functionality
Run this after starting the FastAPI server
"""

import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_email_signup():
    """Test signup with email"""
    print("Testing email signup functionality...")
    
    # Test data with email
    signup_data = {
        "name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "blood_group": "O+",
        "city": "Karachi",
        "country": "Pakistan",
        "password": "TestPass123!"
    }
    
    try:
        # Test signup
        response = requests.post(f"{BASE_URL}/signup/", json=signup_data)
        print(f"Signup Response Status: {response.status_code}")
        print(f"Signup Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Email signup successful!")
            
            # Test login with email
            login_data = {
                "username": "john.doe@example.com",  # Using email as username
                "password": "TestPass123!"
            }
            
            login_response = requests.post(f"{BASE_URL}/login", data=login_data)
            print(f"\nLogin Response Status: {login_response.status_code}")
            print(f"Login Response: {json.dumps(login_response.json(), indent=2)}")
            
            if login_response.status_code == 200:
                print("✅ Email login successful!")
            else:
                print("❌ Email login failed!")
        else:
            print("❌ Email signup failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_phone_signup():
    """Test signup without email (phone only)"""
    print("\nTesting phone-only signup functionality...")
    
    # Test data without email
    signup_data = {
        "name": "Jane",
        "last_name": "Smith",
        "phone_number": "0987654321",
        "blood_group": "A+",
        "city": "Lahore",
        "country": "Pakistan",
        "password": "TestPass456!"
    }
    
    try:
        # Test signup
        response = requests.post(f"{BASE_URL}/signup/", json=signup_data)
        print(f"Signup Response Status: {response.status_code}")
        print(f"Signup Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✅ Phone-only signup successful!")
            
            # Test login with phone
            login_data = {
                "username": "0987654321",  # Using phone as username
                "password": "TestPass456!"
            }
            
            login_response = requests.post(f"{BASE_URL}/login", data=login_data)
            print(f"\nLogin Response Status: {login_response.status_code}")
            print(f"Login Response: {json.dumps(login_response.json(), indent=2)}")
            
            if login_response.status_code == 200:
                print("✅ Phone login successful!")
            else:
                print("❌ Phone login failed!")
        else:
            print("❌ Phone-only signup failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Blood Donation API Email Signup Functionality")
    print("=" * 60)
    
    test_email_signup()
    test_phone_signup()
    
    print("\n" + "=" * 60)
    print("Test completed!")
