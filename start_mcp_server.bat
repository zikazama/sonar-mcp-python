@echo off
echo Starting SonarQube MCP Server for Qwen, Cursor, and Claude
echo ========================================================
echo.
echo Make sure you have:
echo 1. Python 3.8+ installed
echo 2. Dependencies installed (pip install -r requirements.txt)
echo 3. .env file configured with your SonarQube settings
echo.
echo Starting MCP server...
echo.
python mcp_server.py
echo.
echo MCP server stopped.
pause