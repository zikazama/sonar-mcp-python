# Qwen Integration Guide for SonarQube MCP Server

This guide explains how to configure Qwen to use the SonarQube MCP server to access code quality metrics and project information.

## Prerequisites

1. Qwen Chat or Qwen Code installed
2. Docker Desktop (if using containerized version) or Python 3.8+ (if running directly)
3. SonarQube instance running and accessible

## Integration Methods

You can integrate the MCP server with Qwen using either:

### Option 1: Using Docker Container (Recommended)

If you've already built and started the Docker container:

1. Ensure the container is running:
   ```bash
   docker-compose -f docker-compose.mcp.yml ps
   ```

2. The MCP server is accessible through Docker's stdin/stdout interface.

### Option 2: Running Directly

If you prefer to run the server directly without Docker:

1. Make sure dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the MCP server:
   ```bash
   python mcp_server.py
   ```

## Configuring Qwen

### Step 1: Access Qwen Settings

1. Open Qwen Chat or Qwen Code
2. Navigate to Settings (usually accessible via the gear icon or through the main menu)
3. Look for "Tools" or "MCP Servers" or "Custom Tools" section

### Step 2: Add MCP Server Configuration

Add a new MCP server with the following configuration:

**If using Docker:**
- **Name**: SonarQube MCP
- **Description**: SonarQube FastAPI MCP Server for Qwen
- **Command**: docker-compose
- **Arguments**: ["-f", "docker-compose.mcp.yml", "exec", "-T", "sonarqube-mcp", "python", "mcp_server.py"]
- **Working Directory**: Path to your sonarqube-fastapi-mcp directory

**If running directly:**
- **Name**: SonarQube MCP
- **Description**: SonarQube FastAPI MCP Server for Qwen
- **Command**: python
- **Arguments**: ["mcp_server.py"]
- **Working Directory**: Path to your sonarqube-fastapi-mcp directory

### Step 3: Verify Connection

Once configured, Qwen should automatically discover the available tools. You can test the connection by asking Qwen to use one of the SonarQube tools.

## Available Tools

The SonarQube MCP server provides the following tools for Qwen:

1. **get_all_projects** - Get all projects from SonarQube
   - Parameters: 
     - `page` (integer, optional): Page number (default: 1)
     - `page_size` (integer, optional): Number of projects per page (default: 100, max: 500)

2. **get_coverage_metrics** - Get all coverage metrics for a component
   - Parameters:
     - `component_key` (string, required): The SonarQube component key

3. **get_overall_coverage** - Get overall coverage for a component
   - Parameters:
     - `component_key` (string, required): The SonarQube component key

4. **get_new_code_coverage** - Get new code coverage for a component
   - Parameters:
     - `component_key` (string, required): The SonarQube component key

5. **get_duplication_rate** - Get duplication rate for a component
   - Parameters:
     - `component_key` (string, required): The SonarQube component key

6. **get_uncovered_lines** - Get uncovered lines for a component
   - Parameters:
     - `component_key` (string, required): The SonarQube component key

7. **get_project_issues** - Get issues for a SonarQube component
   - Parameters:
     - `component_key` (string, required): The SonarQube component key
     - `types` (array of strings, optional): Issue types to filter
     - `severities` (array of strings, optional): Severities to filter
     - `statuses` (array of strings, optional): Statuses to filter

8. **health_check** - Check if the SonarQube MCP server is healthy
   - Parameters: None

## Example Qwen Prompts

Once configured, you can ask Qwen questions like:

- "What projects are in my SonarQube instance?"
- "List all projects in SonarQube"
- "What is the overall coverage for jatis_coster_contact_export?"
- "Check the new code coverage for jatis_coster_contact_export"
- "Get all coverage metrics for jatis_coster_contact_export"
- "What is the duplication rate for jatis_coster_contact_export?"
- "How many lines are uncovered in jatis_coster_contact_export?"
- "Show me critical issues in jatis_coster_contact_export"
- "What bugs are in jatis_coster_contact_export?"
- "Check if the SonarQube MCP server is healthy"

Qwen will automatically use the appropriate MCP tool to fetch the data from SonarQube.

## Troubleshooting

### Common Issues

1. **Connection refused**: Make sure the MCP server is running before asking Qwen to use any tools.

2. **Tools not appearing**: Verify that the MCP server started correctly and that Qwen is pointing to the correct directory.

3. **Authorization errors**: Check that your SonarQube token in the `.env` file is correct and has the necessary permissions.

4. **Component not found**: Verify that the component key you're using exists in your SonarQube instance.

### Checking Server Logs

If you're experiencing issues, check the logs:

**For Docker:**
```bash
docker-compose -f docker-compose.mcp.yml logs
```

**For direct execution:**
Check the terminal where you started the MCP server.

### Restarting the Server

If you make changes to the configuration or code, you'll need to restart the MCP server:

**For Docker:**
```bash
docker-compose -f docker-compose.mcp.yml restart
```

**For direct execution:**
1. Stop the server by pressing Ctrl+C in the terminal
2. Start it again with `python mcp_server.py`

## Updating the Configuration

If you need to modify the available tools or their schemas, you can edit the configuration files:
- `qwen-mcp-config.json` - Basic configuration for Qwen
- `mcp-server.json` - Detailed tool schemas

After making changes, restart both the MCP server and Qwen to ensure the changes take effect.