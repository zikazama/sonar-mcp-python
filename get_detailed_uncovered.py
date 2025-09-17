#!/usr/bin/env python3
"""
Script to get detailed uncovered lines information for the Jatis Coster Contact Import project
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
import httpx

async def get_detailed_uncovered_lines():
    """Get detailed uncovered lines information for the Jatis Coster Contact Import project"""
    try:
        # Get configuration from environment
        sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        
        print(f"Connecting to SonarQube at: {sonarqube_url}")
        print("=" * 70)
        
        project_key = "jatis_coster_contact_import"
        project_name = "Jatis Coster Contact Import"
        
        print(f"Getting detailed uncovered lines for project: {project_name}")
        print(f"Project Key: {project_key}")
        print("=" * 70)
        
        # Prepare authentication
        auth = None
        if sonarqube_token:
            auth = (sonarqube_token, "")
        elif sonarqube_username and sonarqube_password:
            auth = (sonarqube_username, sonarqube_password)
        
        # Use direct HTTP request to get sources and coverage information
        async with httpx.AsyncClient() as client:
            # Get components (files) in the project
            components_url = f"{sonarqube_url}/api/sources/raw"
            components_params = {
                "key": project_key
            }
            
            try:
                # Try to get project components
                search_url = f"{sonarqube_url}/api/components/tree"
                search_params = {
                    "component": project_key,
                    "qualifiers": "FIL"
                }
                
                response = await client.get(
                    search_url,
                    params=search_params,
                    auth=auth,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Project files found: {len(data.get('components', []))}")
                    
                    # Get coverage data for each file
                    coverage_url = f"{sonarqube_url}/api/measures/component"
                    
                    for component in data.get('components', [])[:5]:  # Limit to first 5 files
                        component_key = component.get('key')
                        component_name = component.get('name')
                        
                        print(f"\nFile: {component_name}")
                        print(f"Key: {component_key}")
                        
                        # Get coverage metrics for this file
                        coverage_params = {
                            "component": component_key,
                            "metricKeys": "lines_to_cover,uncovered_lines,line_coverage"
                        }
                        
                        coverage_response = await client.get(
                            coverage_url,
                            params=coverage_params,
                            auth=auth,
                            timeout=30.0
                        )
                        
                        if coverage_response.status_code == 200:
                            coverage_data = coverage_response.json()
                            measures = coverage_data.get("component", {}).get("measures", [])
                            
                            lines_to_cover = "N/A"
                            uncovered_lines = "N/A"
                            line_coverage = "N/A"
                            
                            for measure in measures:
                                if measure.get("metric") == "lines_to_cover":
                                    lines_to_cover = measure.get("value", "N/A")
                                elif measure.get("metric") == "uncovered_lines":
                                    uncovered_lines = measure.get("value", "N/A")
                                elif measure.get("metric") == "line_coverage":
                                    line_coverage = measure.get("value", "N/A")
                            
                            print(f"  Lines to cover: {lines_to_cover}")
                            print(f"  Uncovered lines: {uncovered_lines}")
                            print(f"  Line coverage: {line_coverage}%")
                        else:
                            print(f"  Failed to get coverage data: {coverage_response.status_code}")
                else:
                    print(f"Failed to get project components: {response.status_code}")
                    print(response.text)
                    
            except Exception as e:
                print(f"Error getting project data: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(get_detailed_uncovered_lines())