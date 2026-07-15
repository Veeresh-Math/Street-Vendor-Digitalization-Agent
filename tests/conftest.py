"""
Pytest configuration for SVDA tests.
"""

import os
import sys

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Set test environment variables before any imports
os.environ.setdefault("IBM_API_KEY", "test-api-key")
os.environ.setdefault("IBM_PROJECT_ID", "test-project-id")
os.environ.setdefault("IBM_URL", "https://au-syd.ml.cloud.ibm.com")
