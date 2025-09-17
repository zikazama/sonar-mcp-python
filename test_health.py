#!/usr/bin/env python3
"""
Script to test SonarQube connection health
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from sonarqube_service import SonarQubeService
import httpx

async def test_health():
    """Test SonarQube connection health"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Testing connection to SonarQube at: {sonarqube_url}")
        
        # Prepare authentication
        auth = None
        if sonarqube_token:
            auth = (sonarqube_token, "")
        elif sonarqube_username and sonarqube_password:
            auth = (sonarqube_username, sonarqube_password)
        
        # Test system status endpoint
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{sonarqube_url}/api/system/status",
                auth=auth,
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                print("SonarQube Health Check: OK")
                print(f"  Status: {data.get('status', 'N/A')}")
                print(f"  Version: {data.get('version', 'N/A')}")
                print(f"  Edition: {data.get('edition', 'N/A')}")
            else:
                print(f"SonarQube Health Check: FAILED")
                print(f"  Status code: {response.status_code}")
                print(f"  Response: {response.text}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_health())