import asyncio
import sys
import os
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from sonarqube_service import SonarQubeService

async def get_project_coverage(project_key, project_name):
    """Get coverage metrics for a specific project"""
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
        
        print(f"Getting coverage metrics for project: {project_name} ({project_key})")
        print("-" * 50)
        
        # Get coverage metrics
        coverage_data = await service.get_coverage_metrics(project_key)
        
        print(f"Coverage Metrics for {project_name}:")
        print(f"  Overall Coverage: {coverage_data.overall_coverage or 'N/A'}")
        print(f"  New Code Coverage: {coverage_data.new_code_coverage or 'N/A'}")
        print(f"  Duplication Rate: {coverage_data.duplication_rate or 'N/A'}%")
        print(f"  Uncovered Lines: {coverage_data.uncovered_lines or 'N/A'}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_coverage.py <project_key> <project_name>")
        sys.exit(1)
    
    project_key = sys.argv[1]
    project_name = sys.argv[2]
    asyncio.run(get_project_coverage(project_key, project_name))