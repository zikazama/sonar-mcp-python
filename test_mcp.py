#!/usr/bin/env python3
"""
Test script to simulate MCP request for get_all_projects
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

async def test_mcp_request():
    """Test MCP request for get_all_projects"""
    try:
        # Initialize the MCP server
        mcp = SonarQubeMCP()
        
        # Simulate the MCP request for get_all_projects
        request = {
            "method": "tools/call",
            "params": {
                "name": "get_all_projects",
                "arguments": {
                    "page": 1,
                    "page_size": 100
                }
            }
        }
        
        print("Testing MCP request for get_all_projects...")
        print(f"Request: {json.dumps(request, indent=2)}")
        print("=" * 50)
        
        # Handle the request
        response = await mcp.handle_request(request)
        
        print("Response:")
        print(json.dumps(response, indent=2))
        
        # Check if there's an error in the response
        if "error" in response:
            print("\nERROR FOUND:")
            print(f"Code: {response['error'].get('code')}")
            print(f"Message: {response['error'].get('message')}")
            print(f"Data: {response['error'].get('data')}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_request())