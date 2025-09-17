import asyncio
import json
from mcp_server import SonarQubeMCP

async def test_mcp():
    mcp = SonarQubeMCP()
    
    # Simulate the request that's failing
    request = {
        "method": "tools/call",
        "params": {
            "name": "get_all_projects",
            "arguments": {}
        }
    }
    
    try:
        response = await mcp.handle_request(request)
        print("Response:")
        print(json.dumps(response, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp())