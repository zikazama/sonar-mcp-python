#!/usr/bin/env python3
"""
Script to get uncovered lines for the Jatis Coster Contact Import project
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

async def get_uncovered_lines():
    """Get uncovered lines for the Jatis Coster Contact Import project"""
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
        
        project_key = "jatis_coster_contact_import"
        project_name = "Jatis Coster Contact Import"
        
        print(f"Getting uncovered lines for project: {project_name}")
        print(f"Project Key: {project_key}")
        print("=" * 70)
        
        # Get uncovered lines
        uncovered_data = await service.get_uncovered_lines(project_key)
        
        print(f"Uncovered Lines Information:")
        print(f"  Component Key: {uncovered_data.component_key}")
        print(f"  Component Name: {uncovered_data.component_name}")
        print(f"  Metric: {uncovered_data.metric}")
        print(f"  Value: {uncovered_data.value}")
        
        # Also get detailed coverage metrics
        print(f"\nDetailed Coverage Metrics:")
        coverage_data = await service.get_coverage_metrics(project_key)
        
        print(f"  Overall Coverage: {coverage_data.overall_coverage or 'N/A'}%")
        print(f"  New Code Coverage: {coverage_data.new_code_coverage or 'N/A'}%")
        print(f"  Duplication Rate: {coverage_data.duplication_rate or 'N/A'}%")
        print(f"  Uncovered Lines: {coverage_data.uncovered_lines or 'N/A'}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up resources
        if service:
            await service.close()

if __name__ == "__main__":
    asyncio.run(get_uncovered_lines())