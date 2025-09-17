#!/usr/bin/env python3
"""
MCP Server implementation for SonarQube FastAPI
This allows Qwen, Cursor, and Claude to interact with the SonarQube data through MCP protocol
"""

import json
import asyncio
import sys
import logging
from typing import Dict, Any, List, Optional
from sonarqube_service import SonarQubeService
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Configure logging to stderr to avoid interfering with MCP protocol
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

class SonarQubeMCP:
    def __init__(self):
        self.sonarqube_url = os.getenv("SONARQUBE_URL", "http://localhost:8088")
        self.sonarqube_token = os.getenv("SONARQUBE_TOKEN", "")
        self.sonarqube_username = os.getenv("SONARQUBE_USERNAME", "")
        self.sonarqube_password = os.getenv("SONARQUBE_PASSWORD", "")
        self.service = None
        logger.info(f"SonarQubeMCP initialized with URL: {self.sonarqube_url}")
        
    async def initialize_service(self):
        """Initialize the SonarQube service with connection pooling"""
        if self.service is None:
            self.service = SonarQubeService(
                self.sonarqube_url,
                self.sonarqube_token,
                self.sonarqube_username,
                self.sonarqube_password
            )
            logger.info("SonarQubeService initialized")
        return self.service
        
    async def close_service(self):
        """Close the SonarQube service connection"""
        if self.service:
            await self.service.close()
            self.service = None
            logger.info("SonarQubeService closed")

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            
            logger.info(f"Handling request: {method} with params: {params}")
            
            # Initialize service if needed
            await self.initialize_service()
            
            if method == "initialize":
                logger.info("Initialize request received")
                return {
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "sonarqube-mcp",
                            "version": "1.0.0"
                        }
                    }
                }

            elif method == "ping":
                logger.info("Ping request received")
                return {"result": "pong"}

            elif method == "tools/list":
                logger.info("Get tools request received")
                return {
                    "result": {
                        "tools": [
                            {
                                "name": "get_all_projects",
                                "description": "Get all projects from SonarQube",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "page": {
                                            "type": "integer",
                                            "description": "Page number (default: 1)",
                                            "minimum": 1
                                        },
                                        "page_size": {
                                            "type": "integer",
                                            "description": "Number of projects per page (default: 100, max: 500)",
                                            "minimum": 1,
                                            "maximum": 500
                                        }
                                    }
                                }
                            },
                            {
                                "name": "get_coverage_metrics",
                                "description": "Get all coverage metrics for a SonarQube component",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "component_key": {
                                            "type": "string",
                                            "description": "The SonarQube component key"
                                        }
                                    },
                                    "required": ["component_key"]
                                }
                            },
                            {
                                "name": "get_overall_coverage",
                                "description": "Get overall coverage for a SonarQube component",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "component_key": {
                                            "type": "string",
                                            "description": "The SonarQube component key"
                                        }
                                    },
                                    "required": ["component_key"]
                                }
                            },
                            {
                                "name": "get_new_code_coverage",
                                "description": "Get new code coverage for a SonarQube component",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "component_key": {
                                            "type": "string",
                                            "description": "The SonarQube component key"
                                        }
                                    },
                                    "required": ["component_key"]
                                }
                            },
                            {
                                "name": "get_duplication_rate",
                                "description": "Get duplication rate for a SonarQube component",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "component_key": {
                                            "type": "string",
                                            "description": "The SonarQube component key"
                                        }
                                    },
                                    "required": ["component_key"]
                                }
                            },
                            {
                                "name": "get_uncovered_lines",
                                "description": "Get uncovered lines for a SonarQube component",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "component_key": {
                                            "type": "string",
                                            "description": "The SonarQube component key"
                                        }
                                    },
                                    "required": ["component_key"]
                                }
                            },
                            {
                                "name": "get_project_issues",
                                "description": "Get issues for a SonarQube component",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "component_key": {
                                            "type": "string",
                                            "description": "The SonarQube component key"
                                        },
                                        "types": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "Issue types to filter (CODE_SMELL, BUG, VULNERABILITY, SECURITY_HOTSPOT)"
                                        },
                                        "severities": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "Severities to filter (INFO, MINOR, MAJOR, CRITICAL, BLOCKER)"
                                        },
                                        "statuses": {
                                            "type": "array",
                                            "items": {
                                                "type": "string"
                                            },
                                            "description": "Statuses to filter (OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED)"
                                        }
                                    },
                                    "required": ["component_key"]
                                }
                            },
                            {
                                "name": "health_check",
                                "description": "Check if the SonarQube MCP server is healthy",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            }
                        ]
                    }
                }
                
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                
                logger.info(f"Call tool request: {tool_name} with args: {tool_args}")
                
                if tool_name == "get_all_projects":
                    page = tool_args.get("page", 1)
                    page_size = tool_args.get("page_size", 100)
                    
                    logger.info(f"Fetching projects - page: {page}, page_size: {page_size}")
                    try:
                        result = await self.service.get_projects(page, page_size)
                        projects_count = len(result.get('components', []))
                        logger.info(f"Successfully fetched projects: {projects_count} projects found")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result, indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
                        # Provide more detailed error information
                        error_data = {
                            "error_type": type(e).__name__,
                            "error_message": str(e),
                            "page": page,
                            "page_size": page_size
                        }
                        if hasattr(e, '__dict__'):
                            error_data["error_details"] = e.__dict__
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": error_data
                            }
                        }
                    
                elif tool_name == "get_coverage_metrics":
                    component_key = tool_args.get("component_key")
                    if not component_key:
                        logger.warning("Missing component_key for get_coverage_metrics")
                        return {
                            "error": {
                                "code": -32602,
                                "message": "Invalid params",
                                "data": "component_key is required"
                            }
                        }
                    
                    logger.info(f"Fetching coverage metrics for component: {component_key}")
                    try:
                        result = await self.service.get_coverage_metrics(component_key)
                        logger.info(f"Successfully fetched coverage metrics for component: {component_key}")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result.dict(), indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching coverage metrics: {str(e)}", exc_info=True)
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": str(e)
                            }
                        }
                        
                elif tool_name == "get_overall_coverage":
                    component_key = tool_args.get("component_key")
                    if not component_key:
                        logger.warning("Missing component_key for get_overall_coverage")
                        return {
                            "error": {
                                "code": -32602,
                                "message": "Invalid params",
                                "data": "component_key is required"
                            }
                        }
                    
                    logger.info(f"Fetching overall coverage for component: {component_key}")
                    try:
                        result = await self.service.get_overall_coverage(component_key)
                        logger.info(f"Successfully fetched overall coverage for component: {component_key}")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result.dict(), indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching overall coverage: {str(e)}", exc_info=True)
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": str(e)
                            }
                        }
                        
                elif tool_name == "get_new_code_coverage":
                    component_key = tool_args.get("component_key")
                    if not component_key:
                        logger.warning("Missing component_key for get_new_code_coverage")
                        return {
                            "error": {
                                "code": -32602,
                                "message": "Invalid params",
                                "data": "component_key is required"
                            }
                        }
                    
                    logger.info(f"Fetching new code coverage for component: {component_key}")
                    try:
                        result = await self.service.get_new_code_coverage(component_key)
                        logger.info(f"Successfully fetched new code coverage for component: {component_key}")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result.dict(), indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching new code coverage: {str(e)}", exc_info=True)
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": str(e)
                            }
                        }
                        
                elif tool_name == "get_duplication_rate":
                    component_key = tool_args.get("component_key")
                    if not component_key:
                        logger.warning("Missing component_key for get_duplication_rate")
                        return {
                            "error": {
                                "code": -32602,
                                "message": "Invalid params",
                                "data": "component_key is required"
                            }
                        }
                    
                    logger.info(f"Fetching duplication rate for component: {component_key}")
                    try:
                        result = await self.service.get_duplication_rate(component_key)
                        logger.info(f"Successfully fetched duplication rate for component: {component_key}")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result.dict(), indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching duplication rate: {str(e)}", exc_info=True)
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": str(e)
                            }
                        }
                        
                elif tool_name == "get_uncovered_lines":
                    component_key = tool_args.get("component_key")
                    if not component_key:
                        logger.warning("Missing component_key for get_uncovered_lines")
                        return {
                            "error": {
                                "code": -32602,
                                "message": "Invalid params",
                                "data": "component_key is required"
                            }
                        }
                    
                    logger.info(f"Fetching uncovered lines for component: {component_key}")
                    try:
                        result = await self.service.get_uncovered_lines(component_key)
                        logger.info(f"Successfully fetched uncovered lines for component: {component_key}")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result.dict(), indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching uncovered lines: {str(e)}", exc_info=True)
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": str(e)
                            }
                        }
                        
                elif tool_name == "get_project_issues":
                    component_key = tool_args.get("component_key")
                    if not component_key:
                        logger.warning("Missing component_key for get_project_issues")
                        return {
                            "error": {
                                "code": -32602,
                                "message": "Invalid params",
                                "data": "component_key is required"
                            }
                        }
                    
                    types = tool_args.get("types", [])
                    severities = tool_args.get("severities", [])
                    statuses = tool_args.get("statuses", [])
                    
                    logger.info(f"Fetching issues for component: {component_key}")
                    try:
                        result = await self.service.get_issues(component_key, types, severities, statuses)
                        issues_count = result.get('total', 0)
                        logger.info(f"Successfully fetched issues for component: {component_key} ({issues_count} issues)")
                        return {
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": json.dumps(result, indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        logger.error(f"Error fetching issues: {str(e)}", exc_info=True)
                        return {
                            "error": {
                                "code": -32603,
                                "message": "Internal error",
                                "data": str(e)
                            }
                        }
                        
                elif tool_name == "health_check":
                    logger.info("Health check requested")
                    try:
                        # Test SonarQube connection
                        test_result = await self.service.get_projects(page=1, page_size=1)
                        projects_count = test_result.get('paging', {}).get('total', 0)
                        health_data = {
                            "status": "healthy", 
                            "message": "SonarQube MCP server is running and connected to SonarQube",
                            "url": self.sonarqube_url,
                            "projects_count": projects_count
                        }
                        logger.info(f"Health check successful: {projects_count} projects found")
                    except Exception as e:
                        health_data = {
                            "status": "unhealthy", 
                            "message": "SonarQube MCP server is running but cannot connect to SonarQube",
                            "url": self.sonarqube_url,
                            "error": str(e)
                        }
                        logger.error(f"Health check failed: {str(e)}", exc_info=True)
                    return {
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(health_data, indent=2)
                                }
                            ]
                        }
                    }
                    
                else:
                    logger.warning(f"Unknown tool requested: {tool_name}")
                    return {
                        "error": {
                            "code": -32601,
                            "message": "Method not found",
                            "data": f"Unknown tool: {tool_name}"
                        }
                    }
                    
            else:
                logger.warning(f"Unknown method requested: {method}")
                return {
                    "error": {
                        "code": -32601,
                        "message": "Method not found",
                        "data": f"Unknown method: {method}"
                    }
                }
                
        except Exception as e:
            logger.error(f"Error handling request: {str(e)}", exc_info=True)
            return {
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }

    async def handle_notification(self, notification: Dict[str, Any]) -> None:
        """Handle MCP notifications (no response expected)"""
        method = notification.get("method")
        params = notification.get("params", {})
        
        logger.info(f"Handling notification: {method} with params: {params}")
        
        # Currently no specific notifications are handled
        # This is a placeholder for future functionality
        pass

@asynccontextmanager
async def mcp_server_context():
    """Context manager for proper resource management"""
    mcp = SonarQubeMCP()
    try:
        yield mcp
    finally:
        await mcp.close_service()

async def main():
    """Main MCP server loop"""
    async with mcp_server_context() as mcp:
        logger.info("Starting SonarQube MCP server")
        
        # Handle MCP protocol
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                    
                request = json.loads(line.strip())
                
                # Check if this is a notification (no id) or a request (has id)
                if "id" in request:
                    # Handle as request (expecting response)
                    response = await mcp.handle_request(request)
                    
                    # Add the jsonrpc version and request ID to the response
                    response["jsonrpc"] = "2.0"
                    response["id"] = request["id"]
                    
                    # Write response to stdout
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
                else:
                    # Handle as notification (no response expected)
                    await mcp.handle_notification(request)
                    
            except json.JSONDecodeError as e:
                # Handle invalid JSON
                logger.error(f"Invalid JSON received: {e}")
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}", exc_info=True)
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if "request" in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e)
                    }
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

if __name__ == "__main__":
    logger.info("SonarQube MCP server starting...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("SonarQube MCP server stopped by user")
    except Exception as e:
        logger.error(f"SonarQube MCP server error: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("SonarQube MCP server shutdown complete")
