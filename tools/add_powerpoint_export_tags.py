#!/usr/bin/env python3
"""
Add PowerPoint Export Tags to DRIVE Checks

Migrates YAML check files from schema v2.0 to v2.1 by adding intelligent
powerpoint_export configuration based on severity, level, and business impact.

Usage:
    python3 add_powerpoint_export_tags.py                  # All checks
    python3 add_powerpoint_export_tags.py --dry-run        # Preview only
    python3 add_powerpoint_export_tags.py checks/SP-*.yaml # Specific files
    python3 add_powerpoint_export_tags.py --priority-mapping custom.json
"""

import yaml
import sys
import os
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Default priority assignment logic
PRIORITY_RULES = {
    # (min_level, max_level, severity) -> priority
    # Level 1 checks
    (1, 1, 'Critical'): '1-PrimaryFocus',
    (1, 1, 'High'): '1-PrimaryFocus',
    (1, 1, 'Medium'): '2-SecondaryFocus',
    (1, 1, 'Low'): '2-SecondaryFocus',

    # Level 2 checks
    (2, 2, 'Critical'): '1-PrimaryFocus',
    (2, 2, 'High'): '2-SecondaryFocus',
    (2, 2, 'Medium'): '2-SecondaryFocus',
    (2, 2, 'Low'): '3-AdditionalFinding',

    # Level 3 checks
    (3, 3, 'Critical'): '2-SecondaryFocus',
    (3, 3, 'High'): '2-SecondaryFocus',
    (3, 3, 'Medium'): '3-AdditionalFinding',
    (3, 3, 'Low'): '3-AdditionalFinding',

    # Level 4-5 checks (enhanced/state-of-the-art)
    (4, 5, 'Critical'): '2-SecondaryFocus',
    (4, 5, 'High'): '3-AdditionalFinding',
    (4, 5, 'Medium'): '3-AdditionalFinding',
    (4, 5, 'Low'): '3-AdditionalFinding',
}

# Keywords that indicate executive relevance
EXECUTIVE_KEYWORDS = [
    'anonymous', 'public', 'breach', 'exposure', 'confidential', 'sensitive',
    'admin', 'global', 'privileged', 'mfa', 'multi-factor', 'authentication',
    'compliance', 'gdpr', 'hipaa', 'sox', 'pci', 'regulation',
    'stale', 'orphaned', 'unmonitored', 'no owner', 'missing owner'
]

# Keywords that indicate technical detail (demote)
TECHNICAL_KEYWORDS = [
    'protocol', 'cipher', 'algorithm', 'registry', 'configuration drift',
    'low severity', 'informational', 'individual file'
]

def determine_priority(check: Dict) -> str:
    """Determine PowerPoint priority based on check characteristics"""

    # Get first threshold (usually most severe)
    thresholds = check.get('level_thresholds', [])
    if not thresholds:
        return '3-AdditionalFinding'

    # Get minimum level and maximum severity
    min_level = min(t.get('level', 5) for t in thresholds)
    max_severity = None
    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

    for threshold in thresholds:
        sev = threshold.get('severity', 'Low')
        if max_severity is None or severity_order.get(sev, 3) < severity_order.get(max_severity, 3):
            max_severity = sev

    if max_severity is None:
        max_severity = 'Low'

    # Match against priority rules
    for (min_lvl, max_lvl, severity), priority in PRIORITY_RULES.items():
        if min_lvl <= min_level <= max_lvl and severity == max_severity:
            base_priority = priority
            break
    else:
        # Default fallback
        base_priority = '3-AdditionalFinding'

    # Adjust based on executive keywords
    title_lower = check.get('title', '').lower()
    desc_lower = check.get('detailed_description', '').lower()

    # Promote if executive keywords present
    if any(keyword in title_lower or keyword in desc_lower for keyword in EXECUTIVE_KEYWORDS):
        if base_priority == '3-AdditionalFinding':
            base_priority = '2-SecondaryFocus'
        elif base_priority == '2-SecondaryFocus' and min_level == 1:
            base_priority = '1-PrimaryFocus'

    # Demote if technical keywords present
    if any(keyword in title_lower or keyword in desc_lower for keyword in TECHNICAL_KEYWORDS):
        if base_priority == '2-SecondaryFocus':
            base_priority = '3-AdditionalFinding'
        elif base_priority == '1-PrimaryFocus' and min_level > 1:
            base_priority = '2-SecondaryFocus'

    return base_priority

def determine_slide_section(priority: str, check: Dict) -> str:
    """Determine recommended slide section"""

    if priority == '1-PrimaryFocus':
        return "Critical Findings"
    elif priority == '2-SecondaryFocus':
        # Check for compliance keywords
        desc = check.get('detailed_description', '').lower()
        if 'compliance' in desc or 'regulation' in desc or 'gdpr' in desc:
            return "Compliance Gaps"
        else:
            return "High Priority Risks"
    elif priority == '3-AdditionalFinding':
        return "Additional Context"
    else:
        return "Technical Details"

def determine_chart_visualization(check: Dict) -> str:
    """Determine recommended chart type"""

    thresholds = check.get('level_thresholds', [])

    # If multiple thresholds at different levels, trend chart
    if len(thresholds) > 1:
        levels = [t.get('level') for t in thresholds]
        if len(set(levels)) > 1:
            return "trend"

    # Default to gauge for threshold-based checks
    return "gauge"

def create_executive_summary(check: Dict) -> str:
    """Create concise executive summary from check description"""

    detailed = check.get('detailed_description', '')
    short = check.get('short_description', '')

    # Prefer detailed description, but truncate if needed
    summary = detailed if detailed else short

    # Take first sentence only
    if '.' in summary:
        summary = summary.split('.')[0] + '.'

    # Truncate if too long
    if len(summary) > 200:
        summary = summary[:197] + '...'

    return summary

def add_powerpoint_export(check: Dict) -> Dict:
    """Add powerpoint_export section to check"""

    # Skip if already has powerpoint_export
    if 'powerpoint_export' in check:
        return check

    # Determine priority
    priority = determine_priority(check)

    # Build powerpoint_export section
    powerpoint_export = {
        'include': priority != '4-Exclude',
        'priority': priority,
        'slide_section': determine_slide_section(priority, check),
        'chart_visualization': determine_chart_visualization(check)
    }

    # Add executive summary for primary focus checks
    if priority == '1-PrimaryFocus':
        powerpoint_export['executive_summary'] = create_executive_summary(check)

    check['powerpoint_export'] = powerpoint_export

    # Update schema version
    if 'metadata' in check:
        check['metadata']['schema_version'] = '2.1'
        check['metadata']['last_updated'] = datetime.utcnow().isoformat() + 'Z'

        # Add change history
        if 'change_history' not in check['metadata']:
            check['metadata']['change_history'] = []

        check['metadata']['change_history'].append({
            'date': datetime.utcnow().strftime('%Y-%m-%d'),
            'version': check['metadata'].get('version', '1.0.0'),
            'change': 'Added PowerPoint export tagging (schema v2.1)',
            'author': 'PowerPoint-Migration-Script'
        })

    return check

def process_check_file(file_path: str, dry_run: bool = False) -> bool:
    """Process a single check file"""

    try:
        # Read existing check
        with open(file_path, 'r') as f:
            check = yaml.safe_load(f)

        # Check if already has powerpoint_export
        schema_version = check.get('metadata', {}).get('schema_version', '2.0')
        has_pptx = 'powerpoint_export' in check

        if has_pptx:
            print(f"⏭️  {file_path}: Already has powerpoint_export (skipping)")
            return False

        # Add powerpoint_export section
        updated_check = add_powerpoint_export(check)

        # Get priority for display
        priority = updated_check['powerpoint_export']['priority']

        if dry_run:
            print(f"🔍 {file_path}: Would add priority={priority}")
            return False
        else:
            # Write updated check
            with open(file_path, 'w') as f:
                yaml.dump(updated_check, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            print(f"✅ {file_path}: Added priority={priority}")
            return True

    except Exception as e:
        print(f"❌ {file_path}: Error - {e}")
        return False

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Add PowerPoint export tags to DRIVE checks (schema v2.0 → v2.1)'
    )
    parser.add_argument(
        'checks',
        nargs='*',
        help='Specific YAML check files to process (default: all checks in checks/)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    parser.add_argument(
        '--priority-mapping',
        type=str,
        help='JSON file with custom priority mapping rules'
    )

    args = parser.parse_args()

    # Load custom priority mapping if provided
    if args.priority_mapping:
        try:
            with open(args.priority_mapping, 'r') as f:
                custom_mapping = json.load(f)
                PRIORITY_RULES.update(custom_mapping)
                print(f"📋 Loaded custom priority mapping from {args.priority_mapping}")
        except Exception as e:
            print(f"⚠️  Failed to load custom mapping: {e}")

    # Determine which files to process
    if args.checks:
        # Process specific files
        yaml_files = [Path(f) for f in args.checks]
    else:
        # Process all checks in checks/ directory
        checks_dir = Path(__file__).parent.parent / 'checks'
        if not checks_dir.exists():
            print(f"❌ Checks directory not found: {checks_dir}")
            sys.exit(1)

        yaml_files = list(checks_dir.glob("*.yaml")) + list(checks_dir.glob("*.yml"))

    if len(yaml_files) == 0:
        print("⚠️  No YAML files found to process")
        sys.exit(0)

    print(f"\n🚀 Processing {len(yaml_files)} check files...")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")
    print()

    # Process each file
    updated_count = 0
    skipped_count = 0
    error_count = 0

    for yaml_file in sorted(yaml_files):
        try:
            result = process_check_file(str(yaml_file), dry_run=args.dry_run)
            if result:
                updated_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"❌ {yaml_file}: Unexpected error - {e}")
            error_count += 1

    # Summary
    print()
    print("=" * 70)
    print("📊 Migration Summary:")
    print(f"   ✅ Updated: {updated_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Total: {len(yaml_files)}")

    if args.dry_run:
        print("\n🔍 DRY RUN COMPLETE - Run without --dry-run to apply changes")

    print("=" * 70)

    sys.exit(0 if error_count == 0 else 1)

if __name__ == "__main__":
    main()
