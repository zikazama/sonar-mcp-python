@echo off
echo SonarQube MCP Server for Qwen
echo ==============================
echo.
echo This script starts the SonarQube MCP server for use with Qwen.
echo.

REM Check if Docker is available and the container exists
docker-compose -f docker-compose.mcp.yml ps >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Starting MCP server in Docker container...
    docker-compose -f docker-compose.mcp.yml up -d
    echo.
    echo MCP server is now running in Docker container.
    echo Configure Qwen to connect to it using the Docker exec method.
    echo.
) else (
    echo Docker not available or compose file not found.
    echo Starting MCP server directly...
    echo.
    python mcp_server.py
)

echo.
echo To stop the server, press Ctrl+C or close this window.
pause