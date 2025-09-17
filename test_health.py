#!/usr/bin/env python3
"""
Test script to verify health check with connection test
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

async def test_health_check():
    """Test health check with connection test"""
    try:
        # Initialize the MCP server
        mcp = SonarQubeMCP()
        
        # Simulate the MCP request for health_check
        request = {
            "method": "tools/call",
            "params": {
                "name": "health_check",
                "arguments": {}
            }
        }
        
        print("Testing health check with connection test...")
        print(f"Request: {json.dumps(request, indent=2)}")
        print("=" * 50)
        
        # Handle the request
        response = await mcp.handle_request(request)
        
        print("Response:")
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_health_check())