@echo off
echo Docker Compose Configuration Usage
echo ==================================
echo.
echo 1. Development (default):
echo    docker-compose up
echo    docker-compose down
echo.
echo 2. Production:
echo    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
echo    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
echo.
echo 3. MCP Server:
echo    docker-compose -f docker-compose.mcp.yml up -d
echo    docker-compose -f docker-compose.mcp.yml down
echo.
echo 4. View logs:
echo    docker-compose logs -f
echo.
echo 5. Execute commands in container:
echo    docker-compose exec sonarqube-mcp ^<command^>
echo.
echo 6. Build images:
echo    docker-compose build
echo.
pause