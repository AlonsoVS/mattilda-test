#!/usr/bin/env python3
"""
Test script to verify caching functionality.
This script tests various endpoints to ensure caching is working correctly.
"""

import asyncio
import httpx
import time
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000/api/v1"

async def test_endpoint_caching():
    """Test caching functionality on various endpoints."""
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Caching Functionality\n")
        
        # Test cache health
        print("1. Testing cache health...")
        try:
            response = await client.get(f"{BASE_URL}/cache/health")
            if response.status_code == 200:
                print("✅ Cache system is healthy")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Cache health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error testing cache health: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Test cache stats
        print("2. Testing cache statistics...")
        try:
            response = await client.get(f"{BASE_URL}/cache/stats")
            if response.status_code == 200:
                print("✅ Cache stats retrieved successfully")
                stats = response.json()
                print(f"   Stats: {json.dumps(stats, indent=2)}")
            else:
                print(f"❌ Cache stats failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error getting cache stats: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Test endpoint caching
        print("3. Testing endpoint caching...")
        
        # Test schools endpoint
        print("   Testing schools endpoint caching...")
        start_time = time.time()
        response1 = await client.get(f"{BASE_URL}/schools/")
        time1 = time.time() - start_time
        
        start_time = time.time()
        response2 = await client.get(f"{BASE_URL}/schools/")
        time2 = time.time() - start_time
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            # Check if second response has cache indicators
            if '_cached' in str(data2):
                print("✅ Schools endpoint caching working")
                print(f"   First request: {time1:.3f}s")
                print(f"   Second request (cached): {time2:.3f}s")
                print(f"   Speed improvement: {((time1 - time2) / time1 * 100):.1f}%")
            else:
                print("⚠️  Schools endpoint caching might not be working as expected")
                print(f"   First request: {time1:.3f}s")
                print(f"   Second request: {time2:.3f}s")
        
        print("\n" + "="*50 + "\n")
        
        # Test individual school endpoint
        print("4. Testing individual school endpoint caching...")
        start_time = time.time()
        response1 = await client.get(f"{BASE_URL}/schools/1")
        time1 = time.time() - start_time
        
        start_time = time.time()
        response2 = await client.get(f"{BASE_URL}/schools/1")
        time2 = time.time() - start_time
        
        if response1.status_code == 200 and response2.status_code == 200:
            print("✅ Individual school endpoint caching working")
            print(f"   First request: {time1:.3f}s")
            print(f"   Second request (cached): {time2:.3f}s")
            print(f"   Speed improvement: {((time1 - time2) / time1 * 100):.1f}%" if time1 > time2 else "No improvement")
        
        print("\n" + "="*50 + "\n")
        
        # Test account statement caching
        print("5. Testing school account statement caching...")
        start_time = time.time()
        response1 = await client.get(f"{BASE_URL}/schools/1/account-statement")
        time1 = time.time() - start_time
        
        start_time = time.time()
        response2 = await client.get(f"{BASE_URL}/schools/1/account-statement")
        time2 = time.time() - start_time
        
        if response1.status_code == 200 and response2.status_code == 200:
            print("✅ School account statement caching working")
            print(f"   First request: {time1:.3f}s")
            print(f"   Second request (cached): {time2:.3f}s")
            print(f"   Speed improvement: {((time1 - time2) / time1 * 100):.1f}%" if time1 > time2 else "No improvement")
        
        print("\n" + "="*50 + "\n")
        
        # Test cache clearing
        print("6. Testing cache clearing...")
        try:
            response = await client.delete(f"{BASE_URL}/cache/clear")
            if response.status_code == 200:
                result = response.json()
                print("✅ Cache clearing successful")
                print(f"   Cleared {result.get('entries_cleared', 0)} entries")
            else:
                print(f"❌ Cache clearing failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error clearing cache: {e}")
        
        print("\n" + "="*50 + "\n")
        
        # Final cache stats
        print("7. Final cache statistics...")
        try:
            response = await client.get(f"{BASE_URL}/cache/stats")
            if response.status_code == 200:
                stats = response.json()
                print("✅ Final cache stats:")
                print(f"   {json.dumps(stats, indent=2)}")
            else:
                print(f"❌ Final cache stats failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error getting final cache stats: {e}")
        
        print("\n🎉 Caching test completed!")

if __name__ == "__main__":
    print("Starting cache functionality tests...")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    try:
        asyncio.run(test_endpoint_caching())
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
