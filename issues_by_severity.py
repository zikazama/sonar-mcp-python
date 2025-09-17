#!/usr/bin/env python3
"""
Script to get detailed issues breakdown by severity for a project
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

async def project_issues_by_severity(project_key, project_name):
    """Get detailed issues breakdown by severity for a project"""
    service = None
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
        
        print(f"Analyzing issues for project: {project_name}")
        print(f"Project Key: {project_key}")
        print("=" * 70)
        
        # Get all issues
        issues_data = await service.get_issues(project_key)
        issues = issues_data.get('issues', [])
        
        print(f"Total Issues: {issues_data.get('total', 0)}")
        print()
        
        # Count issues by severity
        severity_counts = {}
        type_counts = {}
        
        for issue in issues:
            severity = issue.get('severity', 'UNKNOWN')
            issue_type = issue.get('type', 'UNKNOWN')
            
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
        
        print("Issues by Severity:")
        print("-" * 30)
        severities = ['BLOCKER', 'CRITICAL', 'MAJOR', 'MINOR', 'INFO']
        for severity in severities:
            count = severity_counts.get(severity, 0)
            print(f"{severity:12}: {count}")
        
        print()
        print("Issues by Type:")
        print("-" * 30)
        types = ['BUG', 'VULNERABILITY', 'CODE_SMELL', 'SECURITY_HOTSPOT']
        for issue_type in types:
            count = type_counts.get(issue_type, 0)
            print(f"{issue_type:16}: {count}")
        
        print()
        print("Detailed Issues (first 10):")
        print("-" * 50)
        
        for i, issue in enumerate(issues[:10], 1):
            message = issue.get('message', 'N/A')
            # Truncate long messages
            if len(message) > 60:
                message = message[:60] + "..."
            print(f"{i:2d}. [{issue.get('severity', 'N/A')}] {issue.get('type', 'N/A')}")
            print(f"    {message}")
            component = issue.get('component', 'N/A')
            # Show only the file name, not the full path
            if ':' in component:
                component = component.split(':')[-1]
            print(f"    File: {component}")
            print()
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up resources
        if service:
            await service.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python issues_by_severity.py <project_key> <project_name>")
        print("Example: python issues_by_severity.py jatis_coster_contact_import \"Jatis Coster Contact Import\"")
        sys.exit(1)
    
    project_key = sys.argv[1]
    project_name = sys.argv[2]
    asyncio.run(project_issues_by_severity(project_key, project_name))