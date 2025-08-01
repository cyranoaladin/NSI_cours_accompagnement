"""
API Documentation Integration Script
Integrates Flask-RestX documentation with the main application
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields, Namespace

def integrate_api_docs(app: Flask) -> Api:
    """
    Integrate comprehensive API documentation with the Flask application

    Args:
        app: Flask application instance

    Returns:
        Api: Configured Flask-RestX API instance with full documentation
    """

    # Import the documentation module
    from ..src.docs import init_api_docs

    # Initialize API documentation
    api = init_api_docs(app)

    # Add documentation route
    @app.route('/api/docs/export')
    def export_api_docs():
        """Export API documentation as JSON"""
        try:
            # Get the OpenAPI specification
            spec = api.__schema__

            # Add metadata
            export_data = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "api_version": "1.0.0",
                "export_format": "openapi-3.0.0",
                "specification": spec
            }

            return export_data, 200, {'Content-Type': 'application/json'}

        except (RuntimeError, OSError, ValueError) as e:
            return {"error": "Failed to export API documentation", "message": str(e)}, 500

    return api


def generate_static_docs(app: Flask, output_dir: str = "docs/api"):
    """
    Generate static API documentation files

    Args:
        app: Flask application instance
        output_dir: Directory to save generated documentation
    """

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate OpenAPI specification
    with app.app_context():
        from ..src.docs import init_api_docs
        api = init_api_docs(app)

        # Export OpenAPI spec
        spec = api.__schema__

        # Save as JSON
        spec_file = os.path.join(output_dir, "openapi.json")
        with open(spec_file, 'w', encoding='utf-8') as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

        # Generate HTML documentation
        html_content = generate_html_docs(spec)
        html_file = os.path.join(output_dir, "index.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ API documentation generated in {output_dir}/")
        print(f"   - OpenAPI spec: {spec_file}")
        print(f"   - HTML docs: {html_file}")


def generate_html_docs(spec: Dict[str, Any]) -> str:
    """
    Generate HTML documentation from OpenAPI specification

    Args:
        spec: OpenAPI specification dictionary

    Returns:
        str: HTML content for documentation
    """

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Réussite Backend API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css" />
    <style>
        html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
        *, *:before, *:after { box-sizing: inherit; }
        body { margin:0; background: #fafafa; }
        .swagger-ui .topbar { display: none; }
        .swagger-ui .info .title { color: #3b4151; font-size: 36px; }
        .swagger-ui .info .description { color: #3b4151; font-size: 16px; line-height: 1.6; }
        .custom-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 0;
            text-align: center;
            margin-bottom: 20px;
        }
        .custom-header h1 { margin: 0; font-size: 2.5em; font-weight: 300; }
        .custom-header p { margin: 10px 0 0 0; font-size: 1.2em; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="custom-header">
        <h1>🎓 Nexus Réussite Backend API</h1>
        <p>Intelligent Educational Platform API Documentation</p>
    </div>

    <div id="swagger-ui"></div>

    <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                spec: """ + json.dumps(spec) + """,
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null,
                supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                docExpansion: 'list',
                operationsSorter: 'alpha',
                tagsSorter: 'alpha',
                filter: true,
                tryItOutEnabled: true,
                requestInterceptor: function(request) {
                    // Add authorization header if token is available
                    const token = localStorage.getItem('jwt_token');
                    if (token) {
                        request.headers['Authorization'] = 'Bearer ' + token;
                    }
                    return request;
                }
            });

            // Add custom functionality for JWT token management
            const tokenInput = document.createElement('div');
            tokenInput.innerHTML = `
                <div style="position: fixed; top: 10px; right: 10px; background: white; padding: 10px; border: 1px solid #ccc; border-radius: 5px; z-index: 1000;">
                    <label for="jwt-token">JWT Token:</label>
                    <input type="password" id="jwt-token" placeholder="Enter JWT token" style="margin-left: 10px; padding: 5px;">
                    <button onclick="setToken()" style="margin-left: 5px; padding: 5px 10px;">Set</button>
                    <button onclick="clearToken()" style="margin-left: 5px; padding: 5px 10px;">Clear</button>
                </div>
            `;
            document.body.appendChild(tokenInput);

            window.setToken = function() {
                const token = document.getElementById('jwt-token').value;
                if (token) {
                    localStorage.setItem('jwt_token', token);
                    alert('JWT token set successfully!');
                }
            };

            window.clearToken = function() {
                localStorage.removeItem('jwt_token');
                document.getElementById('jwt-token').value = '';
                alert('JWT token cleared!');
            };

            // Load existing token
            const existingToken = localStorage.getItem('jwt_token');
            if (existingToken) {
                document.getElementById('jwt-token').value = existingToken;
            }
        };
    </script>
</body>
</html>
    """

    return html_template


if __name__ == "__main__":
    # Generate static documentation
    from ..src.main_production import create_app

    app = create_app()
    generate_static_docs(app)
