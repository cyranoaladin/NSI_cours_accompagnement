#!/usr/bin/env python3
"""
Database & ORM Audit for Nexus Réussite
========================================

This script performs a comprehensive audit of the database schema,
SQLAlchemy models, and migrations for the Nexus Réussite platform.

Features:
- Reverse-engineer DB schema from SQLAlchemy models
- Validate naming conventions, PK/FK, indices, constraints
- Detect potential N+1 queries
- Generate ER diagram
- Recommend indexing and migration improvements
"""

import os
import sys
import inspect
import importlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Any, Optional, Tuple
from collections import defaultdict
import re

# Add backend source to path
backend_path = Path(__file__).parent / "backend" / "src"
sys.path.insert(0, str(backend_path))

try:
    import sqlalchemy as sa
    from sqlalchemy import MetaData, Table, Column, ForeignKey, Index
    from sqlalchemy.orm import relationship, backref
    from sqlalchemy.inspection import inspect as sa_inspect
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.dialects import postgresql, sqlite
    
    print("✅ Successfully imported SQLAlchemy")
except ImportError as e:
    print(f"❌ SQLAlchemy import error: {e}")
    sys.exit(1)

class DatabaseAuditor:
    """Comprehensive database audit tool"""
    
    def __init__(self):
        self.models = {}
        self.relationships = {}
        self.foreign_keys = {}
        self.indices = {}
        self.constraints = {}
        self.issues = []
        self.recommendations = []
        self.n_plus_one_risks = []
        
    def discover_models(self):
        """Discover all SQLAlchemy models in the project"""
        print("\n🔍 Discovering SQLAlchemy models...")
        
        # Import models from different modules
        model_modules = [
            'models.user',
            'models.student', 
            'models.formulas',
            'models.content_system'
        ]
        
        discovered_models = {}
        
        for module_name in model_modules:
            try:
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        hasattr(obj, '__tablename__') and
                        isinstance(obj, DeclarativeMeta)):
                        
                        discovered_models[name] = obj
                        print(f"  📋 Found model: {name} -> {obj.__tablename__}")
                        
            except ImportError as e:
                print(f"  ⚠️  Could not import {module_name}: {e}")
                
        self.models = discovered_models
        return discovered_models
        
    def analyze_schema(self):
        """Analyze the database schema structure"""
        print("\n📊 Analyzing database schema...")
        
        schema_analysis = {
            'tables': {},
            'total_columns': 0,
            'total_relationships': 0,
            'total_indices': 0,
            'naming_issues': [],
            'missing_indices': [],
            'constraint_issues': []
        }
        
        for model_name, model_class in self.models.items():
            table_info = self._analyze_table(model_class)
            schema_analysis['tables'][model_name] = table_info
            schema_analysis['total_columns'] += len(table_info['columns'])
            schema_analysis['total_relationships'] += len(table_info['relationships'])
            
        return schema_analysis
        
    def _analyze_table(self, model_class) -> Dict[str, Any]:
        """Analyze a single table/model"""
        
        table_info = {
            'tablename': model_class.__tablename__,
            'columns': {},
            'relationships': {},
            'foreign_keys': {},
            'indices': [],
            'constraints': [],
            'naming_score': 0
        }
        
        # Analyze columns
        for column_name, column in model_class.__table__.columns.items():
            column_info = {
                'type': str(column.type),
                'nullable': column.nullable,
                'primary_key': column.primary_key,
                'foreign_key': column.foreign_keys,
                'default': column.default,
                'unique': column.unique,
                'index': column.index
            }
            table_info['columns'][column_name] = column_info
            
        # Analyze relationships
        for attr_name in dir(model_class):
            attr = getattr(model_class, attr_name)
            if hasattr(attr.property, 'mapper') if hasattr(attr, 'property') else False:
                rel_info = {
                    'target_model': attr.property.mapper.class_.__name__,
                    'back_populates': getattr(attr.property, 'back_populates', None),
                    'lazy': getattr(attr.property, 'lazy', None),
                    'cascade': getattr(attr.property, 'cascade', None)
                }
                table_info['relationships'][attr_name] = rel_info
                
        # Analyze foreign keys
        for fk in model_class.__table__.foreign_keys:
            fk_info = {
                'column': fk.parent.name,
                'references': f"{fk.column.table.name}.{fk.column.name}",
                'ondelete': fk.ondelete,
                'onupdate': fk.onupdate
            }
            table_info['foreign_keys'][fk.parent.name] = fk_info
            
        # Analyze indices
        for index in model_class.__table__.indexes:
            index_info = {
                'name': index.name,
                'columns': [col.name for col in index.columns],
                'unique': index.unique
            }
            table_info['indices'].append(index_info)
            
        # Check naming conventions
        table_info['naming_score'] = self._check_naming_conventions(model_class)
        
        return table_info
        
    def _check_naming_conventions(self, model_class) -> int:
        """Check naming convention compliance"""
        score = 0
        issues = []
        
        # Table name should be lowercase and plural
        table_name = model_class.__tablename__
        if table_name.islower():
            score += 2
        else:
            issues.append(f"Table {table_name} should be lowercase")
            
        # Check if table name is plural (basic check)
        if table_name.endswith('s') or table_name.endswith('es'):
            score += 1
        else:
            issues.append(f"Table {table_name} should be plural")
            
        # Column naming
        for column_name, column in model_class.__table__.columns.items():
            if column_name.islower():
                score += 1
            else:
                issues.append(f"Column {table_name}.{column_name} should be lowercase")
                
            # Foreign key naming
            if column.foreign_keys:
                if column_name.endswith('_id'):
                    score += 1
                else:
                    issues.append(f"Foreign key {table_name}.{column_name} should end with '_id'")
                    
        self.issues.extend(issues)
        return score
        
    def detect_n_plus_one_risks(self):
        """Detect potential N+1 query issues"""
        print("\n🔍 Detecting potential N+1 query risks...")
        
        risks = []
        
        for model_name, model_class in self.models.items():
            # Check relationships with lazy loading
            for attr_name in dir(model_class):
                attr = getattr(model_class, attr_name)
                if hasattr(attr, 'property') and hasattr(attr.property, 'mapper'):
                    lazy_setting = getattr(attr.property, 'lazy', 'select')
                    
                    if lazy_setting == 'select':  # Default lazy loading
                        risk = {
                            'model': model_name,
                            'relationship': attr_name,
                            'target': attr.property.mapper.class_.__name__,
                            'risk_level': 'HIGH',
                            'description': f"Relationship {model_name}.{attr_name} uses lazy='select' which can cause N+1 queries",
                            'recommendation': f"Consider using lazy='joined' or lazy='subquery' for {attr_name}"
                        }
                        risks.append(risk)
                        
        self.n_plus_one_risks = risks
        return risks
        
    def validate_indices(self):
        """Validate index usage and suggest improvements"""
        print("\n📈 Validating indices and suggesting improvements...")
        
        missing_indices = []
        recommendations = []
        
        for model_name, model_class in self.models.items():
            table = model_class.__table__
            
            # Check for missing indices on foreign keys
            for column in table.columns:
                if column.foreign_keys and not column.index and not column.primary_key:
                    missing_indices.append({
                        'table': table.name,
                        'column': column.name,
                        'reason': 'Foreign key without index',
                        'recommendation': f"ADD INDEX idx_{table.name}_{column.name} ON {table.name}({column.name})"
                    })
                    
            # Check for commonly queried fields that should have indices
            common_query_fields = ['email', 'created_at', 'updated_at', 'status', 'type']
            for column in table.columns:
                if (column.name in common_query_fields and 
                    not column.index and 
                    not column.primary_key and 
                    not column.unique):
                    
                    missing_indices.append({
                        'table': table.name,
                        'column': column.name,
                        'reason': f'Common query field "{column.name}" without index',
                        'recommendation': f"ADD INDEX idx_{table.name}_{column.name} ON {table.name}({column.name})"
                    })
                    
        # Suggest composite indices for common query patterns
        composite_suggestions = [
            {
                'table': 'users',
                'columns': ['role', 'status'],
                'reason': 'Common filtering pattern'
            },
            {
                'table': 'learning_sessions',
                'columns': ['student_id', 'created_at'],
                'reason': 'Common student session queries'
            },
            {
                'table': 'assessments',
                'columns': ['student_id', 'subject'],
                'reason': 'Subject-specific assessments per student'
            }
        ]
        
        for suggestion in composite_suggestions:
            if suggestion['table'] in [model.__tablename__ for model in self.models.values()]:
                recommendations.append({
                    'type': 'composite_index',
                    'table': suggestion['table'],
                    'columns': suggestion['columns'],
                    'reason': suggestion['reason'],
                    'sql': f"CREATE INDEX idx_{suggestion['table']}_{'_'.join(suggestion['columns'])} ON {suggestion['table']}({', '.join(suggestion['columns'])})"
                })
                
        return missing_indices, recommendations
        
    def generate_er_diagram_dbml(self):
        """Generate ER diagram in DBML format"""
        print("\n🎨 Generating ER diagram in DBML format...")
        
        dbml_content = []
        dbml_content.append("// Nexus Réussite Database Schema")
        dbml_content.append(f"// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        dbml_content.append("")
        
        # Generate tables
        for model_name, model_class in self.models.items():
            table = model_class.__table__
            
            dbml_content.append(f"Table {table.name} {{")
            
            # Add columns
            for column in table.columns:
                column_def = f"  {column.name} {self._get_dbml_type(column.type)}"
                
                attributes = []
                if column.primary_key:
                    attributes.append("pk")
                if not column.nullable:
                    attributes.append("not null")
                if column.unique:
                    attributes.append("unique")
                if column.default:
                    attributes.append(f"default: {column.default}")
                    
                if attributes:
                    column_def += f" [{', '.join(attributes)}]"
                    
                dbml_content.append(column_def)
                
            dbml_content.append("}")
            dbml_content.append("")
            
        # Generate relationships
        dbml_content.append("// Relationships")
        for model_name, model_class in self.models.items():
            table = model_class.__table__
            
            for fk in table.foreign_keys:
                ref_table = fk.column.table.name
                ref_column = fk.column.name
                local_column = fk.parent.name
                
                dbml_content.append(f"Ref: {table.name}.{local_column} > {ref_table}.{ref_column}")
                
        return "\n".join(dbml_content)
        
    def _get_dbml_type(self, sa_type):
        """Convert SQLAlchemy type to DBML type"""
        type_mapping = {
            'INTEGER': 'int',
            'VARCHAR': 'varchar',
            'TEXT': 'text',
            'BOOLEAN': 'boolean',
            'DATETIME': 'datetime',
            'DATE': 'date',
            'FLOAT': 'float',
            'JSON': 'json'
        }
        
        type_str = str(sa_type).upper()
        for sa_t, dbml_t in type_mapping.items():
            if sa_t in type_str:
                return dbml_t
        return 'varchar'  # default
        
    def generate_migration_recommendations(self):
        """Generate migration and cleanup recommendations"""
        print("\n🔧 Generating migration and cleanup recommendations...")
        
        recommendations = []
        
        # Index recommendations
        missing_indices, index_recommendations = self.validate_indices()
        
        for missing_idx in missing_indices:
            recommendations.append({
                'type': 'add_index',
                'priority': 'HIGH',
                'description': f"Add index to {missing_idx['table']}.{missing_idx['column']}",
                'reason': missing_idx['reason'],
                'migration_sql': missing_idx['recommendation']
            })
            
        # Naming convention fixes
        for issue in self.issues:
            if 'should be lowercase' in issue:
                recommendations.append({
                    'type': 'naming_convention',
                    'priority': 'MEDIUM',
                    'description': issue,
                    'reason': 'Improve consistency and readability'
                })
                
        # N+1 query fixes
        for risk in self.n_plus_one_risks:
            recommendations.append({
                'type': 'performance',
                'priority': 'HIGH',
                'description': risk['description'],
                'reason': 'Prevent N+1 query performance issues',
                'fix': risk['recommendation']
            })
            
        # Data type optimizations
        for model_name, model_class in self.models.items():
            for column_name, column in model_class.__table__.columns.items():
                # Suggest VARCHAR limits for text fields
                if 'VARCHAR' in str(column.type) and not hasattr(column.type, 'length'):
                    recommendations.append({
                        'type': 'data_type',
                        'priority': 'LOW',
                        'description': f"Add length limit to {model_class.__tablename__}.{column_name}",
                        'reason': 'Improve storage efficiency and validation'
                    })
                    
        return recommendations
        
    def generate_report(self):
        """Generate comprehensive audit report"""
        print("\n📋 Generating comprehensive audit report...")
        
        # Discover models
        models = self.discover_models()
        
        # Analyze schema
        schema_analysis = self.analyze_schema()
        
        # Detect N+1 risks
        n_plus_one_risks = self.detect_n_plus_one_risks()
        
        # Validate indices
        missing_indices, index_recommendations = self.validate_indices()
        
        # Generate DBML
        dbml_content = self.generate_er_diagram_dbml()
        
        # Generate recommendations
        migration_recommendations = self.generate_migration_recommendations()
        
        # Create report
        report = {
            'audit_date': datetime.now().isoformat(),
            'summary': {
                'total_models': len(models),
                'total_tables': len(schema_analysis['tables']),
                'total_columns': schema_analysis['total_columns'],
                'total_relationships': schema_analysis['total_relationships'],
                'total_issues': len(self.issues),
                'n_plus_one_risks': len(n_plus_one_risks),
                'missing_indices': len(missing_indices),
                'recommendations': len(migration_recommendations)
            },
            'models': models,
            'schema_analysis': schema_analysis,
            'n_plus_one_risks': n_plus_one_risks,
            'missing_indices': missing_indices,
            'recommendations': migration_recommendations,
            'dbml_schema': dbml_content
        }
        
        return report
        
    def save_report(self, report, output_dir="docs/audit/database"):
        """Save audit report to files"""
        import json
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save JSON report
        json_file = output_path / "database_audit_report.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            # Convert non-serializable objects to strings
            serializable_report = self._make_serializable(report)
            json.dump(serializable_report, f, indent=2, ensure_ascii=False)
            
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
        
    def _make_serializable(self, obj):
        """Convert objects to JSON-serializable format"""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return str(obj)
        else:
            return obj
            
    def _generate_markdown_report(self, report, output_file):
        """Generate markdown audit report"""
        
        md_content = []
        md_content.append("# Database & ORM Audit Report")
        md_content.append(f"**Generated:** {report['audit_date']}")
        md_content.append("")
        
        # Executive Summary
        summary = report['summary']
        md_content.append("## Executive Summary")
        md_content.append("")
        md_content.append(f"- **Total Models:** {summary['total_models']}")
        md_content.append(f"- **Total Tables:** {summary['total_tables']}")
        md_content.append(f"- **Total Columns:** {summary['total_columns']}")
        md_content.append(f"- **Total Relationships:** {summary['total_relationships']}")
        md_content.append(f"- **Issues Found:** {summary['total_issues']}")
        md_content.append(f"- **N+1 Query Risks:** {summary['n_plus_one_risks']}")
        md_content.append(f"- **Missing Indices:** {summary['missing_indices']}")
        md_content.append(f"- **Total Recommendations:** {summary['recommendations']}")
        md_content.append("")
        
        # Models Overview
        md_content.append("## Models Overview")
        md_content.append("")
        for model_name in report['models'].keys():
            md_content.append(f"- **{model_name}**")
        md_content.append("")
        
        # N+1 Query Risks
        if report['n_plus_one_risks']:
            md_content.append("## ⚠️ N+1 Query Risks")
            md_content.append("")
            for risk in report['n_plus_one_risks']:
                md_content.append(f"### {risk['model']}.{risk['relationship']}")
                md_content.append(f"- **Risk Level:** {risk['risk_level']}")
                md_content.append(f"- **Description:** {risk['description']}")
                md_content.append(f"- **Recommendation:** {risk['recommendation']}")
                md_content.append("")
                
        # Missing Indices
        if report['missing_indices']:
            md_content.append("## 📈 Missing Indices")
            md_content.append("")
            for idx in report['missing_indices']:
                md_content.append(f"### {idx['table']}.{idx['column']}")
                md_content.append(f"- **Reason:** {idx['reason']}")
                md_content.append(f"- **SQL:** `{idx['recommendation']}`")
                md_content.append("")
                
        # Recommendations
        md_content.append("## 🔧 Recommendations")
        md_content.append("")
        
        # Group recommendations by priority
        high_priority = [r for r in report['recommendations'] if r.get('priority') == 'HIGH']
        medium_priority = [r for r in report['recommendations'] if r.get('priority') == 'MEDIUM']
        low_priority = [r for r in report['recommendations'] if r.get('priority') == 'LOW']
        
        if high_priority:
            md_content.append("### 🔴 High Priority")
            md_content.append("")
            for rec in high_priority:
                md_content.append(f"- **{rec['type'].title()}:** {rec['description']}")
                if 'migration_sql' in rec:
                    md_content.append(f"  ```sql\n  {rec['migration_sql']}\n  ```")
                md_content.append("")
                
        if medium_priority:
            md_content.append("### 🟡 Medium Priority")
            md_content.append("")
            for rec in medium_priority:
                md_content.append(f"- **{rec['type'].title()}:** {rec['description']}")
                md_content.append("")
                
        if low_priority:
            md_content.append("### 🟢 Low Priority")
            md_content.append("")
            for rec in low_priority:
                md_content.append(f"- **{rec['type'].title()}:** {rec['description']}")
                md_content.append("")
                
        # DBML Schema
        md_content.append("## 🎨 Database Schema (DBML)")
        md_content.append("")
        md_content.append("```dbml")
        md_content.append(report['dbml_schema'])
        md_content.append("```")
        
        # Write file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))

def main():
    """Main audit function"""
    print("🚀 Starting Database & ORM Audit for Nexus Réussite")
    print("=" * 60)
    
    auditor = DatabaseAuditor()
    
    try:
        # Generate comprehensive report
        report = auditor.generate_report()
        
        # Save reports
        auditor.save_report(report)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        print(f"✅ Models analyzed: {report['summary']['total_models']}")
        print(f"📋 Tables found: {report['summary']['total_tables']}")
        print(f"🔗 Relationships: {report['summary']['total_relationships']}")
        print(f"⚠️  Issues found: {report['summary']['total_issues']}")
        print(f"🐌 N+1 risks: {report['summary']['n_plus_one_risks']}")
        print(f"📈 Missing indices: {report['summary']['missing_indices']}")
        print(f"💡 Recommendations: {report['summary']['recommendations']}")
        
        if report['summary']['total_issues'] > 0:
            print(f"\n🔴 Critical issues found! Check the detailed report.")
        else:
            print(f"\n✅ No critical issues found. Great job!")
            
    except Exception as e:
        print(f"\n❌ Audit failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
