#!/usr/bin/env python3
"""
Migrate existing CSV catalog to new YAML multi-level threshold format
"""
import csv
import yaml
from pathlib import Path
from datetime import datetime

def map_severity_to_level(severity):
    """Map severity to primary maturity level"""
    severity_map = {
        'Critical': 1,
        'High': 2,
        'Medium': 3,
        'Low': 4
    }
    return severity_map.get(severity, 3)

def create_yaml_check(csv_row):
    """Convert CSV row to YAML check structure"""

    check_id = csv_row['check_id']
    severity = csv_row.get('severity', 'Medium')
    level = map_severity_to_level(severity)

    # Calculate CVSS score estimate based on severity
    cvss_map = {'Critical': 9.0, 'High': 7.5, 'Medium': 5.5, 'Low': 3.5}
    cvss_score = cvss_map.get(severity, 5.0)

    # Calculate points deduction
    weight = float(csv_row.get('drive_weight', 0.5))
    points = int(weight * 100) if weight < 1 else int(weight)

    check = {
        'check_id': check_id,
        'title': csv_row.get('title', ''),
        'short_description': csv_row.get('title', ''),
        'detailed_description': csv_row.get('description', ''),
        'category': csv_row.get('category', 'Access Control'),
        'platform': csv_row.get('platform', 'SharePoint'),
        'drive_pillars': [csv_row.get('drive_pillar', 'R')] if csv_row.get('drive_pillar') else ['R'],
        'automatable': csv_row.get('automatable', 'true').lower() == 'true',
        'owner': csv_row.get('owner', 'DRIVE-Team'),
        'status': csv_row.get('status', 'active'),
        'created_date': '2024-01-15',
        'last_updated': csv_row.get('last_updated_utc', datetime.utcnow().strftime('%Y-%m-%d')),

        # Detection
        'detection': {
            'data_sources': ['Microsoft 365 API', f'{csv_row.get("platform", "SharePoint")} API'],
            'query_logic': csv_row.get('logic', 'Detection logic to be documented'),
            'data_points_required': csv_row.get('data_points', 'Data points to be documented').split(',')
        },

        # Level thresholds - single threshold for migration
        'level_thresholds': [{
            'level': level,
            'threshold_id': f"{check_id}-L{level}",
            'threshold_condition': 'Condition to be defined',
            'threshold_description': csv_row.get('title', ''),
            'severity': severity,
            'business_impact': csv_row.get('description', ''),
            'threat_timeline': get_threat_timeline(level),
            'attacker_profile': get_attacker_profile(level),
            'cvss_score': cvss_score,
            'points_deduction': points,
            'remediation_priority': level
        }],

        # Framework mappings
        'framework_mappings': {
            'nist_csf': {
                'function': csv_row.get('nist_csf_function', 'PROTECT'),
                'categories': [csv_row.get('nist_csf_id', '')] if csv_row.get('nist_csf_id') else [],
                'controls': [csv_row.get('nist_csf_id', '')] if csv_row.get('nist_csf_id') else []
            },
            'cis_v8': {
                'controls': [csv_row.get('cis_v8_control', '')] if csv_row.get('cis_v8_control') else []
            },
            'cis_m365': {
                'version': 'v5.0',
                'recommendations': [csv_row.get('cis_m365_benchmark', '')] if csv_row.get('cis_m365_benchmark') else []
            },
            'iso_27001': {
                'version': '2022',
                'controls': [csv_row.get('iso_27001_annex', '')] if csv_row.get('iso_27001_annex') else []
            }
        },

        # Remediation
        'remediation': {
            'automated_fix_available': False,
            '1secure_remediable': False,
            'fix_complexity': 'Medium',
            'estimated_time_minutes': 60,
            'prerequisites': ['Administrator access', 'Change approval'],
            'steps': [{
                'step': 1,
                'level_target': [level],
                'action': 'Review and remediate finding',
                'details': 'Detailed remediation steps to be documented',
                'requires_manual': True,
                'manual_reason': 'Requires business context and approval'
            }]
        },

        # Validation
        'validation': {
            'test_queries': [],
            'false_positive_scenarios': []
        },

        # References
        'references': {
            'microsoft_docs': [],
            'industry_guidance': [],
            'threat_intelligence': []
        },

        # Metadata
        'metadata': {
            'version': '1.0.0',
            'schema_version': '2.0',
            'last_reviewed': datetime.utcnow().strftime('%Y-%m-%d'),
            'next_review_due': '2026-01-09',
            'reviewed_by': 'DRIVE-Team',
            'change_history': [{
                'date': datetime.utcnow().strftime('%Y-%m-%d'),
                'version': '1.0.0',
                'change': 'Migrated from CSV to YAML multi-level format',
                'author': 'Migration Script'
            }]
        }
    }

    return check

def get_threat_timeline(level):
    """Get threat timeline based on level"""
    timelines = {
        1: 'Exploitable within hours',
        2: 'Exploitable within days to weeks',
        3: 'Exploitable within weeks to months',
        4: 'Low probability exploitation',
        5: 'Future-proofing'
    }
    return timelines.get(level, 'Exploitable within weeks to months')

def get_attacker_profile(level):
    """Get attacker profile based on level"""
    profiles = {
        1: 'Low skill - script kiddie',
        2: 'Medium skill - skilled attacker',
        3: 'Advanced - persistent threat actor',
        4: 'Expert - APT groups',
        5: 'Nation-state actors'
    }
    return profiles.get(level, 'Medium skill')

def migrate_catalog():
    """Migrate CSV catalog to YAML format"""

    csv_file = 'catalog/drive_risk_catalog.csv'
    output_dir = Path('checks')
    output_dir.mkdir(exist_ok=True)

    print(f"Reading catalog from {csv_file}...")

    migrated = 0
    errors = []

    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            try:
                check = create_yaml_check(row)
                check_id = check['check_id']

                # Write YAML file
                yaml_file = output_dir / f"{check_id}.yaml"

                with open(yaml_file, 'w') as yf:
                    yaml.dump(check, yf, default_flow_style=False, sort_keys=False, allow_unicode=True)

                print(f"✓ Migrated {check_id} -> {yaml_file}")
                migrated += 1

            except Exception as e:
                errors.append(f"✗ Error migrating {row.get('check_id', 'unknown')}: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Migration Summary:")
    print(f"  ✓ Successfully migrated: {migrated} checks")
    if errors:
        print(f"  ✗ Errors: {len(errors)}")
        for error in errors[:5]:  # Show first 5 errors
            print(f"    {error}")
        if len(errors) > 5:
            print(f"    ... and {len(errors) - 5} more errors")
    print(f"{'='*60}")

    print(f"\nNext steps:")
    print(f"1. Review generated YAML files in checks/ directory")
    print(f"2. Add multi-level thresholds to checks that warrant it")
    print(f"3. Fill in detailed remediation steps")
    print(f"4. Validate with: python tools/validate_checks.py checks/")
    print(f"5. Aggregate for web: python tools/aggregate_checks.py checks/")

if __name__ == "__main__":
    migrate_catalog()
