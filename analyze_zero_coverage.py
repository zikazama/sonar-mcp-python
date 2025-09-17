#!/usr/bin/env python3
"""
Script to analyze projects with 0.0% code coverage in detail
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

async def analyze_zero_coverage_projects():
    """Analyze projects with 0.0% code coverage in detail"""
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
        
        # Get all projects
        print("Fetching projects...")
        projects_data = await service.get_projects(page=1, page_size=100)
        
        # Filter projects with 0.0% coverage
        projects = projects_data.get('components', [])
        zero_coverage_projects = []
        
        print("Analyzing projects for code coverage...")
        for project in projects:
            project_key = project.get('key', 'N/A')
            try:
                # Get coverage metrics for each project
                coverage_data = await service.get_coverage_metrics(project_key)
                if coverage_data.overall_coverage == "0.0":
                    zero_coverage_projects.append({
                        'project': project,
                        'coverage_data': coverage_data
                    })
            except Exception as e:
                print(f"Error getting metrics for {project_key}: {e}")
        
        print(f"\nFound {len(zero_coverage_projects)} projects with 0.0% code coverage:")
        print("=" * 70)
        
        if zero_coverage_projects:
            # Sort by project name
            zero_coverage_projects.sort(key=lambda x: x['project'].get('name', '').lower())
            
            for i, project_info in enumerate(zero_coverage_projects, 1):
                project = project_info['project']
                coverage_data = project_info['coverage_data']
                
                project_name = project.get('name', 'N/A')
                project_key = project.get('key', 'N/A')
                
                print(f"{i}. {project_name}")
                print(f"   Key: {project_key}")
                print(f"   Overall Coverage: {coverage_data.overall_coverage or 'N/A'}%")
                print(f"   Duplication Rate: {coverage_data.duplication_rate or 'N/A'}%")
                print(f"   Uncovered Lines: {coverage_data.uncovered_lines or 'N/A'}")
                
                # Get detailed issues breakdown
                try:
                    issues_data = await service.get_issues(
                        project_key,
                        types=["BUG", "VULNERABILITY", "CODE_SMELL"],
                        severities=["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]
                    )
                    
                    # Count issues by type
                    bug_count = 0
                    vulnerability_count = 0
                    code_smell_count = 0
                    
                    issues = issues_data.get('issues', [])
                    for issue in issues:
                        issue_type = issue.get('type')
                        if issue_type == "BUG":
                            bug_count += 1
                        elif issue_type == "VULNERABILITY":
                            vulnerability_count += 1
                        elif issue_type == "CODE_SMELL":
                            code_smell_count += 1
                    
                    print(f"   Issues Breakdown:")
                    print(f"     - Bugs: {bug_count}")
                    print(f"     - Vulnerabilities: {vulnerability_count}")
                    print(f"     - Code Smells: {code_smell_count}")
                    print(f"     - Total: {len(issues)}")
                    
                    # Get issues by severity
                    blocker_count = 0
                    critical_count = 0
                    major_count = 0
                    minor_count = 0
                    info_count = 0
                    
                    for issue in issues:
                        severity = issue.get('severity')
                        if severity == "BLOCKER":
                            blocker_count += 1
                        elif severity == "CRITICAL":
                            critical_count += 1
                        elif severity == "MAJOR":
                            major_count += 1
                        elif severity == "MINOR":
                            minor_count += 1
                        elif severity == "INFO":
                            info_count += 1
                    
                    print(f"   Severity Breakdown:")
                    print(f"     - Blocker: {blocker_count}")
                    print(f"     - Critical: {critical_count}")
                    print(f"     - Major: {major_count}")
                    print(f"     - Minor: {minor_count}")
                    print(f"     - Info: {info_count}")
                    
                except Exception as e:
                    print(f"   Error getting detailed issues: {e}")
                
                print()
        else:
            print("No projects found with 0.0% code coverage.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(analyze_zero_coverage_projects())
