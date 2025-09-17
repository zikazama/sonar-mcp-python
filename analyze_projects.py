#!/usr/bin/env python3
"""
Script to get detailed information about all projects in SonarQube
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

async def analyze_sonarqube_projects():
    """Get detailed information about all projects in SonarQube"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Connecting to SonarQube at: {sonarqube_url}")
        print("=" * 60)
        
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
        print("=" * 60)
        
        if projects:
            # Sort projects by name for consistent output
            projects.sort(key=lambda x: x.get('name', '').lower())
            
            for i, project in enumerate(projects, 1):
                project_name = project.get('name', 'N/A')
                project_key = project.get('key', 'N/A')
                
                print(f"{i:2d}. {project_name}")
                print(f"     Key: {project_key}")
                
                try:
                    # Get coverage metrics for each project
                    coverage_data = await service.get_coverage_metrics(project_key)
                    
                    print(f"     Overall Coverage: {coverage_data.overall_coverage or 'N/A'}%")
                    print(f"     Duplication Rate: {coverage_data.duplication_rate or 'N/A'}%")
                    print(f"     Uncovered Lines: {coverage_data.uncovered_lines or 'N/A'}")
                    
                    # Get issues for the project
                    issues_data = await service.get_issues(project_key)
                    total_issues = issues_data.get('total', 0)
                    print(f"     Total Issues: {total_issues}")
                    
                except Exception as e:
                    print(f"     Error getting metrics: {e}")
                
                print()
        else:
            print("No projects found.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(analyze_sonarqube_projects())
