# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set labels
LABEL maintainer="Fauzi Fadhlurrohman <https://www.linkedin.com/in/fauzi-fadhlurrohman/>"
LABEL description="SonarQube FastAPI MCP Server"

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (though MCP server uses stdin/stdout, this is for health checks)
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app

# Default command to run the MCP server
CMD ["python", "mcp_server.py"]