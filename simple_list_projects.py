#!/usr/bin/env python3
"""
Simple script to list all SonarQube projects
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

async def list_projects():
    """List all SonarQube projects"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        # Initialize the service
        service = SonarQubeService(
            sonarqube_url,
            sonarqube_token,
            sonarqube_username,
            sonarqube_password
        )
        
        # Get all projects
        result = await service.get_projects()
        
        print("SonarQube Projects:")
        print("=" * 40)
        
        for project in result.get('components', []):
            name = project.get('name', 'N/A')
            key = project.get('key', 'N/A')
            print(f"- {name} ({key})")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(list_projects())