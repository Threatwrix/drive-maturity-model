#!/usr/bin/env python3
"""
Aggregate YAML check files into single JSON for GitHub Pages
"""
import yaml
import json
import sys
from pathlib import Path

def load_yaml_check(file_path):
    """Load and parse a YAML check file"""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def simplify_check_for_web(check):
    """
    Simplify check structure for web display
    Keep essential fields, summarize complex ones
    """
    # Extract first threshold for backwards compatibility
    first_threshold = check['level_thresholds'][0] if check.get('level_thresholds') else {}

    return {
        'check_id': check['check_id'],
        'title': check['title'],
        'short_description': check.get('short_description', ''),
        'description': check.get('detailed_description', check.get('short_description', '')),
        'category': check['category'],
        'platform': check['platform'],
        'severity': first_threshold.get('severity', 'Medium'),
        'drive_pillar': check['drive_pillars'][0] if check.get('drive_pillars') else '',
        'drive_maturity_min': first_threshold.get('level', 1),
        'drive_weight': first_threshold.get('points_deduction', 0) / 100.0,  # Normalize
        'automatable': check.get('automatable', True),
        'status': check.get('status', 'active'),

        # Framework mappings - simplified
        'nist_csf_function': check.get('framework_mappings', {}).get('nist_csf', {}).get('function', ''),
        'nist_csf_id': ', '.join(check.get('framework_mappings', {}).get('nist_csf', {}).get('controls', [])),
        'cis_v8_control': ', '.join(check.get('framework_mappings', {}).get('cis_v8', {}).get('controls', [])),
        'cis_m365_benchmark': ', '.join(check.get('framework_mappings', {}).get('cis_m365', {}).get('recommendations', [])),
        'iso_27001_annex': ', '.join(check.get('framework_mappings', {}).get('iso_27001', {}).get('controls', [])),

        # Metadata
        'last_updated': check.get('metadata', {}).get('last_reviewed', ''),

        # Include level thresholds for detail view
        'level_thresholds': check.get('level_thresholds', []),

        # Tags
        'tags': ', '.join(check.get('framework_mappings', {}).get('mitre_attack', {}).get('techniques', []))
    }

def aggregate_checks(checks_dir):
    """Aggregate all YAML checks into single JSON"""
    checks_path = Path(checks_dir)

    if not checks_path.exists():
        print(f"Error: Checks directory not found: {checks_dir}")
        return []

    yaml_files = list(checks_path.glob("*.yaml")) + list(checks_path.glob("*.yml"))

    if len(yaml_files) == 0:
        print(f"Warning: No YAML files found in {checks_dir}")
        # Fall back to loading from CSV if it exists
        return []

    aggregated = []
    errors = []

    for yaml_file in sorted(yaml_files):
        try:
            check = load_yaml_check(yaml_file)
            simplified = simplify_check_for_web(check)
            aggregated.append(simplified)
            print(f"✓ Loaded {check['check_id']}")
        except Exception as e:
            errors.append(f"✗ Error loading {yaml_file.name}: {e}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"Aggregated {len(aggregated)} checks from {len(yaml_files)} YAML files")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors:
            print(f"  {error}")
    print(f"{'='*60}\n")

    return aggregated

def main():
    # Get checks directory
    checks_dir = sys.argv[1] if len(sys.argv) > 1 else 'checks'

    # Aggregate checks
    aggregated = aggregate_checks(checks_dir)

    if len(aggregated) == 0:
        print("Warning: No checks were aggregated. Falling back to existing catalog.")
        # Try to use existing catalog as fallback
        try:
            with open('catalog/drive_risk_catalog.json', 'r') as f:
                aggregated = json.load(f)
            print(f"Loaded {len(aggregated)} checks from existing catalog")
        except:
            print("Error: No checks available")
            sys.exit(1)

    # Create docs/catalog directory if needed
    Path('docs/catalog').mkdir(parents=True, exist_ok=True)

    # Write aggregated JSON
    output_file = 'docs/catalog/drive_risk_catalog.json'
    with open(output_file, 'w') as f:
        json.dump(aggregated, f, indent=2)

    print(f"✅ Wrote {len(aggregated)} checks to {output_file}")

    # Also write summary statistics
    stats = {
        'total_checks': len(aggregated),
        'by_platform': {},
        'by_severity': {},
        'by_level': {},
        'by_pillar': {},
        'last_updated': aggregated[0].get('last_updated', '') if aggregated else ''
    }

    for check in aggregated:
        # Count by platform
        platform = check.get('platform', 'Unknown')
        stats['by_platform'][platform] = stats['by_platform'].get(platform, 0) + 1

        # Count by severity
        severity = check.get('severity', 'Unknown')
        stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1

        # Count by level
        level = check.get('drive_maturity_min', 0)
        stats['by_level'][f'Level {level}'] = stats['by_level'].get(f'Level {level}', 0) + 1

        # Count by pillar
        pillar = check.get('drive_pillar', 'Unknown')
        stats['by_pillar'][pillar] = stats['by_pillar'].get(pillar, 0) + 1

    stats_file = 'docs/catalog/stats.json'
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)

    print(f"✅ Wrote statistics to {stats_file}")

if __name__ == "__main__":
    main()
