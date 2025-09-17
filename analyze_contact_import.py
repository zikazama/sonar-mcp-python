#!/usr/bin/env python3
"""
Script to get detailed information about the Jatis Coster Contact Import project
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

async def analyze_contact_import_project():
    """Get detailed information about the Jatis Coster Contact Import project"""
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
        
        project_key = "jatis_coster_contact_import"
        project_name = "Jatis Coster Contact Import"
        
        print(f"Analyzing project: {project_name}")
        print(f"Project Key: {project_key}")
        print("=" * 70)
        
        # Get coverage metrics
        print("Getting coverage metrics...")
        coverage_data = await service.get_coverage_metrics(project_key)
        
        print(f"\nCoverage Metrics:")
        print(f"  Overall Coverage: {coverage_data.overall_coverage or 'N/A'}%")
        print(f"  New Code Coverage: {coverage_data.new_code_coverage or 'N/A'}%")
        print(f"  Duplication Rate: {coverage_data.duplication_rate or 'N/A'}%")
        print(f"  Uncovered Lines: {coverage_data.uncovered_lines or 'N/A'}")
        
        # Get issues
        print("\nGetting issues...")
        issues_data = await service.get_issues(project_key)
        total_issues = issues_data.get('total', 0)
        
        print(f"\nIssues Summary:")
        print(f"  Total Issues: {total_issues}")
        
        # Get issues by type
        issues_by_type = await service.get_issues(
            project_key,
            types=["BUG", "VULNERABILITY", "CODE_SMELL"]
        )
        
        bug_count = 0
        vulnerability_count = 0
        code_smell_count = 0
        
        issues = issues_by_type.get('issues', [])
        for issue in issues:
            issue_type = issue.get('type')
            if issue_type == "BUG":
                bug_count += 1
            elif issue_type == "VULNERABILITY":
                vulnerability_count += 1
            elif issue_type == "CODE_SMELL":
                code_smell_count += 1
        
        print(f"\nIssues by Type:")
        print(f"  Bugs: {bug_count}")
        print(f"  Vulnerabilities: {vulnerability_count}")
        print(f"  Code Smells: {code_smell_count}")
        
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
        
        print(f"\nIssues by Severity:")
        print(f"  Blocker: {blocker_count}")
        print(f"  Critical: {critical_count}")
        print(f"  Major: {major_count}")
        print(f"  Minor: {minor_count}")
        print(f"  Info: {info_count}")
        
        # Show some sample issues
        print(f"\nSample Issues (first 5):")
        print("-" * 40)
        for i, issue in enumerate(issues[:5]):
            print(f"{i+1}. {issue.get('type', 'N/A')}: {issue.get('message', 'N/A')[:40]}...")
            print(f"   Severity: {issue.get('severity', 'N/A')}")
            print(f"   Component: {issue.get('component', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(analyze_contact_import_project())