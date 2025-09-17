#!/usr/bin/env python3
"""
Script to test all SonarQube MCP tools
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

async def test_all_tools():
    """Test all SonarQube MCP tools"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Testing all SonarQube MCP tools")
        print(f"SonarQube URL: {sonarqube_url}")
        print("=" * 50)
        
        # Initialize the service
        service = SonarQubeService(
            sonarqube_url,
            sonarqube_token,
            sonarqube_username,
            sonarqube_password
        )
        
        # Test 1: get_all_projects
        print("1. Testing get_all_projects...")
        try:
            projects_data = await service.get_projects(page=1, page_size=5)  # Limit to 5 for testing
            total_projects = projects_data.get('paging', {}).get('total', 0)
            components = projects_data.get('components', [])
            print(f"   SUCCESS: Found {total_projects} projects")
            print(f"   Sample projects: {len(components)}")
            for project in components[:3]:  # Show first 3
                print(f"     - {project.get('name', 'N/A')} ({project.get('key', 'N/A')})")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        # Use a known project for the remaining tests
        test_project_key = "jatis_coster_contact_import"
        test_project_name = "Jatis Coster Contact Import"
        print(f"\nUsing test project: {test_project_name} ({test_project_key})")
        print("-" * 50)
        
        # Test 2: get_coverage_metrics
        print("2. Testing get_coverage_metrics...")
        try:
            coverage_data = await service.get_coverage_metrics(test_project_key)
            print(f"   SUCCESS:")
            print(f"     Overall Coverage: {coverage_data.overall_coverage or 'N/A'}%")
            print(f"     New Code Coverage: {coverage_data.new_code_coverage or 'N/A'}%")
            print(f"     Duplication Rate: {coverage_data.duplication_rate or 'N/A'}%")
            print(f"     Uncovered Lines: {coverage_data.uncovered_lines or 'N/A'}")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        # Test 3: get_overall_coverage
        print("3. Testing get_overall_coverage...")
        try:
            overall_coverage = await service.get_overall_coverage(test_project_key)
            print(f"   SUCCESS: {overall_coverage.value or 'N/A'}%")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        # Test 4: get_new_code_coverage
        print("4. Testing get_new_code_coverage...")
        try:
            new_coverage = await service.get_new_code_coverage(test_project_key)
            print(f"   SUCCESS: {new_coverage.value or 'N/A'}%")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        # Test 5: get_duplication_rate
        print("5. Testing get_duplication_rate...")
        try:
            duplication_rate = await service.get_duplication_rate(test_project_key)
            print(f"   SUCCESS: {duplication_rate.value or 'N/A'}%")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        # Test 6: get_uncovered_lines
        print("6. Testing get_uncovered_lines...")
        try:
            uncovered_lines = await service.get_uncovered_lines(test_project_key)
            print(f"   SUCCESS: {uncovered_lines.value or 'N/A'} lines")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        # Test 7: get_project_issues
        print("7. Testing get_project_issues...")
        try:
            issues_data = await service.get_issues(test_project_key, types=["BUG", "CODE_SMELL"])
            total_issues = issues_data.get('total', 0)
            print(f"   SUCCESS: Found {total_issues} issues")
            
            # Show issue breakdown
            issues = issues_data.get('issues', [])
            bug_count = sum(1 for issue in issues if issue.get('type') == 'BUG')
            code_smell_count = sum(1 for issue in issues if issue.get('type') == 'CODE_SMELL')
            print(f"     Bugs: {bug_count}")
            print(f"     Code Smells: {code_smell_count}")
        except Exception as e:
            print(f"   FAILED: {e}")
        
        print("\n" + "=" * 50)
        print("All tool tests completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_all_tools())