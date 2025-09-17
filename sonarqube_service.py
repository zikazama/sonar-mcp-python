from fastapi import HTTPException
import httpx
import os
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

class SonarQubeMeasure(BaseModel):
    metric: str
    value: str
    bestValue: Optional[bool] = None

class SonarQubeComponent(BaseModel):
    key: str
    name: str
    qualifier: str
    measures: List[SonarQubeMeasure]

class SonarQubeResponse(BaseModel):
    component: SonarQubeComponent

class SonarQubeProject(BaseModel):
    key: str
    name: str
    qualifier: str
    visibility: str
    lastAnalysisDate: Optional[str] = None

class SonarQubeProjectsResponse(BaseModel):
    components: List[SonarQubeProject]
    paging: Dict[str, Any]

class CoverageMetricsResponse(BaseModel):
    overall_coverage: Optional[str] = None
    new_code_coverage: Optional[str] = None
    duplication_rate: Optional[str] = None
    uncovered_lines: Optional[str] = None
    component_key: str
    component_name: str

class SingleMetricResponse(BaseModel):
    component_key: str
    component_name: str
    metric: str
    value: Optional[str] = None

class SonarQubeService:
    def __init__(self, base_url: str, token: str = "", username: str = "", password: str = ""):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.username = username
        self.password = password
        
        # Create HTTP client with connection pooling and optimized settings
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=5,
                keepalive_expiry=30.0
            ),
            follow_redirects=True
        )
        
        logger.info(f"SonarQubeService initialized with URL: {self.base_url}")
        
    async def get_component_measures(
        self, 
        component_key: str, 
        metric_keys: List[str],
        branch: Optional[str] = None,
        pull_request: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get measures for a specific component from SonarQube
        
        Args:
            component_key: The key of the component in SonarQube
            metric_keys: List of metric keys to retrieve
            branch: Branch name (optional)
            pull_request: Pull request ID (optional)
        """
        url = f"{self.base_url}/api/measures/component"
        
        # Prepare query parameters
        params = {
            "component": component_key,
            "metricKeys": ",".join(metric_keys)
        }
        
        # Add optional parameters
        if branch:
            params["branch"] = branch
        if pull_request:
            params["pullRequest"] = pull_request
            
        # Prepare authentication
        auth = None
        if self.token:
            # SonarQube uses token as username with empty password
            auth = (self.token, "")
        elif self.username and self.password:
            # Use basic authentication with username and password
            auth = (self.username, self.password)
            
        try:
            logger.debug(f"Making request to SonarQube API: {url} with params: {params}")
            response = await self.client.get(
                url, 
                params=params, 
                auth=auth
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            logger.debug(f"Successfully retrieved measures for component: {component_key}")
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} when fetching measures for {component_key}: {e.response.text}")
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Component '{component_key}' not found in SonarQube"
                )
            elif e.response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized: Invalid or missing SonarQube token"
                )
            else:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"SonarQube API error: {e.response.text}"
                )
        except httpx.RequestError as e:
            logger.error(f"Network error when connecting to SonarQube for component {component_key}: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to SonarQube: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error when fetching measures for component {component_key}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
    
    async def get_projects(self, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """
        Get list of all projects from SonarQube
        
        Args:
            page: Page number (default: 1)
            page_size: Number of projects per page (default: 100, max: 500)
        """
        url = f"{self.base_url}/api/components/search"
        
        # Prepare query parameters
        params = {
            "qualifiers": "TRK",  # TRK = Projects
            "p": page,
            "ps": min(page_size, 500)  # Max 500 per page
        }
        
        # Prepare authentication
        auth = None
        if self.token:
            auth = (self.token, "")
        elif self.username and self.password:
            auth = (self.username, self.password)
            
        try:
            logger.debug(f"Making request to SonarQube API: {url} with params: {params}")
            response = await self.client.get(
                url,
                params=params,
                auth=auth
            )
            
            response.raise_for_status()
            logger.debug("Successfully retrieved projects list")
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} when fetching projects: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"SonarQube API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Network error when connecting to SonarQube for projects: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to SonarQube: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error when fetching projects: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
    
    async def get_coverage_metrics(self, component_key: str) -> CoverageMetricsResponse:
        """
        Get specific coverage metrics for a component
        """
        # Define the metrics we want to retrieve
        coverage_metrics = [
            "coverage",           # Overall coverage
            "new_coverage",       # New code coverage
            "duplicated_lines_density",  # Duplication rate
            "uncovered_lines"     # Uncovered lines
        ]
        
        try:
            logger.debug(f"Fetching coverage metrics for component: {component_key}")
            # Get the measures from SonarQube
            data = await self.get_component_measures(component_key, coverage_metrics)
            
            # Extract metrics from the response
            measures = data.get("component", {}).get("measures", [])
            metrics_dict = {}
            
            # Safely extract metric values
            for measure in measures:
                metric_key = measure.get("metric")
                metric_value = measure.get("value")
                if metric_key is not None:  # Allow empty string values but not None
                    metrics_dict[metric_key] = metric_value
            
            # Create response with the specific metrics
            result = CoverageMetricsResponse(
                overall_coverage=metrics_dict.get("coverage"),
                new_code_coverage=metrics_dict.get("new_coverage"),
                duplication_rate=metrics_dict.get("duplicated_lines_density"),
                uncovered_lines=metrics_dict.get("uncovered_lines"),
                component_key=data.get("component", {}).get("key", ""),
                component_name=data.get("component", {}).get("name", "")
            )
            
            logger.debug(f"Successfully retrieved coverage metrics for component: {component_key}")
            return result
            
        except Exception as e:
            logger.error(f"Error retrieving coverage metrics for {component_key}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving coverage metrics: {str(e)}"
            )
    
    async def get_single_metric(self, component_key: str, metric_key: str) -> SingleMetricResponse:
        """
        Get a single metric for a component
        """
        try:
            logger.debug(f"Fetching metric '{metric_key}' for component: {component_key}")
            # Get the measure from SonarQube
            data = await self.get_component_measures(component_key, [metric_key])
            
            # Extract the metric from the response
            measures = data.get("component", {}).get("measures", [])
            value = None
            if measures and len(measures) > 0 and "value" in measures[0]:
                value = measures[0]["value"]
            
            # Create response with the metric
            result = SingleMetricResponse(
                component_key=data.get("component", {}).get("key", ""),
                component_name=data.get("component", {}).get("name", ""),
                metric=metric_key,
                value=value
            )
            
            logger.debug(f"Successfully retrieved metric '{metric_key}' for component: {component_key}")
            return result
            
        except Exception as e:
            logger.error(f"Error retrieving metric '{metric_key}' for component {component_key}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving metric '{metric_key}': {str(e)}"
            )
    
    async def get_overall_coverage(self, component_key: str) -> SingleMetricResponse:
        """
        Get overall coverage for a component
        """
        return await self.get_single_metric(component_key, "coverage")
    
    async def get_new_code_coverage(self, component_key: str) -> SingleMetricResponse:
        """
        Get new code coverage for a component
        """
        return await self.get_single_metric(component_key, "new_coverage")
    
    async def get_duplication_rate(self, component_key: str) -> SingleMetricResponse:
        """
        Get duplication rate for a component
        """
        return await self.get_single_metric(component_key, "duplicated_lines_density")
    
    async def get_uncovered_lines(self, component_key: str) -> SingleMetricResponse:
        """
        Get uncovered lines for a component
        """
        return await self.get_single_metric(component_key, "uncovered_lines")
    
    async def get_available_metrics(self) -> Dict[str, Any]:
        """
        Get list of available metrics from SonarQube
        """
        url = f"{self.base_url}/api/metrics/search"
        
        # Prepare authentication
        auth = None
        if self.token:
            auth = (self.token, "")
        elif self.username and self.password:
            auth = (self.username, self.password)
            
        try:
            logger.debug(f"Making request to SonarQube API: {url}")
            response = await self.client.get(
                url,
                auth=auth
            )
            
            response.raise_for_status()
            logger.debug("Successfully retrieved available metrics")
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} when fetching metrics: {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"SonarQube API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Network error when connecting to SonarQube for metrics: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to SonarQube: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error when fetching metrics: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )
    
    async def close(self):
        """Close the HTTP client"""
        if self.client:
            await self.client.aclose()
            logger.info("SonarQubeService HTTP client closed")
        
    async def get_issues(self, component_key: str, types: List[str] = None, severities: List[str] = None, statuses: List[str] = None) -> Dict[str, Any]:
        """
        Get issues for a component
        
        Args:
            component_key: The key of the component in SonarQube
            types: Issue types to filter (CODE_SMELL, BUG, VULNERABILITY, SECURITY_HOTSPOT)
            severities: Severities to filter (INFO, MINOR, MAJOR, CRITICAL, BLOCKER)
            statuses: Statuses to filter (OPEN, CONFIRMED, REOPENED, RESOLVED, CLOSED)
        """
        url = f"{self.base_url}/api/issues/search"
        
        # Prepare query parameters
        params = {
            "componentKeys": component_key
        }
        
        # Add optional filters
        if types:
            params["types"] = ",".join(types)
        if severities:
            params["severities"] = ",".join(severities)
        if statuses:
            params["statuses"] = ",".join(statuses)
            
        # Prepare authentication
        auth = None
        if self.token:
            auth = (self.token, "")
        elif self.username and self.password:
            auth = (self.username, self.password)
            
        try:
            logger.debug(f"Making request to SonarQube API: {url} with params: {params}")
            response = await self.client.get(
                url,
                params=params,
                auth=auth
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            logger.debug(f"Successfully retrieved issues for component: {component_key}")
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code} when fetching issues for {component_key}: {e.response.text}")
            if e.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Component '{component_key}' not found in SonarQube"
                )
            elif e.response.status_code == 401:
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized: Invalid or missing SonarQube token"
                )
            else:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"SonarQube API error: {e.response.text}"
                )
        except httpx.RequestError as e:
            logger.error(f"Network error when connecting to SonarQube for issues {component_key}: {str(e)}")
            raise HTTPException(
                status_code=503,
                detail=f"Error connecting to SonarQube: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error when fetching issues for component {component_key}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )