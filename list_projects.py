#!/usr/bin/env python3
"""
Script to list all projects in SonarQube
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
import os

async def list_sonarqube_projects():
    """List all projects in SonarQube"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Connecting to SonarQube at: {sonarqube_url}")
        print("=" * 50)
        
        # Initialize the service
        service = SonarQubeService(
            sonarqube_url,
            sonarqube_token,
            sonarqube_username,
            sonarqube_password
        )
        
        # Get all projects
        print("Fetching projects...")
        projects_data = await service.get_projects(page=1, page_size=100)
        
        # Display results
        total_projects = projects_data.get('paging', {}).get('total', 0)
        projects = projects_data.get('components', [])
        
        print(f"\nFound {total_projects} projects in SonarQube:")
        print("-" * 50)
        
        if projects:
            for i, project in enumerate(projects, 1):
                print(f"{i:2d}. {project.get('name', 'N/A')}")
                print(f"     Key: {project.get('key', 'N/A')}")
                if project.get('lastAnalysisDate'):
                    print(f"     Last Analysis: {project.get('lastAnalysisDate')}")
                print()
        else:
            print("No projects found.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(list_sonarqube_projects())