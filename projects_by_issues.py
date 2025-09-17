#!/usr/bin/env python3
"""
Script to get projects with the most issues
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

async def projects_by_issues():
    """Get projects sorted by number of issues"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Connecting to SonarQube at: {sonarqube_url}")
        print("=" * 70)
        
        # Initialize the service
        service = SonarQubeService(
            sonarqube_url,
            sonarqube_token,
            sonarqube_username,
            sonarqube_password
        )
        
        print("Fetching all projects...")
        projects_data = await service.get_projects(page=1, page_size=100)
        projects = projects_data.get('components', [])
        
        print(f"Analyzing issues for {len(projects)} projects...")
        
        # Get issues for each project
        project_issues_data = []
        
        for project in projects:
            try:
                project_key = project.get('key')
                project_name = project.get('name')
                
                issues_data = await service.get_issues(project_key)
                total_issues = issues_data.get('total', 0)
                
                project_issues_data.append({
                    'name': project_name,
                    'key': project_key,
                    'total_issues': total_issues
                })
            except Exception as e:
                print(f"Error getting issues for {project.get('name')}: {e}")
                continue
        
        # Sort by total issues (descending)
        project_issues_data.sort(key=lambda x: x['total_issues'], reverse=True)
        
        print(f"\nProjects with Most Issues:")
        print("=" * 70)
        
        for i, project_data in enumerate(project_issues_data[:10], 1):
            print(f"{i:2d}. {project_data['name']}")
            print(f"     Key: {project_data['key']}")
            print(f"     Total Issues: {project_data['total_issues']}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(projects_by_issues())