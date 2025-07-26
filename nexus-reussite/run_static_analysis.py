#!/usr/bin/env python3
"""
Static Code Analysis Automation Script
Step 3: Static code analysis & style compliance

This script runs comprehensive static analysis tools for both backend (Python)
and frontend (JavaScript/TypeScript) code and generates HTML reports.

Tools used:
Backend: pylint, flake8, black --check, mypy, bandit, safety
Frontend: eslint --max-warnings 0, prettier --check, tsc --noEmit, depcheck
"""

import subprocess
import json
import html
import datetime
import os
import sys
from pathlib import Path
from collections import defaultdict


class StaticAnalysisRunner:
    def __init__(self):
        self.report_dir = Path("docs/audit/static_analysis")
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.backend_dir = Path("backend")
        self.frontend_dir = Path("frontend")
        self.results = {}
        self.violation_matrix = defaultdict(lambda: defaultdict(int))
        
    def run_command(self, cmd, cwd=None, capture_output=True):
        """Run a shell command and return the result."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                timeout=300
            )
            return {
                'cmd': cmd,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                'cmd': cmd,
                'returncode': -1,
                'stdout': '',
                'stderr': 'Command timed out',
                'success': False
            }
        except Exception as e:
            return {
                'cmd': cmd,
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }

    def analyze_backend(self):
        """Run Python static analysis tools."""
        print("🐍 Running Backend Static Analysis...")
        backend_results = {}
        
        # Create src path for analysis
        src_path = self.backend_dir / "src"
        
        # 1. Pylint
        print("  Running pylint...")
        pylint_result = self.run_command(
            f"pylint --output-format=json --score=yes {src_path} --disable=import-error,no-member",
            cwd="."
        )
        backend_results['pylint'] = pylint_result
        
        # 2. Flake8
        print("  Running flake8...")
        flake8_result = self.run_command(
            f"flake8 --format=json {src_path} --max-line-length=88 --extend-ignore=E203,W503",
            cwd="."
        )
        backend_results['flake8'] = flake8_result
        
        # 3. Black check
        print("  Running black --check...")
        black_result = self.run_command(
            f"black --check --diff {src_path}",
            cwd="."
        )
        backend_results['black'] = black_result
        
        # 4. MyPy
        print("  Running mypy...")
        mypy_result = self.run_command(
            f"mypy {src_path} --ignore-missing-imports --json-report mypy_report",
            cwd="."
        )
        backend_results['mypy'] = mypy_result
        
        # 5. Bandit
        print("  Running bandit...")
        bandit_result = self.run_command(
            f"bandit -r {src_path} -f json -o bandit_report.json",
            cwd="."
        )
        backend_results['bandit'] = bandit_result
        
        # 6. Safety
        print("  Running safety...")
        safety_result = self.run_command(
            f"safety check --json --file {self.backend_dir}/requirements.txt",
            cwd="."
        )
        backend_results['safety'] = safety_result
        
        self.results['backend'] = backend_results
        
    def analyze_frontend(self):
        """Run JavaScript/TypeScript static analysis tools."""
        print("🌐 Running Frontend Static Analysis...")
        frontend_results = {}
        
        # 1. ESLint with max warnings 0
        print("  Running eslint...")
        eslint_result = self.run_command(
            "npx eslint --max-warnings 0 --format json src/",
            cwd=self.frontend_dir
        )
        frontend_results['eslint'] = eslint_result
        
        # 2. Prettier check
        print("  Running prettier --check...")
        prettier_result = self.run_command(
            "npx prettier --check src/",
            cwd=self.frontend_dir
        )
        frontend_results['prettier'] = prettier_result
        
        # 3. TypeScript check
        print("  Running tsc --noEmit...")
        tsc_result = self.run_command(
            "npx tsc --noEmit",
            cwd=self.frontend_dir
        )
        frontend_results['tsc'] = tsc_result
        
        # 4. Depcheck
        print("  Running depcheck...")
        depcheck_result = self.run_command(
            "npx depcheck --json",
            cwd=self.frontend_dir
        )
        frontend_results['depcheck'] = depcheck_result
        
        self.results['frontend'] = frontend_results
        
    def parse_results(self):
        """Parse results and build violation matrix."""
        print("📊 Parsing results and building violation matrix...")
        
        # Parse backend results
        if 'backend' in self.results:
            backend = self.results['backend']
            
            # Parse pylint results
            if backend.get('pylint', {}).get('stdout'):
                try:
                    pylint_data = json.loads(backend['pylint']['stdout'])
                    for issue in pylint_data:
                        if isinstance(issue, dict) and 'type' in issue:
                            severity = issue['type']
                            module = issue.get('module', 'unknown')
                            self.violation_matrix[module][f'pylint_{severity}'] += 1
                except:
                    pass
            
            # Parse flake8 results
            if backend.get('flake8', {}).get('stdout'):
                try:
                    flake8_data = json.loads(backend['flake8']['stdout'])
                    for issue in flake8_data:
                        if isinstance(issue, dict):
                            code = issue.get('code', 'unknown')
                            filename = issue.get('filename', 'unknown')
                            module = Path(filename).stem if filename != 'unknown' else 'unknown'
                            self.violation_matrix[module][f'flake8_{code}'] += 1
                except:
                    pass
                    
            # Parse bandit results
            if os.path.exists('bandit_report.json'):
                try:
                    with open('bandit_report.json', 'r') as f:
                        bandit_data = json.load(f)
                        for issue in bandit_data.get('results', []):
                            severity = issue.get('issue_severity', 'unknown')
                            filename = issue.get('filename', 'unknown')
                            module = Path(filename).stem if filename != 'unknown' else 'unknown'
                            self.violation_matrix[module][f'bandit_{severity.lower()}'] += 1
                except:
                    pass
        
        # Parse frontend results
        if 'frontend' in self.results:
            frontend = self.results['frontend']
            
            # Parse eslint results
            if frontend.get('eslint', {}).get('stdout'):
                try:
                    eslint_data = json.loads(frontend['eslint']['stdout'])
                    for file_result in eslint_data:
                        filepath = file_result.get('filePath', 'unknown')
                        module = Path(filepath).stem if filepath != 'unknown' else 'unknown'
                        for message in file_result.get('messages', []):
                            severity = 'error' if message.get('severity') == 2 else 'warning'
                            rule_id = message.get('ruleId', 'unknown')
                            self.violation_matrix[module][f'eslint_{severity}_{rule_id}'] += 1
                except:
                    pass
                    
            # Parse depcheck results
            if frontend.get('depcheck', {}).get('stdout'):
                try:
                    depcheck_data = json.loads(frontend['depcheck']['stdout'])
                    unused = depcheck_data.get('dependencies', [])
                    missing = depcheck_data.get('missing', {})
                    if unused:
                        self.violation_matrix['package.json']['depcheck_unused'] = len(unused)
                    if missing:
                        self.violation_matrix['package.json']['depcheck_missing'] = len(missing)
                except:
                    pass

    def generate_html_report(self, tool_name, tool_result, output_file):
        """Generate HTML report for a specific tool."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tool_name.title()} Static Analysis Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; margin: -30px -30px 30px -30px; border-radius: 8px 8px 0 0; }}
        .success {{ color: #27ae60; font-weight: bold; }}
        .error {{ color: #e74c3c; font-weight: bold; }}
        .warning {{ color: #f39c12; font-weight: bold; }}
        .info {{ color: #3498db; font-weight: bold; }}
        .code-block {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; margin: 10px 0; font-family: 'Courier New', monospace; }}
        .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #3498db; background: #f8f9fa; }}
        .metric {{ display: inline-block; margin: 10px; padding: 10px 15px; background: #ecf0f1; border-radius: 5px; }}
        .status-success {{ background: #d5f4e6; border-left-color: #27ae60; }}
        .status-error {{ background: #fdf2f2; border-left-color: #e74c3c; }}
        .status-warning {{ background: #fef9e7; border-left-color: #f39c12; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 {tool_name.title()} Analysis Report</h1>
            <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section {'status-success' if tool_result.get('success') else 'status-error'}">
            <h2>📋 Execution Summary</h2>
            <div class="metric">
                <strong>Status:</strong> 
                <span class="{'success' if tool_result.get('success') else 'error'}">
                    {'✅ Success' if tool_result.get('success') else '❌ Failed'}
                </span>
            </div>
            <div class="metric"><strong>Return Code:</strong> {tool_result.get('returncode', 'N/A')}</div>
            <div class="metric"><strong>Command:</strong> <code>{html.escape(tool_result.get('cmd', 'N/A'))}</code></div>
        </div>
        
        <div class="section">
            <h2>📤 Standard Output</h2>
            <div class="code-block">
                <pre>{html.escape(tool_result.get('stdout', 'No output') or 'No output')}</pre>
            </div>
        </div>
        
        <div class="section">
            <h2>📥 Standard Error</h2>
            <div class="code-block">
                <pre>{html.escape(tool_result.get('stderr', 'No errors') or 'No errors')}</pre>
            </div>
        </div>
        
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def generate_master_report(self):
        """Generate master HTML report with all results."""
        print("📝 Generating master HTML report...")
        
        # Calculate overall statistics
        total_tools = 0
        successful_tools = 0
        
        for category in self.results.values():
            for tool_result in category.values():
                total_tools += 1
                if tool_result.get('success'):
                    successful_tools += 1
        
        success_rate = (successful_tools / total_tools * 100) if total_tools > 0 else 0
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Static Code Analysis Report - Nexus Réussite</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; margin-bottom: 30px; border-radius: 10px; text-align: center; }}
        .dashboard {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .metric-large {{ font-size: 2.5em; font-weight: bold; color: #3498db; text-align: center; }}
        .metric-label {{ text-align: center; color: #7f8c8d; margin-top: 10px; }}
        .success {{ color: #27ae60; }}
        .error {{ color: #e74c3c; }}
        .warning {{ color: #f39c12; }}
        .tool-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; }}
        .tool-card {{ background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); overflow: hidden; }}
        .tool-header {{ padding: 15px; font-weight: bold; color: white; }}
        .tool-backend {{ background: #3498db; }}
        .tool-frontend {{ background: #e67e22; }}
        .tool-content {{ padding: 20px; }}
        .status-success {{ color: #27ae60; }}
        .status-error {{ color: #e74c3c; }}
        .matrix-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .matrix-table th, .matrix-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .matrix-table th {{ background-color: #f2f2f2; font-weight: bold; }}
        .matrix-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .severity-high {{ background-color: #ffebee; color: #c62828; }}
        .severity-medium {{ background-color: #fff3e0; color: #ef6c00; }}
        .severity-low {{ background-color: #f3e5f5; color: #8e24aa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Static Code Analysis Report</h1>
            <h2>Nexus Réussite Platform</h2>
            <p>Comprehensive code quality and security audit</p>
            <p><strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="dashboard">
            <div class="card">
                <div class="metric-large success">{successful_tools}/{total_tools}</div>
                <div class="metric-label">Tools Executed Successfully</div>
            </div>
            <div class="card">
                <div class="metric-large {'success' if success_rate >= 80 else 'warning' if success_rate >= 60 else 'error'}">{success_rate:.1f}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            <div class="card">
                <div class="metric-large">{len(self.violation_matrix)}</div>
                <div class="metric-label">Modules Analyzed</div>
            </div>
        </div>
        
        <div class="card">
            <h2>🎯 Tool Execution Results</h2>
            <div class="tool-grid">
"""

        # Backend tools
        if 'backend' in self.results:
            for tool_name, tool_result in self.results['backend'].items():
                status = "✅ Success" if tool_result.get('success') else "❌ Failed"
                status_class = "status-success" if tool_result.get('success') else "status-error"
                
                html_content += f"""
                <div class="tool-card">
                    <div class="tool-header tool-backend">🐍 {tool_name.upper()}</div>
                    <div class="tool-content">
                        <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
                        <p><strong>Return Code:</strong> {tool_result.get('returncode', 'N/A')}</p>
                        <p><a href="{tool_name}_report.html" target="_blank">📄 View Detailed Report</a></p>
                    </div>
                </div>
"""

        # Frontend tools  
        if 'frontend' in self.results:
            for tool_name, tool_result in self.results['frontend'].items():
                status = "✅ Success" if tool_result.get('success') else "❌ Failed"
                status_class = "status-success" if tool_result.get('success') else "status-error"
                
                html_content += f"""
                <div class="tool-card">
                    <div class="tool-header tool-frontend">🌐 {tool_name.upper()}</div>
                    <div class="tool-content">
                        <p><strong>Status:</strong> <span class="{status_class}">{status}</span></p>
                        <p><strong>Return Code:</strong> {tool_result.get('returncode', 'N/A')}</p>
                        <p><a href="{tool_name}_report.html" target="_blank">📄 View Detailed Report</a></p>
                    </div>
                </div>
"""

        html_content += """
            </div>
        </div>
        
        <div class="card">
            <h2>📊 Violation Matrix by Module and Severity</h2>
"""

        if self.violation_matrix:
            html_content += """
            <table class="matrix-table">
                <thead>
                    <tr>
                        <th>Module</th>
                        <th>Violation Type</th>
                        <th>Count</th>
                        <th>Severity</th>
                    </tr>
                </thead>
                <tbody>
"""
            
            for module, violations in self.violation_matrix.items():
                for violation_type, count in violations.items():
                    # Determine severity based on violation type
                    severity = "Low"
                    severity_class = "severity-low"
                    
                    if any(x in violation_type.lower() for x in ['error', 'high', 'bandit_high']):
                        severity = "High"
                        severity_class = "severity-high"
                    elif any(x in violation_type.lower() for x in ['warning', 'medium', 'bandit_medium']):
                        severity = "Medium"
                        severity_class = "severity-medium"
                    
                    html_content += f"""
                    <tr>
                        <td>{html.escape(module)}</td>
                        <td>{html.escape(violation_type)}</td>
                        <td>{count}</td>
                        <td><span class="{severity_class}">{severity}</span></td>
                    </tr>
"""
            
            html_content += """
                </tbody>
            </table>
"""
        else:
            html_content += "<p>No violations detected or no parseable results available.</p>"

        html_content += """
        </div>
        
        <div class="card">
            <h2>🔧 Recommended Actions</h2>
            <ul>
                <li><strong>High Priority:</strong> Address all high-severity security issues found by Bandit</li>
                <li><strong>Code Quality:</strong> Fix ESLint errors and Pylint issues</li>
                <li><strong>Style Consistency:</strong> Run Black and Prettier on codebase</li>
                <li><strong>Type Safety:</strong> Resolve MyPy and TypeScript errors</li>
                <li><strong>Dependencies:</strong> Update vulnerable packages identified by Safety</li>
                <li><strong>Unused Dependencies:</strong> Remove unused packages found by Depcheck</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>📁 Report Files</h2>
            <p>Individual tool reports have been generated in <code>docs/audit/static_analysis/</code>:</p>
            <ul>
"""

        # List all report files
        for category in self.results.values():
            for tool_name in category.keys():
                html_content += f'<li><a href="{tool_name}_report.html">{tool_name}_report.html</a></li>'

        html_content += """
            </ul>
        </div>
    </div>
</body>
</html>
"""
        
        master_report_path = self.report_dir / "index.html"
        with open(master_report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Master report generated: {master_report_path}")

    def generate_individual_reports(self):
        """Generate individual HTML reports for each tool."""
        print("📋 Generating individual tool reports...")
        
        for category_name, category_results in self.results.items():
            for tool_name, tool_result in category_results.items():
                output_file = self.report_dir / f"{tool_name}_report.html"
                self.generate_html_report(tool_name, tool_result, output_file)
                print(f"  ✅ Generated: {output_file}")

    def create_configuration_files(self):
        """Create PR-ready configuration files."""
        print("⚙️  Creating PR-ready configuration files...")
        
        # Create .pylintrc
        pylintrc_content = """[MASTER]
load-plugins=

[MESSAGES CONTROL]
disable=C0111,R0903,R0913,R0914,W0613,C0103,R0801,import-error,no-member

[REPORTS]
output-format=text
files-output=no
reports=yes
score=yes

[FORMAT]
max-line-length=88
indent-string='    '
indent-after-paren=4

[VARIABLES]
good-names=i,j,k,ex,Run,_,db,id

[DESIGN]
max-args=10
max-locals=20
max-returns=6
max-branches=12
max-statements=50
max-parents=7
max-attributes=15
min-public-methods=1
max-public-methods=20
"""
        
        with open(".pylintrc", "w") as f:
            f.write(pylintrc_content)
        
        # Create .eslintrc.json for frontend
        eslintrc_content = """{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "plugin:jsx-a11y/recommended",
    "plugin:import/recommended",
    "plugin:import/typescript",
    "prettier"
  ],
  "plugins": [
    "@typescript-eslint",
    "react",
    "react-hooks",
    "jsx-a11y",
    "import",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2020,
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "env": {
    "browser": true,
    "es2020": true,
    "node": true,
    "jest": true
  },
  "settings": {
    "react": {
      "version": "detect"
    },
    "import/resolver": {
      "typescript": {}
    }
  },
  "rules": {
    "prettier/prettier": "error",
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/explicit-function-return-type": "off",
    "@typescript-eslint/explicit-module-boundary-types": "off",
    "@typescript-eslint/no-explicit-any": "warn",
    "import/order": ["error", {
      "groups": ["builtin", "external", "internal", "parent", "sibling", "index"],
      "newlines-between": "always"
    }]
  }
}
"""
        
        frontend_eslintrc_path = self.frontend_dir / ".eslintrc.json"
        with open(frontend_eslintrc_path, "w") as f:
            f.write(eslintrc_content)
        
        print("  ✅ Created .pylintrc")
        print(f"  ✅ Created {frontend_eslintrc_path}")

    def run_analysis(self):
        """Run the complete static analysis."""
        print("🚀 Starting Static Code Analysis...")
        print("=" * 60)
        
        # Run backend analysis
        if self.backend_dir.exists():
            self.analyze_backend()
        else:
            print("⚠️  Backend directory not found, skipping backend analysis")
        
        # Run frontend analysis  
        if self.frontend_dir.exists():
            self.analyze_frontend()
        else:
            print("⚠️  Frontend directory not found, skipping frontend analysis")
        
        # Parse results and build matrix
        self.parse_results()
        
        # Generate reports
        self.generate_individual_reports()
        self.generate_master_report()
        
        # Create configuration files
        self.create_configuration_files()
        
        print("=" * 60)
        print("✅ Static analysis complete!")
        print(f"📊 Master report: {self.report_dir}/index.html")
        print(f"📁 All reports: {self.report_dir}/")


if __name__ == "__main__":
    runner = StaticAnalysisRunner()
    runner.run_analysis()
