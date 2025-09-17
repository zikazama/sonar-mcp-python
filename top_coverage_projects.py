#!/usr/bin/env python3
"""
Script to get top 5 projects by coverage
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

async def top_projects_by_coverage():
    """Get top 5 projects by coverage"""
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
        
        print(f"Analyzing coverage for {len(projects)} projects...")
        
        # Get coverage for each project
        project_coverage_data = []
        
        for project in projects:
            try:
                project_key = project.get('key')
                project_name = project.get('name')
                
                coverage_data = await service.get_coverage_metrics(project_key)
                coverage_value = coverage_data.overall_coverage
                
                # Convert to float for sorting, handle None/NaN values
                if coverage_value and coverage_value != 'N/A':
                    try:
                        coverage_float = float(coverage_value)
                        project_coverage_data.append({
                            'name': project_name,
                            'key': project_key,
                            'coverage': coverage_float,
                            'duplication': coverage_data.duplication_rate,
                            'uncovered_lines': coverage_data.uncovered_lines
                        })
                    except ValueError:
                        # Skip projects with invalid coverage values
                        pass
                else:
                    # Add projects with no coverage data at the end
                    project_coverage_data.append({
                        'name': project_name,
                        'key': project_key,
                        'coverage': 0.0,
                        'duplication': coverage_data.duplication_rate,
                        'uncovered_lines': coverage_data.uncovered_lines
                    })
            except Exception as e:
                print(f"Error getting coverage for {project.get('name')}: {e}")
                continue
        
        # Sort by coverage (descending)
        project_coverage_data.sort(key=lambda x: x['coverage'], reverse=True)
        
        print(f"\nTop 5 Projects by Code Coverage:")
        print("=" * 70)
        
        for i, project_data in enumerate(project_coverage_data[:5], 1):
            print(f"{i}. {project_data['name']}")
            print(f"   Key: {project_data['key']}")
            print(f"   Coverage: {project_data['coverage']}%")
            print(f"   Duplication: {project_data['duplication'] or 'N/A'}%")
            print(f"   Uncovered Lines: {project_data['uncovered_lines'] or 'N/A'}")
            print()
            
        print(f"\nBottom 5 Projects by Code Coverage:")
        print("=" * 70)
        
        for i, project_data in enumerate(project_coverage_data[-5:], len(project_coverage_data)-4):
            if i > 0:  # Only show if there are enough projects
                print(f"{i}. {project_data['name']}")
                print(f"   Key: {project_data['key']}")
                print(f"   Coverage: {project_data['coverage']}%")
                print(f"   Duplication: {project_data['duplication'] or 'N/A'}%")
                print(f"   Uncovered Lines: {project_data['uncovered_lines'] or 'N/A'}")
                print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(top_projects_by_coverage())