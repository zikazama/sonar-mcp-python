# SonarQube FastAPI MCP Server

This project provides a FastAPI-based MCP (Machine Control Protocol) server for interacting with SonarQube. It allows tools like Qwen, Cursor, and Claude to access SonarQube data through MCP protocol.

## Features

- Get all projects from SonarQube
- Retrieve coverage metrics for projects
- Get duplication rates
- Access project issues
- Obtain uncovered lines information
- Health check endpoint

## Author

**Fauzi Fadhlurrohman**
- LinkedIn: [https://www.linkedin.com/in/fauzi-fadhlurrohman/](https://www.linkedin.com/in/fauzi-fadhlurrohman/)

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env` file
4. Run the server: `python mcp_server.py`

## Docker Deployment

The project includes multiple Docker Compose configurations:

1. **Development (default)**:
   ```bash
   docker-compose up
   docker-compose down
   ```

2. **Production**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
   ```

3. **MCP Server**:
   ```bash
   docker-compose -f docker-compose.mcp.yml up -d
   docker-compose -f docker-compose.mcp.yml down
   ```

## Usage

The server implements MCP protocol and can be used with compatible AI tools like Qwen, Cursor, and Claude.# sonar-mcp-python
