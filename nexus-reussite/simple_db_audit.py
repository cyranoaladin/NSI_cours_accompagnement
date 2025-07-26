#!/usr/bin/env python3
"""
Simple Database & ORM Audit for Nexus Réussite
=============================================

This script analyzes the database models by directly parsing the Python files
to extract schema information and provide recommendations.
"""

import os
import re
import ast
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import json

class SimpleDBAnalyzer:
    """Simple database analyzer that parses model files"""
    
    def __init__(self):
        self.models = {}
        self.issues = []
        self.recommendations = []
        
    def analyze_model_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single model file"""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract class definitions
        tree = ast.parse(content)
        models_in_file = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Look for SQLAlchemy models
                model_info = self._analyze_class(node, content)
                if model_info:
                    models_in_file[node.name] = model_info
                    
        return models_in_file
        
    def _analyze_class(self, class_node: ast.ClassDef, file_content: str) -> Dict[str, Any]:
        """Analyze a class definition to extract model info"""
        
        model_info = {
            'name': class_node.name,
            'tablename': None,
            'columns': [],
            'relationships': [],
            'foreign_keys': [],
            'indices': [],
            'issues': []
        }
        
        # Check if it's a SQLAlchemy model
        has_tablename = False
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == '__tablename__':
                            has_tablename = True
                            if isinstance(node.value, ast.Constant):
                                model_info['tablename'] = node.value.value
                                
                        elif target.id.endswith('_id') or 'Column' in ast.dump(node.value):
                            # This looks like a column
                            column_info = self._extract_column_info(target.id, node, file_content)
                            if column_info:
                                model_info['columns'].append(column_info)
                                
                        elif 'relationship' in ast.dump(node.value):
                            # This looks like a relationship
                            rel_info = self._extract_relationship_info(target.id, node, file_content)
                            if rel_info:
                                model_info['relationships'].append(rel_info)
                                
        return model_info if has_tablename else None
        
    def _extract_column_info(self, name: str, node: ast.AST, content: str) -> Dict[str, Any]:
        """Extract column information"""
        
        column_info = {
            'name': name,
            'type': 'Unknown',
            'nullable': True,
            'primary_key': False,
            'foreign_key': False,
            'unique': False,
            'index': False
        }
        
        # Parse the column definition from the source
        try:
            line_start = node.lineno
            lines = content.split('\n')
            if line_start <= len(lines):
                line = lines[line_start - 1]
                
                # Check for common patterns
                if 'primary_key=True' in line:
                    column_info['primary_key'] = True
                if 'nullable=False' in line:
                    column_info['nullable'] = False
                if 'unique=True' in line:
                    column_info['unique'] = True
                if 'index=True' in line:
                    column_info['index'] = True
                if 'ForeignKey' in line:
                    column_info['foreign_key'] = True
                    
                # Extract type
                if 'Integer' in line:
                    column_info['type'] = 'Integer'
                elif 'String' in line:
                    column_info['type'] = 'String'
                elif 'Text' in line:
                    column_info['type'] = 'Text'
                elif 'Boolean' in line:
                    column_info['type'] = 'Boolean'
                elif 'DateTime' in line:
                    column_info['type'] = 'DateTime'
                elif 'JSON' in line:
                    column_info['type'] = 'JSON'
                elif 'Float' in line:
                    column_info['type'] = 'Float'
                elif 'Enum' in line:
                    column_info['type'] = 'Enum'
                    
        except Exception:
            pass
            
        return column_info
        
    def _extract_relationship_info(self, name: str, node: ast.AST, content: str) -> Dict[str, Any]:
        """Extract relationship information"""
        
        rel_info = {
            'name': name,
            'target': 'Unknown',
            'backref': None,
            'lazy': 'select',  # default
            'cascade': None
        }
        
        try:
            line_start = node.lineno
            lines = content.split('\n')
            if line_start <= len(lines):
                line = lines[line_start - 1]
                
                # Extract target model
                if "'" in line:
                    quotes = re.findall(r"'([^']*)'", line)
                    if quotes:
                        rel_info['target'] = quotes[0]
                        
                # Check lazy loading
                if 'lazy=True' in line:
                    rel_info['lazy'] = 'select'
                elif "lazy='joined'" in line:
                    rel_info['lazy'] = 'joined'
                elif "lazy='subquery'" in line:
                    rel_info['lazy'] = 'subquery'
                elif "lazy='dynamic'" in line:
                    rel_info['lazy'] = 'dynamic'
                    
        except Exception:
            pass
            
        return rel_info
        
    def analyze_all_models(self) -> Dict[str, Any]:
        """Analyze all model files in the project"""
        
        backend_path = Path("backend/src/models")
        if not backend_path.exists():
            return {"error": "Models directory not found"}
            
        all_models = {}
        
        # Find all Python files in models directory
        for py_file in backend_path.glob("*.py"):
            if py_file.name != "__init__.py":
                print(f"📋 Analyzing {py_file.name}")
                models_in_file = self.analyze_model_file(py_file)
                all_models.update(models_in_file)
                
        self.models = all_models
        return all_models
        
    def validate_naming_conventions(self):
        """Validate naming conventions"""
        
        naming_issues = []
        
        for model_name, model_info in self.models.items():
            table_name = model_info.get('tablename', '')
            
            # Table name should be lowercase and plural
            if not table_name.islower():
                naming_issues.append({
                    'type': 'naming',
                    'severity': 'medium',
                    'model': model_name,
                    'issue': f"Table name '{table_name}' should be lowercase",
                    'recommendation': f"Change to '{table_name.lower()}'"
                })
                
            if not (table_name.endswith('s') or table_name.endswith('es')):
                naming_issues.append({
                    'type': 'naming',
                    'severity': 'low',
                    'model': model_name,
                    'issue': f"Table name '{table_name}' should be plural",
                    'recommendation': f"Consider making table name plural"
                })
                
            # Check column naming
            for column in model_info.get('columns', []):
                col_name = column['name']
                
                if column['foreign_key'] and not col_name.endswith('_id'):
                    naming_issues.append({
                        'type': 'naming',
                        'severity': 'medium',
                        'model': model_name,
                        'issue': f"Foreign key column '{col_name}' should end with '_id'",
                        'recommendation': f"Rename to '{col_name}_id' if appropriate"
                    })
                    
        return naming_issues
        
    def detect_missing_indices(self):
        """Detect missing indices"""
        
        missing_indices = []
        
        for model_name, model_info in self.models.items():
            table_name = model_info.get('tablename', '')
            
            for column in model_info.get('columns', []):
                col_name = column['name']
                
                # Foreign keys should have indices
                if column['foreign_key'] and not column['index'] and not column['primary_key']:
                    missing_indices.append({
                        'type': 'missing_index',
                        'severity': 'high',
                        'model': model_name,
                        'table': table_name,
                        'column': col_name,
                        'reason': 'Foreign key without index',
                        'sql': f"CREATE INDEX idx_{table_name}_{col_name} ON {table_name}({col_name});"
                    })
                    
                # Common query fields should have indices
                common_fields = ['email', 'created_at', 'updated_at', 'status', 'type']
                if (col_name in common_fields and 
                    not column['index'] and 
                    not column['primary_key'] and 
                    not column['unique']):
                    
                    missing_indices.append({
                        'type': 'missing_index',
                        'severity': 'medium',
                        'model': model_name,
                        'table': table_name,
                        'column': col_name,
                        'reason': f'Common query field "{col_name}" without index',
                        'sql': f"CREATE INDEX idx_{table_name}_{col_name} ON {table_name}({col_name});"
                    })
                    
        return missing_indices
        
    def detect_n_plus_one_risks(self):
        """Detect potential N+1 query risks"""
        
        n_plus_one_risks = []
        
        for model_name, model_info in self.models.items():
            for relationship in model_info.get('relationships', []):
                if relationship['lazy'] == 'select':  # Default lazy loading
                    n_plus_one_risks.append({
                        'type': 'n_plus_one_risk',
                        'severity': 'high',
                        'model': model_name,
                        'relationship': relationship['name'],
                        'target': relationship['target'],
                        'issue': f"Relationship {model_name}.{relationship['name']} uses lazy='select'",
                        'recommendation': f"Consider using lazy='joined' or lazy='subquery' for {relationship['name']}"
                    })
                    
        return n_plus_one_risks
        
    def generate_dbml_schema(self):
        """Generate DBML schema"""
        
        dbml_lines = []
        dbml_lines.append("// Nexus Réussite Database Schema")
        dbml_lines.append(f"// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dbml_lines.append("")
        
        # Generate tables
        for model_name, model_info in self.models.items():
            table_name = model_info.get('tablename', model_name.lower())
            
            dbml_lines.append(f"Table {table_name} {{")
            
            for column in model_info.get('columns', []):
                col_def = f"  {column['name']} {self._dbml_type(column['type'])}"
                
                attributes = []
                if column['primary_key']:
                    attributes.append('pk')
                if not column['nullable']:
                    attributes.append('not null')
                if column['unique']:
                    attributes.append('unique')
                    
                if attributes:
                    col_def += f" [{', '.join(attributes)}]"
                    
                dbml_lines.append(col_def)
                
            dbml_lines.append("}")
            dbml_lines.append("")
            
        # Generate relationships (simplified)
        dbml_lines.append("// Relationships")
        for model_name, model_info in self.models.items():
            table_name = model_info.get('tablename', model_name.lower())
            
            for column in model_info.get('columns', []):
                if column['foreign_key'] and column['name'].endswith('_id'):
                    # Try to infer the referenced table
                    ref_table = column['name'][:-3] + 's'  # Simple pluralization
                    dbml_lines.append(f"Ref: {table_name}.{column['name']} > {ref_table}.id")
                    
        return "\n".join(dbml_lines)
        
    def _dbml_type(self, sa_type: str) -> str:
        """Convert SQLAlchemy type to DBML type"""
        type_mapping = {
            'Integer': 'int',
            'String': 'varchar',
            'Text': 'text',
            'Boolean': 'boolean',
            'DateTime': 'datetime',
            'JSON': 'json',
            'Float': 'float',
            'Enum': 'varchar'
        }
        return type_mapping.get(sa_type, 'varchar')
        
    def generate_comprehensive_report(self):
        """Generate comprehensive audit report"""
        
        print("\n🔍 Analyzing models...")
        models = self.analyze_all_models()
        
        print("🔍 Validating naming conventions...")
        naming_issues = self.validate_naming_conventions()
        
        print("🔍 Detecting missing indices...")
        missing_indices = self.detect_missing_indices()
        
        print("🔍 Detecting N+1 query risks...")
        n_plus_one_risks = self.detect_n_plus_one_risks()
        
        print("🔍 Generating DBML schema...")
        dbml_schema = self.generate_dbml_schema()
        
        # Combine all issues
        all_issues = naming_issues + missing_indices + n_plus_one_risks
        
        # Group by severity
        high_issues = [i for i in all_issues if i.get('severity') == 'high']
        medium_issues = [i for i in all_issues if i.get('severity') == 'medium']
        low_issues = [i for i in all_issues if i.get('severity') == 'low']
        
        report = {
            'audit_date': datetime.now().isoformat(),
            'summary': {
                'total_models': len(models),
                'total_issues': len(all_issues),
                'high_severity': len(high_issues),
                'medium_severity': len(medium_issues),
                'low_severity': len(low_issues),
                'naming_issues': len(naming_issues),
                'missing_indices': len(missing_indices),
                'n_plus_one_risks': len(n_plus_one_risks)
            },
            'models': models,
            'issues': {
                'high': high_issues,
                'medium': medium_issues,
                'low': low_issues
            },
            'dbml_schema': dbml_schema
        }
        
        return report
        
    def save_report(self, report: Dict[str, Any], output_dir: str = "docs/audit/database"):
        """Save the audit report"""
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON report
        json_file = output_path / "database_audit_report.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Save DBML schema
        dbml_file = output_path / "nexus_reussite_schema.dbml"
        with open(dbml_file, 'w', encoding='utf-8') as f:
            f.write(report['dbml_schema'])
            
        # Save markdown report
        md_file = output_path / "DATABASE_AUDIT_REPORT.md"
        self._generate_markdown_report(report, md_file)
        
        print(f"\n✅ Reports saved to {output_path}/")
        print(f"   📄 JSON Report: {json_file}")
        print(f"   🎨 DBML Schema: {dbml_file}")
        print(f"   📝 Markdown Report: {md_file}")
        
    def _generate_markdown_report(self, report: Dict[str, Any], output_file: Path):
        """Generate markdown report"""
        
        md_content = []
        md_content.append("# Database & ORM Audit Report")
        md_content.append(f"**Generated:** {report['audit_date']}")
        md_content.append("")
        
        # Executive Summary
        summary = report['summary']
        md_content.append("## Executive Summary")
        md_content.append("")
        md_content.append(f"- **Total Models:** {summary['total_models']}")
        md_content.append(f"- **Total Issues:** {summary['total_issues']}")
        md_content.append(f"- **High Severity:** {summary['high_severity']}")
        md_content.append(f"- **Medium Severity:** {summary['medium_severity']}")
        md_content.append(f"- **Low Severity:** {summary['low_severity']}")
        md_content.append("")
        
        # Models Overview
        md_content.append("## Models Discovered")
        md_content.append("")
        for model_name, model_info in report['models'].items():
            table_name = model_info.get('tablename', 'N/A')
            column_count = len(model_info.get('columns', []))
            relationship_count = len(model_info.get('relationships', []))
            
            md_content.append(f"### {model_name}")
            md_content.append(f"- **Table:** `{table_name}`")
            md_content.append(f"- **Columns:** {column_count}")
            md_content.append(f"- **Relationships:** {relationship_count}")
            md_content.append("")
            
        # Issues by Severity
        issues = report['issues']
        
        if issues['high']:
            md_content.append("## 🔴 High Severity Issues")
            md_content.append("")
            for issue in issues['high']:
                md_content.append(f"### {issue['model']}")
                md_content.append(f"- **Type:** {issue['type']}")
                md_content.append(f"- **Issue:** {issue.get('issue', issue.get('reason', 'N/A'))}")
                md_content.append(f"- **Recommendation:** {issue.get('recommendation', 'N/A')}")
                if 'sql' in issue:
                    md_content.append(f"- **SQL:** `{issue['sql']}`")
                md_content.append("")
                
        if issues['medium']:
            md_content.append("## 🟡 Medium Severity Issues")
            md_content.append("")
            for issue in issues['medium']:
                md_content.append(f"### {issue['model']}")
                md_content.append(f"- **Type:** {issue['type']}")
                md_content.append(f"- **Issue:** {issue.get('issue', issue.get('reason', 'N/A'))}")
                md_content.append(f"- **Recommendation:** {issue.get('recommendation', 'N/A')}")
                if 'sql' in issue:
                    md_content.append(f"- **SQL:** `{issue['sql']}`")
                md_content.append("")
                
        if issues['low']:
            md_content.append("## 🟢 Low Severity Issues")
            md_content.append("")
            for issue in issues['low']:
                md_content.append(f"### {issue['model']}")
                md_content.append(f"- **Type:** {issue['type']}")
                md_content.append(f"- **Issue:** {issue.get('issue', issue.get('reason', 'N/A'))}")
                md_content.append(f"- **Recommendation:** {issue.get('recommendation', 'N/A')}")
                md_content.append("")
                
        # DBML Schema
        md_content.append("## Database Schema (DBML)")
        md_content.append("")
        md_content.append("```dbml")
        md_content.append(report['dbml_schema'])
        md_content.append("```")
        
        # Write file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))

def main():
    """Main audit function"""
    print("🚀 Starting Simple Database Audit for Nexus Réussite")
    print("=" * 60)
    
    analyzer = SimpleDBAnalyzer()
    
    try:
        # Generate comprehensive report
        report = analyzer.generate_comprehensive_report()
        
        # Save reports
        analyzer.save_report(report)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        print(f"✅ Models analyzed: {report['summary']['total_models']}")
        print(f"⚠️  Total issues: {report['summary']['total_issues']}")
        print(f"🔴 High severity: {report['summary']['high_severity']}")
        print(f"🟡 Medium severity: {report['summary']['medium_severity']}")
        print(f"🟢 Low severity: {report['summary']['low_severity']}")
        print(f"📝 Naming issues: {report['summary']['naming_issues']}")
        print(f"📈 Missing indices: {report['summary']['missing_indices']}")
        print(f"🐌 N+1 risks: {report['summary']['n_plus_one_risks']}")
        
        if report['summary']['high_severity'] > 0:
            print(f"\n🔴 Critical issues found! Check the detailed report.")
        elif report['summary']['total_issues'] > 0:
            print(f"\n🟡 Some issues found. Review the recommendations.")
        else:
            print(f"\n✅ No issues found. Great job!")
            
    except Exception as e:
        print(f"\n❌ Audit failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
