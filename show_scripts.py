#!/usr/bin/env python3
"""
Script to show all available analysis scripts and how to use them
"""

import os

def show_available_scripts():
    """Show all available scripts and how to use them"""
    
    scripts = {
        "list_projects.py": {
            "description": "Lists all projects in SonarQube",
            "usage": "python list_projects.py"
        },
        "simple_list_projects.py": {
            "description": "Simple script to list all projects",
            "usage": "python simple_list_projects.py"
        },
        "get_coverage.py": {
            "description": "Gets coverage metrics for a specific project",
            "usage": "python get_coverage.py <project_key> \"<project_name>\""
        },
        "analyze_project.py": {
            "description": "Detailed analysis of any project by key",
            "usage": "python analyze_project.py <project_key> \"<project_name>\""
        },
        "analyze_projects.py": {
            "description": "Comprehensive analysis of all projects",
            "usage": "python analyze_projects.py"
        },
        "analyze_zero_coverage.py": {
            "description": "Detailed analysis of projects with 0.0% coverage",
            "usage": "python analyze_zero_coverage.py"
        },
        "top_coverage_projects.py": {
            "description": "Shows top 5 projects by code coverage",
            "usage": "python top_coverage_projects.py"
        },
        "projects_by_issues.py": {
            "description": "Shows projects sorted by number of issues",
            "usage": "python projects_by_issues.py"
        },
        "compare_projects.py": {
            "description": "Compare two projects side by side",
            "usage": "python compare_projects.py <project1_key> \"<project1_name>\" <project2_key> \"<project2_name>\""
        },
        "issues_by_severity.py": {
            "description": "Get detailed issues breakdown by severity for a project",
            "usage": "python issues_by_severity.py <project_key> \"<project_name>\""
        },
        "get_uncovered_lines.py": {
            "description": "Gets uncovered lines information for a project",
            "usage": "python get_uncovered_lines.py"
        },
        "test_health.py": {
            "description": "Tests SonarQube connection health",
            "usage": "python test_health.py"
        },
        "test_all_tools.py": {
            "description": "Tests all SonarQube MCP tools",
            "usage": "python test_all_tools.py"
        }
    }
    
    print("Available SonarQube Analysis Scripts")
    print("=" * 50)
    print()
    
    for script_name, info in scripts.items():
        if os.path.exists(script_name):
            print(f"Script: {script_name}")
            print(f"  Description: {info['description']}")
            print(f"  Usage: {info['usage']}")
            print()

if __name__ == "__main__":
    show_available_scripts()