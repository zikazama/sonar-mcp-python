#!/usr/bin/env python3
"""
Comprehensive test script to verify all tools
"""

import asyncio
import sys
import os
import json
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from mcp_server import SonarQubeMCP

async def test_all_tools():
    """Test all tools to identify any issues"""
    try:
        # Initialize the MCP server
        mcp = SonarQubeMCP()
        
        # Test 1: Health check
        print("Test 1: Health check")
        health_request = {
            "method": "tools/call",
            "params": {
                "name": "health_check",
                "arguments": {}
            }
        }
        
        response = await mcp.handle_request(health_request)
        print(f"Health check result: {response.get('result', {}).get('content', [{}])[0].get('text', 'N/A')}")
        print()
        
        # Test 2: List tools
        print("Test 2: List tools")
        tools_request = {
            "method": "tools/list",
            "params": {}
        }
        
        response = await mcp.handle_request(tools_request)
        tools = response.get('result', {}).get('tools', [])
        print(f"Available tools: {[tool['name'] for tool in tools]}")
        print()
        
        # Test 3: Get all projects with exact parameters from error
        print("Test 3: Get all projects with page=1, page_size=100")
        projects_request = {
            "method": "tools/call",
            "params": {
                "name": "get_all_projects",
                "arguments": {
                    "page": 1,
                    "page_size": 100
                }
            }
        }
        
        response = await mcp.handle_request(projects_request)
        
        if "error" in response:
            print("ERROR in get_all_projects:")
            print(f"  Code: {response['error'].get('code')}")
            print(f"  Message: {response['error'].get('message')}")
            print(f"  Data: {response['error'].get('data')}")
        else:
            print("SUCCESS: get_all_projects worked correctly")
            # Try to parse the result to see how many projects we got
            try:
                result_text = response.get('result', {}).get('content', [{}])[0].get('text', '{}')
                result_data = json.loads(result_text)
                projects_count = len(result_data.get('components', []))
                total_count = result_data.get('paging', {}).get('total', 0)
                print(f"  Found {projects_count} projects (out of {total_count} total)")
            except Exception as e:
                print(f"  Could not parse result: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_all_tools())