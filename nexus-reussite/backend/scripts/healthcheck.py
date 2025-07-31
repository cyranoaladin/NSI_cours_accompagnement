#!/usr/bin/env python3
"""
Health check script for Nexus Réussite Backend Docker container
"""

import os
from urllib.parse import urljoin

import requests


def health_check():
    """Perform health check on the application"""
    try:
        # Get the port from environment or use default
        port = os.environ.get("PORT", "8000")
        base_url = f"http://localhost:{port}"

        # Check if the main application is responding
        health_endpoint = urljoin(base_url, "/health")

        response = requests.get(health_endpoint, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Health check passed")
                return 0
            else:
                print(f"❌ Health check failed: {data}")
                return 1
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return 1

    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed with error: {e}")
        return 1
    except (RuntimeError, OSError, ValueError) as e:
        print(f"❌ Unexpected error during health check: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(health_check())
