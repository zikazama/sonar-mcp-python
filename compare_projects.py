#!/usr/bin/env python3
"""
Script to compare two projects side by side
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

async def compare_projects(project1_key, project1_name, project2_key, project2_name):
    """Compare two projects side by side"""
    service = None
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Connecting to SonarQube at: {sonarqube_url}")
        print("=" * 80)
        
        # Initialize the service
        service = SonarQubeService(
            sonarqube_url,
            sonarqube_token,
            sonarqube_username,
            sonarqube_password
        )
        
        print(f"Comparing projects:")
        print(f"  Project 1: {project1_name} ({project1_key})")
        print(f"  Project 2: {project2_name} ({project2_key})")
        print("=" * 80)
        
        # Get data for both projects
        proj1_coverage = await service.get_coverage_metrics(project1_key)
        proj1_issues = await service.get_issues(project1_key)
        
        proj2_coverage = await service.get_coverage_metrics(project2_key)
        proj2_issues = await service.get_issues(project2_key)
        
        # Calculate issue counts for project 1
        proj1_bug_count = 0
        proj1_code_smell_count = 0
        proj1_issues_list = proj1_issues.get('issues', [])
        for issue in proj1_issues_list:
            issue_type = issue.get('type')
            if issue_type == "BUG":
                proj1_bug_count += 1
            elif issue_type == "CODE_SMELL":
                proj1_code_smell_count += 1
        
        # Calculate issue counts for project 2
        proj2_bug_count = 0
        proj2_code_smell_count = 0
        proj2_issues_list = proj2_issues.get('issues', [])
        for issue in proj2_issues_list:
            issue_type = issue.get('type')
            if issue_type == "BUG":
                proj2_bug_count += 1
            elif issue_type == "CODE_SMELL":
                proj2_code_smell_count += 1
        
        # Display comparison
        print(f"{'Metric':<30} | {project1_name:<25} | {project2_name:<25}")
        print("-" * 80)
        print(f"{'Overall Coverage':<30} | {proj1_coverage.overall_coverage or 'N/A':<25} | {proj2_coverage.overall_coverage or 'N/A':<25}")
        print(f"{'Duplication Rate':<30} | {proj1_coverage.duplication_rate or 'N/A':<25} | {proj2_coverage.duplication_rate or 'N/A':<25}")
        print(f"{'Uncovered Lines':<30} | {proj1_coverage.uncovered_lines or 'N/A':<25} | {proj2_coverage.uncovered_lines or 'N/A':<25}")
        print(f"{'Total Issues':<30} | {proj1_issues.get('total', 'N/A'):<25} | {proj2_issues.get('total', 'N/A'):<25}")
        print(f"{'Bugs':<30} | {proj1_bug_count:<25} | {proj2_bug_count:<25}")
        print(f"{'Code Smells':<30} | {proj1_code_smell_count:<25} | {proj2_code_smell_count:<25}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up resources
        if service:
            await service.close()

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python compare_projects.py <project1_key> <project1_name> <project2_key> <project2_name>")
        print("Example: python compare_projects.py jatis_coster_contact_import \"Jatis Coster Contact Import\" jatis_coster_contact_export \"Jatis Coster Contact Export\"")
        sys.exit(1)
    
    project1_key = sys.argv[1]
    project1_name = sys.argv[2]
    project2_key = sys.argv[3]
    project2_name = sys.argv[4]
    asyncio.run(compare_projects(project1_key, project1_name, project2_key, project2_name))