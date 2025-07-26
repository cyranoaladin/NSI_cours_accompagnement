"""
Security testing using OWASP ZAP for automated security scanning.
"""

import time
from urllib.parse import urljoin

import pytest
from zapv2 import ZAPv2


class TestSecurityScanning:
    """
    OWASP ZAP automated security testing suite.
    """

    @pytest.fixture(scope="class")
    def zap_client(self):
        """Initialize ZAP client."""
        # ZAP should be running on localhost:8080
        # Start with: zap.sh -daemon -port 8080 -config api.disablekey=true
        zap = ZAPv2(
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
        )

        # Clear any existing sessions
        zap.core.new_session()

        yield zap

        # Cleanup
        zap.core.shutdown()

    @pytest.fixture
    def target_url(self):
        """Base URL for testing."""
        return "http://localhost:5000"

    def test_passive_scan_api_endpoints(self, zap_client, target_url):
        """
        Perform passive security scanning on API endpoints.
        """
        # List of endpoints to test
        endpoints = [
            "/api/auth/login",
            "/api/auth/register",
            "/api/users/profile",
            "/api/aria/chat",
            "/api/exercises",
            "/api/documents",
        ]

        # Access each endpoint to populate ZAP's site tree
        for endpoint in endpoints:
            full_url = urljoin(target_url, endpoint)
            try:
                zap_client.urlopen(full_url)
                time.sleep(1)  # Give ZAP time to process
            except Exception as e:
                print(f"Failed to access {full_url}: {e}")

        # Wait for passive scan to complete
        time.sleep(5)

        # Get passive scan results
        alerts = zap_client.core.alerts(baseurl=target_url)

        # Filter out low-priority alerts for CI
        critical_alerts = [
            alert for alert in alerts if alert["risk"] in ["High", "Medium"]
        ]

        # Assert no critical security issues
        assert (
            len(critical_alerts) == 0
        ), f"Security vulnerabilities found: {critical_alerts}"

    def test_authentication_security(self, zap_client, target_url):
        """
        Test authentication-related security vulnerabilities.
        """
        auth_url = urljoin(target_url, "/api/auth/login")

        # Test with various authentication payloads
        test_payloads = [
            {"email": "admin", "password": "admin"},
            {"email": "test@example.com", "password": ""},
            {"email": "", "password": "password"},
            {"email": "test@example.com", "password": "' OR '1'='1"},
        ]

        for payload in test_payloads:
            try:
                zap_client.urlopen(auth_url, postdata=str(payload))
                time.sleep(0.5)
            except Exception:
                pass  # Expected for invalid payloads

        # Check for authentication-related vulnerabilities
        alerts = zap_client.core.alerts(baseurl=auth_url)
        auth_vulnerabilities = [
            alert
            for alert in alerts
            if "authentication" in alert["name"].lower()
            or "password" in alert["name"].lower()
            or "injection" in alert["name"].lower()
        ]

        high_risk_auth = [
            alert for alert in auth_vulnerabilities if alert["risk"] == "High"
        ]

        assert (
            len(high_risk_auth) == 0
        ), f"High-risk auth vulnerabilities: {high_risk_auth}"

    def test_sql_injection_scanning(self, zap_client, target_url):
        """
        Test for SQL injection vulnerabilities.
        """
        # Enable active SQL injection scanner
        zap_client.ascan.enable_scanners("40018,40019,40020,40021")

        # Target URLs that might be vulnerable to SQL injection
        test_urls = [
            f"{target_url}/api/exercises?subject=math&grade_level=terminal",
            f"{target_url}/api/users/profile?id=1",
            f"{target_url}/api/documents?search=test",
        ]

        for url in test_urls:
            # Perform active scan
            scan_id = zap_client.ascan.scan(url)

            # Wait for scan to complete (timeout after 2 minutes)
            timeout = 120
            while int(zap_client.ascan.status(scan_id)) < 100 and timeout > 0:
                time.sleep(2)
                timeout -= 2

        # Check for SQL injection alerts
        alerts = zap_client.core.alerts()
        sql_injection_alerts = [
            alert
            for alert in alerts
            if "sql" in alert["name"].lower() and alert["risk"] in ["High", "Medium"]
        ]

        assert (
            len(sql_injection_alerts) == 0
        ), f"SQL injection vulnerabilities: {sql_injection_alerts}"

    def test_xss_vulnerabilities(self, zap_client, target_url):
        """
        Test for Cross-Site Scripting (XSS) vulnerabilities.
        """
        # Enable XSS scanners
        zap_client.ascan.enable_scanners("40012,40014,40016,40017")

        # Test XSS on endpoints that accept user input
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
        ]

        test_endpoints = [
            "/api/aria/chat",
            "/api/exercises/generate",
            "/api/users/profile",
        ]

        for endpoint in test_endpoints:
            full_url = urljoin(target_url, endpoint)
            for payload in xss_payloads:
                try:
                    # Test different parameter injection points
                    test_data = {
                        "message": payload,
                        "content": payload,
                        "title": payload,
                    }
                    zap_client.urlopen(full_url, postdata=str(test_data))
                    time.sleep(0.5)
                except Exception:
                    pass

        # Check for XSS alerts
        alerts = zap_client.core.alerts(baseurl=target_url)
        xss_alerts = [
            alert
            for alert in alerts
            if "cross site scripting" in alert["name"].lower()
            or "xss" in alert["name"].lower()
        ]

        high_risk_xss = [alert for alert in xss_alerts if alert["risk"] == "High"]
        assert (
            len(high_risk_xss) == 0
        ), f"High-risk XSS vulnerabilities: {high_risk_xss}"

    def test_security_headers(self, zap_client, target_url):
        """
        Test for proper security headers implementation.
        """
        # Access main endpoints
        endpoints = ["/api/auth/login", "/api/users/profile", "/api/aria/chat"]

        for endpoint in endpoints:
            full_url = urljoin(target_url, endpoint)
            zap_client.urlopen(full_url)
            time.sleep(0.5)

        # Check for missing security headers
        alerts = zap_client.core.alerts(baseurl=target_url)
        header_alerts = [
            alert
            for alert in alerts
            if "header" in alert["name"].lower() and alert["risk"] in ["Medium", "High"]
        ]

        # Allow some medium-risk header issues but no high-risk
        high_risk_headers = [
            alert for alert in header_alerts if alert["risk"] == "High"
        ]
        assert (
            len(high_risk_headers) == 0
        ), f"Critical header security issues: {high_risk_headers}"

    def test_information_disclosure(self, zap_client, target_url):
        """
        Test for information disclosure vulnerabilities.
        """
        # Test various endpoints for information leakage
        sensitive_endpoints = [
            "/api/admin/users",
            "/api/admin/metrics",
            "/api/debug/info",
            "/.env",
            "/config",
            "/api/internal",
        ]

        for endpoint in sensitive_endpoints:
            full_url = urljoin(target_url, endpoint)
            try:
                zap_client.urlopen(full_url)
                time.sleep(0.5)
            except Exception:
                pass  # Expected for protected endpoints

        # Check for information disclosure
        alerts = zap_client.core.alerts(baseurl=target_url)
        disclosure_alerts = [
            alert
            for alert in alerts
            if "information disclosure" in alert["name"].lower()
            or "directory browsing" in alert["name"].lower()
            or "debug" in alert["name"].lower()
        ]

        high_risk_disclosure = [
            alert for alert in disclosure_alerts if alert["risk"] == "High"
        ]

        assert (
            len(high_risk_disclosure) == 0
        ), f"Information disclosure issues: {high_risk_disclosure}"

    def test_csrf_protection(self, zap_client, target_url):
        """
        Test for CSRF protection on state-changing operations.
        """
        # Test state-changing endpoints
        csrf_test_endpoints = [
            ("/api/users/profile", "PUT"),
            ("/api/exercises", "POST"),
            ("/api/documents", "POST"),
            ("/api/auth/logout", "POST"),
        ]

        for endpoint, method in csrf_test_endpoints:
            full_url = urljoin(target_url, endpoint)
            try:
                if method == "POST":
                    zap_client.urlopen(full_url, postdata="test=data")
                elif method == "PUT":
                    zap_client.urlopen(full_url, postdata="test=data")
                time.sleep(0.5)
            except Exception:
                pass

        # Check for CSRF alerts
        alerts = zap_client.core.alerts(baseurl=target_url)
        csrf_alerts = [
            alert
            for alert in alerts
            if "csrf" in alert["name"].lower()
            or "cross-site request forgery" in alert["name"].lower()
        ]

        # CSRF protection should be in place for all state-changing operations
        high_risk_csrf = [alert for alert in csrf_alerts if alert["risk"] == "High"]
        assert len(high_risk_csrf) == 0, f"CSRF vulnerabilities: {high_risk_csrf}"
