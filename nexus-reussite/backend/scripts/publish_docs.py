#!/usr/bin/env python3
"""
Documentation Publishing Script for Nexus Réussite Backend
Generates and publishes API documentation to the docs site
"""

import os
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def setup_environment():
    """Setup environment for documentation generation"""
    # Set required environment variables for documentation generation
    os.environ['FLASK_ENV'] = 'development'
    os.environ['SECRET_KEY'] = 'doc-generation-key'
    os.environ['JWT_SECRET_KEY'] = 'doc-jwt-key'
    os.environ['DATABASE_URL'] = 'sqlite:///docs.db'  # Temporary database for docs
    os.environ['REDIS_URL'] = 'redis://localhost:6379/15'  # Use different Redis DB


def generate_api_documentation(output_dir: str = "docs/api") -> bool:
    """
    Generate comprehensive API documentation

    Args:
        output_dir: Directory to save generated documentation

    Returns:
        bool: True if successful, False otherwise
    """

    try:
        # Setup environment
        setup_environment()

        # Import after setting up environment
        from main_production import create_app
        from docs import init_api_docs

        print("🔧 Creating Flask application...")
        app = create_app()

        with app.app_context():
            print("📚 Initializing API documentation...")
            api = init_api_docs(app)

            # Ensure output directory exists
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Generate OpenAPI specification
            print("📝 Generating OpenAPI specification...")
            spec = api.__schema__

            # Add custom metadata
            spec['info']['x-generated'] = datetime.utcnow().isoformat()
            spec['info']['x-generator'] = 'Nexus Réussite Documentation Generator'

            # Save OpenAPI spec as JSON
            spec_file = Path(output_dir) / "openapi.json"
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(spec, f, indent=2, ensure_ascii=False)

            # Generate interactive HTML documentation
            print("🎨 Generating interactive HTML documentation...")
            html_content = generate_swagger_ui_html(spec)
            html_file = Path(output_dir) / "index.html"
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Generate API reference markdown
            print("📖 Generating API reference markdown...")
            markdown_content = generate_api_reference_markdown(spec)
            md_file = Path(output_dir) / "api_reference.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            # Generate Postman collection
            print("📬 Generating Postman collection...")
            postman_collection = generate_postman_collection(spec)
            postman_file = Path(output_dir) / "postman_collection.json"
            with open(postman_file, 'w', encoding='utf-8') as f:
                json.dump(postman_collection, f, indent=2)

            # Copy static assets if needed
            copy_static_assets(output_dir)

            print(f"✅ API documentation generated successfully!")
            print(f"   📁 Output directory: {output_dir}")
            print(f"   🌐 HTML documentation: {html_file}")
            print(f"   📋 OpenAPI spec: {spec_file}")
            print(f"   📖 Markdown reference: {md_file}")
            print(f"   📬 Postman collection: {postman_file}")

            return True

    except (RuntimeError, OSError, ValueError) as e:
        print(f"❌ Error generating documentation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def generate_swagger_ui_html(spec: dict) -> str:
    """Generate Swagger UI HTML with custom styling"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus Réussite Backend API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <link rel="icon" type="image/png" href="https://nexus-reussite.com/favicon.png" sizes="32x32" />
    <style>
        html {{ box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }}
        *, *:before, *:after {{ box-sizing: inherit; }}
        body {{ margin: 0; background: #fafafa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}

        .swagger-ui .topbar {{ display: none; }}
        .swagger-ui .info .title {{ color: #3b4151; font-size: 36px; margin-bottom: 10px; }}
        .swagger-ui .info .description {{ color: #3b4151; font-size: 16px; line-height: 1.6; }}

        .custom-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 0;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .custom-header h1 {{
            margin: 0;
            font-size: 2.8em;
            font-weight: 300;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}

        .custom-header p {{
            margin: 15px 0 0 0;
            font-size: 1.3em;
            opacity: 0.95;
            font-weight: 300;
        }}

        .custom-header .badges {{
            margin-top: 20px;
        }}

        .custom-header .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 20px;
            margin: 0 5px;
            font-size: 0.9em;
            border: 1px solid rgba(255,255,255,0.3);
        }}

        .jwt-token-panel {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            z-index: 1000;
            border: 1px solid #e0e0e0;
            min-width: 300px;
        }}

        .jwt-token-panel h4 {{
            margin: 0 0 10px 0;
            color: #3b4151;
            font-size: 14px;
            font-weight: 600;
        }}

        .jwt-token-panel input {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-bottom: 10px;
            font-family: monospace;
            font-size: 12px;
        }}

        .jwt-token-panel button {{
            padding: 6px 12px;
            margin-right: 5px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
        }}

        .btn-set {{ background: #667eea; color: white; }}
        .btn-clear {{ background: #f44336; color: white; }}
        .btn-test {{ background: #4caf50; color: white; }}

        .swagger-ui .scheme-container {{
            background: #fff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        @media (max-width: 768px) {{
            .jwt-token-panel {{
                position: relative;
                top: auto;
                right: auto;
                margin: 20px;
                width: calc(100% - 40px);
            }}

            .custom-header h1 {{ font-size: 2em; }}
            .custom-header p {{ font-size: 1.1em; }}
        }}
    </style>
</head>
<body>
    <div class="custom-header">
        <h1>🎓 Nexus Réussite Backend API</h1>
        <p>Intelligent Educational Platform API Documentation</p>
        <div class="badges">
            <span class="badge">Version 1.0.0</span>
            <span class="badge">OpenAPI 3.0</span>
            <span class="badge">Production Ready</span>
        </div>
    </div>

    <div class="jwt-token-panel">
        <h4>🔐 JWT Authentication</h4>
        <input type="password" id="jwt-token" placeholder="Enter your JWT token here..." />
        <div>
            <button class="btn-set" onclick="setToken()">Set Token</button>
            <button class="btn-clear" onclick="clearToken()">Clear</button>
            <button class="btn-test" onclick="testToken()">Test</button>
        </div>
        <div id="token-status" style="margin-top: 10px; font-size: 12px;"></div>
    </div>

    <div id="swagger-ui"></div>

    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                spec: {json.dumps(spec, indent=2)},
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
                requestInterceptor: function(request) {{
                    const token = localStorage.getItem('nexus_jwt_token');
                    if (token) {{
                        request.headers['Authorization'] = 'Bearer ' + token;
                    }}
                    return request;
                }},
                responseInterceptor: function(response) {{
                    updateTokenStatus(response.status);
                    return response;
                }}
            }});

            // Load existing token
            loadExistingToken();
        }};

        function setToken() {{
            const token = document.getElementById('jwt-token').value.trim();
            if (token) {{
                localStorage.setItem('nexus_jwt_token', token);
                updateTokenStatus(200, 'Token set successfully');
                // Trigger UI update
                location.reload();
            }} else {{
                updateTokenStatus(400, 'Please enter a valid token');
            }}
        }}

        function clearToken() {{
            localStorage.removeItem('nexus_jwt_token');
            document.getElementById('jwt-token').value = '';
            updateTokenStatus(null, 'Token cleared');
        }}

        function testToken() {{
            const token = localStorage.getItem('nexus_jwt_token');
            if (!token) {{
                updateTokenStatus(400, 'No token set');
                return;
            }}

            // Test token by making a request to the health endpoint
            fetch('/api/health', {{
                headers: {{
                    'Authorization': 'Bearer ' + token
                }}
            }})
            .then(response => {{
                if (response.ok) {{
                    updateTokenStatus(200, 'Token is valid');
                }} else {{
                    updateTokenStatus(response.status, 'Token validation failed');
                }}
            }})
            .catch(error => {{
                updateTokenStatus(500, 'Token test failed: ' + error.message);
            }});
        }}

        function loadExistingToken() {{
            const existingToken = localStorage.getItem('nexus_jwt_token');
            if (existingToken) {{
                document.getElementById('jwt-token').value = existingToken;
                updateTokenStatus(null, 'Token loaded from storage');
            }}
        }}

        function updateTokenStatus(status, message) {{
            const statusDiv = document.getElementById('token-status');
            if (status === 200) {{
                statusDiv.innerHTML = '<span style="color: #4caf50;">✓ ' + message + '</span>';
            }} else if (status >= 400) {{
                statusDiv.innerHTML = '<span style="color: #f44336;">✗ ' + message + '</span>';
            }} else {{
                statusDiv.innerHTML = '<span style="color: #ff9800;">ℹ ' + message + '</span>';
            }}
        }}
    </script>
</body>
</html>"""


def generate_api_reference_markdown(spec: dict) -> str:
    """Generate API reference in Markdown format"""

    md_content = f"""# Nexus Réussite Backend API Reference

Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Overview

{spec.get('info', {}).get('description', 'API Documentation')}

**Version:** {spec.get('info', {}).get('version', '1.0.0')}
**Base URL:** `/api`

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

"""

    # Add endpoint documentation
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        md_content += f"\n### {path}\n\n"

        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                md_content += f"#### {method.upper()} {path}\n\n"
                md_content += f"**Summary:** {details.get('summary', 'No summary available')}\\n\\n"

                if 'description' in details:
                    md_content += f"**Description:** {details['description']}\\n\\n"

                # Parameters
                if 'parameters' in details:
                    md_content += "**Parameters:**\\n\\n"
                    for param in details['parameters']:
                        required = " (required)" if param.get('required', False) else ""
                        md_content += f"- `{param['name']}`{required}: {param.get('description', 'No description')}\\n"
                    md_content += "\\n"

                # Response codes
                if 'responses' in details:
                    md_content += "**Responses:**\\n\\n"
                    for code, response in details['responses'].items():
                        md_content += f"- `{code}`: {response.get('description', 'No description')}\\n"
                    md_content += "\\n"

    return md_content


def generate_postman_collection(spec: dict) -> dict:
    """Generate Postman collection from OpenAPI spec"""

    collection = {
        "info": {
            "name": "Nexus Réussite Backend API",
            "description": spec.get('info', {}).get('description', ''),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {
                    "key": "token",
                    "value": "{{jwt_token}}",
                    "type": "string"
                }
            ]
        },
        "variable": [
            {
                "key": "base_url",
                "value": "http://localhost:5000/api",
                "type": "string"
            },
            {
                "key": "jwt_token",
                "value": "",
                "type": "string"
            }
        ],
        "item": []
    }

    # Convert OpenAPI paths to Postman requests
    paths = spec.get('paths', {})
    for path, methods in paths.items():
        folder = {
            "name": path.replace('/', ' ').strip(),
            "item": []
        }

        for method, details in methods.items():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                request = {
                    "name": f"{method.upper()} {path}",
                    "request": {
                        "method": method.upper(),
                        "header": [],
                        "url": {
                            "raw": "{{base_url}}" + path,
                            "host": ["{{base_url}}"],
                            "path": path.split('/')[1:]  # Remove empty first element
                        }
                    }
                }

                if details.get('summary'):
                    request['request']['description'] = details['summary']

                folder['item'].append(request)

        if folder['item']:  # Only add folders with items
            collection['item'].append(folder)

    return collection


def copy_static_assets(output_dir: str):
    """Copy static assets for documentation"""

    # Create assets directory
    assets_dir = Path(output_dir) / "assets"
    assets_dir.mkdir(exist_ok=True)

    # Create a simple favicon if it doesn't exist
    favicon_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="#667eea"/>
        <text x="50" y="60" text-anchor="middle" fill="white" font-size="40" font-family="Arial">N</text>
    </svg>"""

    favicon_file = assets_dir / "favicon.svg"
    with open(favicon_file, 'w') as f:
        f.write(favicon_content)


def publish_to_github_pages(docs_dir: str, branch: str = "gh-pages") -> bool:
    """
    Publish documentation to GitHub Pages

    Args:
        docs_dir: Directory containing generated documentation
        branch: GitHub Pages branch name

    Returns:
        bool: True if successful, False otherwise
    """

    try:
        import subprocess

        # Check if we're in a git repository
        result = subprocess.run(['git', 'rev-parse', '--git-dir'],
                              capture_output=True, text=True, check=False)
        if result.returncode != 0:
            print("❌ Not in a git repository")
            return False

        # Create or switch to GitHub Pages branch
        print(f"🌿 Switching to {branch} branch...")
        subprocess.run(['git', 'checkout', '-B', branch], check=True, check=False)

        # Copy documentation files
        print("📁 Copying documentation files...")
        for item in Path(docs_dir).iterdir():
            if item.is_file():
                shutil.copy2(item, '.')
            else:
                shutil.copytree(item, item.name, dirs_exist_ok=True)

        # Commit and push
        print("📤 Committing and pushing to GitHub...")
        subprocess.run(['git', 'add', '.'], check=True, check=False)
        subprocess.run(['git', 'commit', '-m', f'Update API documentation - {datetime.utcnow(, check=False).isoformat()}'], check=True)
        subprocess.run(['git', 'push', 'origin', branch], check=True, check=False)

        print(f"✅ Documentation published to GitHub Pages!")
        print(f"   🌐 Available at: https://your-username.github.io/your-repo/")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False
    except (RuntimeError, OSError, ValueError) as e:
        print(f"❌ Publishing failed: {e}")
        return False


def main():
    """Main function for the documentation publishing script"""

    parser = argparse.ArgumentParser(description='Generate and publish API documentation')
    parser.add_argument('--output', '-o', default='docs/api',
                       help='Output directory for documentation')
    parser.add_argument('--publish', '-p', action='store_true',
                       help='Publish to GitHub Pages')
    parser.add_argument('--branch', '-b', default='gh-pages',
                       help='GitHub Pages branch name')

    args = parser.parse_args()

    print("🚀 Starting documentation generation...")

    # Generate documentation
    success = generate_api_documentation(args.output)

    if not success:
        print("❌ Documentation generation failed!")
        sys.exit(1)

    # Publish if requested
    if args.publish:
        print("\\n📤 Publishing to GitHub Pages...")
        publish_success = publish_to_github_pages(args.output, args.branch)

        if not publish_success:
            print("❌ Publishing failed!")
            sys.exit(1)

    print("\\n🎉 Documentation process completed successfully!")


if __name__ == "__main__":
    main()
