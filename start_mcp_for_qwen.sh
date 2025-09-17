#!/bin/bash

echo "SonarQube MCP Server for Qwen"
echo "=============================="
echo
echo "This script starts the SonarQube MCP server for use with Qwen."
echo

# Check if Docker is available and the container exists
if command -v docker-compose &> /dev/null && [ -f "docker-compose.mcp.yml" ]; then
    echo "Starting MCP server in Docker container..."
    docker-compose -f docker-compose.mcp.yml up -d
    echo
    echo "MCP server is now running in Docker container."
    echo "Configure Qwen to connect to it using the Docker exec method."
    echo
else
    echo "Docker not available or compose file not found."
    echo "Starting MCP server directly..."
    echo
    python3 mcp_server.py
fi

echo
echo "To stop the server, press Ctrl+C or close this window."