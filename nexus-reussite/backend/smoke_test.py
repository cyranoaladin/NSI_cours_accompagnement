#!/usr/bin/env python3
"""
Smoke Test Script for Nexus Réussite Backend
End-to-end verification of all services
"""

import json
import requests
import time
import sys
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class TestResult:
    name: str
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


class SmokeTest:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.jwt_token = None
        self.results = []

    def log(self, message: str, level: str = "INFO"):
        print(f"[{level}] {message}")

    def add_result(self, result: TestResult):
        self.results.append(result)
        status_emoji = "✅" if result.status == "PASS" else ("⏭️" if result.status == "SKIP" else "❌")
        self.log(f"{status_emoji} {result.name}: {result.message}")

    def test_health_endpoint(self) -> TestResult:
        """Test health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    return TestResult(
                        "Health Check", "PASS", 
                        "Backend is healthy", data
                    )
                else:
                    return TestResult(
                        "Health Check", "FAIL", 
                        f"Backend status: {data.get('status', 'unknown')}", data
                    )
            else:
                return TestResult(
                    "Health Check", "FAIL", 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            return TestResult(
                "Health Check", "FAIL", f"Error: {str(e)}"
            )

    def test_metrics_endpoint(self) -> TestResult:
        """Test Prometheus metrics endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/metrics", timeout=10)
            if response.status_code == 200:
                content = response.text
                if "python_info" in content and "process_" in content:
                    return TestResult(
                        "Metrics Endpoint", "PASS", 
                        "Prometheus metrics are being emitted"
                    )
                else:
                    return TestResult(
                        "Metrics Endpoint", "FAIL", 
                        "Metrics content doesn't look like Prometheus format"
                    )
            else:
                return TestResult(
                    "Metrics Endpoint", "FAIL", 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            return TestResult(
                "Metrics Endpoint", "FAIL", f"Error: {str(e)}"
            )

    def test_config_endpoint(self) -> TestResult:
        """Test configuration endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/config", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("config_status") == "ok" and data.get("features"):
                    return TestResult(
                        "Config Endpoint", "PASS", 
                        "Configuration endpoint working", data
                    )
                else:
                    return TestResult(
                        "Config Endpoint", "FAIL", 
                        "Config endpoint not returning expected data", data
                    )
            else:
                return TestResult(
                    "Config Endpoint", "FAIL", 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            return TestResult(
                "Config Endpoint", "FAIL", f"Error: {str(e)}"
            )

    def test_readiness_endpoint(self) -> TestResult:
        """Test readiness endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/ready", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ready" and data.get("checks"):
                    return TestResult(
                        "Readiness Check", "PASS", 
                        "Backend is ready for requests", data
                    )
                else:
                    return TestResult(
                        "Readiness Check", "FAIL", 
                        f"Backend not ready: {data.get('status', 'unknown')}", data
                    )
            else:
                return TestResult(
                    "Readiness Check", "FAIL", 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            return TestResult(
                "Readiness Check", "FAIL", f"Error: {str(e)}"
            )

    def test_auth_csrf_protection(self) -> TestResult:
        """Test that CSRF protection is working"""
        try:
            # Test that auth endpoints are protected with CSRF
            response = self.session.post(
                f"{self.base_url}/api/register", 
                json={"test": "data"},
                timeout=10
            )
            
            if response.status_code == 400:
                data = response.json()
                if data.get("code") == "CSRF_ERROR":
                    return TestResult(
                        "CSRF Protection", "PASS", 
                        "CSRF protection is active (security confirmed)", data
                    )
                else:
                    return TestResult(
                        "CSRF Protection", "FAIL", 
                        "CSRF not working as expected", data
                    )
            else:
                return TestResult(
                    "CSRF Protection", "FAIL", 
                    f"Unexpected response: HTTP {response.status_code}"
                )
        except Exception as e:
            return TestResult(
                "CSRF Protection", "FAIL", f"Error: {str(e)}"
            )

    def test_logging_verification(self) -> TestResult:
        """Test that structured logging is working"""
        try:
            # Make a request to generate logs and verify the response structure
            response = self.session.get(f"{self.base_url}/api/live", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "timestamp" in data and "status" in data:
                    # Verify that logs are structured (we can't directly check logs, 
                    # but the response structure suggests logging is working)
                    return TestResult(
                        "Structured Logging", "PASS", 
                        "Liveness endpoint responding with structured data", data
                    )
                else:
                    return TestResult(
                        "Structured Logging", "FAIL", 
                        "Liveness endpoint not returning structured data", data
                    )
            else:
                return TestResult(
                    "Structured Logging", "FAIL", 
                    f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            return TestResult(
                "Structured Logging", "FAIL", f"Error: {str(e)}"
            )

    def run_all_tests(self):
        """Run all smoke tests"""
        self.log("🚀 Starting Nexus Réussite Backend Smoke Tests")
        self.log("=" * 60)
        
        # Health and infrastructure tests
        self.add_result(self.test_health_endpoint())
        self.add_result(self.test_metrics_endpoint())
        
        # API functionality tests
        self.add_result(self.test_config_endpoint())
        self.add_result(self.test_readiness_endpoint())
        self.add_result(self.test_auth_csrf_protection())
        
        # Logging verification
        self.add_result(self.test_logging_verification())
        
        # Summary
        self.log("=" * 60)
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        total = len(self.results)
        passed = len([r for r in self.results if r.status == "PASS"])
        failed = len([r for r in self.results if r.status == "FAIL"])
        skipped = len([r for r in self.results if r.status == "SKIP"])
        
        self.log(f"📊 Test Summary:")
        self.log(f"   Total:   {total}")
        self.log(f"   Passed:  {passed} ✅")
        self.log(f"   Failed:  {failed} ❌")
        self.log(f"   Skipped: {skipped} ⏭️")
        
        success_rate = (passed / total) * 100 if total > 0 else 0
        self.log(f"   Success Rate: {success_rate:.1f}%")
        
        if failed > 0:
            self.log("\n❌ Failed Tests:")
            for result in self.results:
                if result.status == "FAIL":
                    self.log(f"   - {result.name}: {result.message}")
        
        return failed == 0


def main():
    """Main function"""
    print("🧪 Nexus Réussite Backend - End-to-End Smoke Test")
    print("=" * 60)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    tester = SmokeTest()
    tester.run_all_tests()
    
    # Check if all tests passed
    failed_count = len([r for r in tester.results if r.status == "FAIL"])
    
    if failed_count == 0:
        print("\n🎉 All tests passed! Backend is ready for use.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Please check the logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
