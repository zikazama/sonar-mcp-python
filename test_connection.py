import asyncio
from sonarqube_service import SonarQubeService

async def test():
    service = SonarQubeService('http://localhost:8088', 'squ_f5d437fc56b7a7b8f1654a7f3515511d1e16581d')
    try:
        result = await service.get_projects()
        print("Success! Here are the projects:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())