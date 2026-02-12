#!/usr/bin/env python3
"""
Emergency Routing System - Complete Testing & Verification Script
Tests all endpoints and features for functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_URL = "http://localhost:5000/api"
TEST_RESULTS = []

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

def print_test(name, status, message=""):
    """Print test result"""
    symbol = "[OK]" if status else "[X]"
    TEST_RESULTS.append((name, status, message))
    print(f"{symbol} {name}")
    if message:
        print(f"  |-- {message}")

def test_health_check():
    """Test 1: Health check endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print_test("Health Check", True)
                return True
        print_test("Health Check", False, f"Status code: {response.status_code}")
        return False
    except Exception as e:
        print_test("Health Check", False, str(e))
        return False

def test_get_hospitals():
    """Test 2: Get all hospitals"""
    try:
        response = requests.get(f"{API_URL}/hospitals/")
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("hospitals"):
                print_test("Get Hospitals", True, f"Found {len(data['hospitals'])} hospitals")
                return True, data['hospitals']
        print_test("Get Hospitals", False, f"Status: {response.status_code}")
        return False, []
    except Exception as e:
        print_test("Get Hospitals", False, str(e))
        return False, []

def test_find_hospital():
    """Test 3: Find nearest hospital"""
    try:
        payload = {
            "patient_type": "Serious",
            "emergency_type": "Accident",
            "needs": {
                "bed": True,
                "icu": True,
                "oxygen": False,
                "ventilator": False
            }
        }
        response = requests.post(f"{API_URL}/ambulance/find-hospital", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("request_id"):
                print_test("Find Hospital", True, f"Request ID: {data['request_id']}, Distance: {data['distance']}km")
                return True, data['request_id']
        print_test("Find Hospital", False, f"Status: {response.status_code}")
        return False, None
    except Exception as e:
        print_test("Find Hospital", False, str(e))
        return False, None

def test_get_pending_requests():
    """Test 4: Get pending requests"""
    try:
        response = requests.get(f"{API_URL}/hospital/pending-requests")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test("Get Pending Requests", True, f"Found {len(data['requests'])} requests")
                return True, data['requests']
        print_test("Get Pending Requests", False, f"Status: {response.status_code}")
        return False, []
    except Exception as e:
        print_test("Get Pending Requests", False, str(e))
        return False, []

def test_check_status(request_id):
    """Test 5: Check request status"""
    if not request_id:
        print_test("Check Status", False, "No request ID available")
        return False
    try:
        payload = {"request_id": request_id}
        response = requests.post(f"{API_URL}/ambulance/check-status", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test("Check Status", True, f"Status: {data['status']}")
                return True
        print_test("Check Status", False, f"Status: {response.status_code}")
        return False
    except Exception as e:
        print_test("Check Status", False, str(e))
        return False

def test_accept_request(request_id):
    """Test 6: Accept request"""
    if not request_id:
        print_test("Accept Request", False, "No request ID available")
        return False
    try:
        payload = {"request_id": request_id}
        response = requests.post(f"{API_URL}/hospital/accept-request", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_test("Accept Request", True)
                return True
        print_test("Accept Request", False, f"Status: {response.status_code}")
        return False
    except Exception as e:
        print_test("Accept Request", False, str(e))
        return False

def test_get_stats():
    """Test 7: Get statistics"""
    try:
        response = requests.get(f"{API_URL}/ambulance/stats")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = f"Hospitals: {data['total_hospitals']}, Pending: {data['pending_count']}, Accepted: {data['accepted_count']}"
                print_test("Get Statistics", True, stats)
                return True
        print_test("Get Statistics", False, f"Status: {response.status_code}")
        return False
    except Exception as e:
        print_test("Get Statistics", False, str(e))
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{BLUE}{'='*70}{END}")
    print(f"{BLUE}Emergency Routing System - Complete Feature Testing{END}")
    print(f"{BLUE}{'='*70}{END}\n")
    
    print(f"{YELLOW}Testing API Endpoints...{END}\n")
    
    # Test 1: Health check
    test_health_check()
    
    # Test 2: Get hospitals
    success, hospitals = test_get_hospitals()
    
    # Test 3: Find hospital
    success, request_id = test_find_hospital()
    
    # Test 4: Get pending requests
    success, requests_list = test_get_pending_requests()
    
    # Test 5: Check status
    if request_id:
        test_check_status(request_id)
    
    # Test 6: Accept request
    if request_id:
        test_accept_request(request_id)
    
    # Test 7: Get statistics
    test_get_stats()
    
    # Print summary
    print(f"\n{BLUE}{'='*70}{END}")
    print(f"{BLUE}Test Summary{END}")
    print(f"{BLUE}{'='*70}{END}\n")
    
    passed = sum(1 for _, status, _ in TEST_RESULTS if status)
    total = len(TEST_RESULTS)
    
    for name, status, message in TEST_RESULTS:
        symbol = "[OK]" if status else "[X]"
        print(f"{symbol} {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("[OK] All features working correctly!\n")
    else:
        print("[X] Some tests failed. Check errors above.\n")

if __name__ == "__main__":
    print(f"\n{YELLOW}Starting tests... (Make sure backend is running at {API_URL}){END}")
    time.sleep(1)
    run_all_tests()
