#!/usr/bin/env python3
"""
Test script to verify SonarQube connection from within the container
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

async def test_connection():
    """Test SonarQube connection from within the container"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://host.docker.internal:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Testing connection to SonarQube at: {sonarqube_url}")
        print("=" * 50)
        
        # Initialize the service
        service = SonarQubeService(
            sonarqube_url,
            sonarqube_token,
            sonarqube_username,
            sonarqube_password
        )
        
        # Test get_projects function
        print("Testing get_projects function...")
        projects_data = await service.get_projects(page=1, page_size=1)
        
        # Display results
        total_projects = projects_data.get('paging', {}).get('total', 0)
        projects = projects_data.get('components', [])
        
        print(f"SUCCESS: Found {total_projects} projects in SonarQube")
        if projects:
            project = projects[0]
            print(f"First project: {project.get('name', 'N/A')} (Key: {project.get('key', 'N/A')})")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())