#!/usr/bin/env python3
"""
Add Level 5 (State-of-the-Art) thresholds to selected 1Secure checks.
"""

import yaml
from datetime import datetime

# Level 5 threshold definitions
LEVEL5_ADDITIONS = {
    '1S-DATA-003': {
        'threshold_condition': '<1% of permissions are stale',
        'threshold_description': 'Stale Direct User Permissions at Level 5 - Continuous cleanup',
        'business_impact': 'Organizations achieving <1% stale permissions demonstrate automated access lifecycle management and continuous hygiene',
    },
    '1S-DATA-005': {
        'threshold_condition': '<1% of sensitive files shared externally/anonymously',
        'threshold_description': 'External and Anonymous Sharing of Sensitive Data at Level 5 - Strict control',
        'business_impact': 'Organizations achieving <1% external sharing demonstrate strict data governance and continuous monitoring',
    },
    '1S-DATA-006': {
        'threshold_condition': '<2% of sensitive files unlabeled',
        'threshold_description': 'Unlabeled Sensitive Files at Level 5 - Near-perfect classification',
        'business_impact': 'Organizations achieving <2% unlabeled demonstrate continuous data classification excellence and automated governance',
    },
    '1S-DATA-008': {
        'threshold_condition': '0% of sensitive data has open access',
        'threshold_description': 'Open Access to Sensitive Data at Level 5 - Perfect access control',
        'business_impact': 'Organizations achieving zero open access demonstrate perfect access control and continuous monitoring',
    },
    '1S-IDENTITY-003': {
        'threshold_condition': '<0.01% of user accounts inactive',
        'threshold_description': 'Inactive User Accounts at Level 5 - Automated lifecycle',
        'business_impact': 'Organizations achieving <0.01% inactive accounts demonstrate fully automated identity lifecycle management',
    },
    '1S-IDENTITY-006': {
        'threshold_condition': '0% of security groups are empty',
        'threshold_description': 'Empty Security Groups at Level 5 - Perfect hygiene',
        'business_impact': 'Organizations achieving zero empty groups demonstrate continuous group lifecycle management and automation',
    },
    '1S-IDENTITY-015': {
        'threshold_condition': '2-3 Global Administrators',
        'threshold_description': 'Global Administrators at Level 5 - Minimal privileged access',
        'business_impact': 'Organizations with 2-3 Global Admins demonstrate strict least privilege and just-in-time access patterns',
    },
    '1S-INFRA-001': {
        'threshold_condition': '<0.5% of computer accounts disabled',
        'threshold_description': 'Disabled Computer Accounts at Level 5 - Continuous cleanup',
        'business_impact': 'Organizations achieving <0.5% disabled accounts demonstrate automated computer lifecycle management',
    },
    '1S-INFRA-016': {
        'threshold_condition': '0 obsolete Windows Server 2012 member servers',
        'threshold_description': 'Obsolete Windows Server 2012 Member Servers at Level 5 - Always current',
        'business_impact': 'Organizations with zero obsolete systems demonstrate continuous patching, modern infrastructure, and zero technical debt',
    },
}

def add_level5_threshold(check_id):
    """Add Level 5 threshold to a check."""
    filepath = f'checks/{check_id}.yaml'

    try:
        with open(filepath, 'r') as f:
            check = yaml.safe_load(f)

        # Check if Level 5 already exists
        existing_levels = [t['level'] for t in check['level_thresholds']]
        if 5 in existing_levels:
            print(f'⚠️  {check_id}: Level 5 already exists, skipping')
            return False

        # Get Level 5 definition
        level5_def = LEVEL5_ADDITIONS.get(check_id)
        if not level5_def:
            print(f'❌ {check_id}: No Level 5 definition found')
            return False

        # Create Level 5 threshold
        level5_threshold = {
            'level': 5,
            'threshold_id': f'{check_id}-L5',
            'threshold_condition': level5_def['threshold_condition'],
            'threshold_description': level5_def['threshold_description'],
            'severity': 'Low',
            'business_impact': level5_def['business_impact'],
            'threat_timeline': 'Ongoing operational excellence',
            'attacker_profile': 'State-of-the-art security posture',
            'cvss_score': 2.0,
            'remediation_priority': 5
        }

        # Add to check
        check['level_thresholds'].append(level5_threshold)

        # Update metadata
        check['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        if 'change_history' in check['metadata']:
            check['metadata']['change_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d'),
                'version': '1.1.0',
                'change': 'Added Level 5 (State-of-the-Art) threshold',
                'author': 'DRIVE-1Secure-Integration'
            })
        check['metadata']['version'] = '1.1.0'

        # Add remediation step for Level 5
        if 'steps' in check['remediation']:
            check['remediation']['steps'].append({
                'step': 5,
                'level_target': [5],
                'action': 'Achieve Level 5 state-of-the-art security',
                'details': f'Use 1Secure to continuously monitor and maintain: {level5_def["threshold_condition"]}',
                'requires_manual': False,
                'manual_reason': 'Automated via 1Secure continuous monitoring'
            })

        # Write back
        with open(filepath, 'w') as f:
            yaml.dump(check, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

        print(f'✅ {check_id}: Added Level 5 threshold')
        return True

    except FileNotFoundError:
        print(f'❌ {check_id}: File not found at {filepath}')
        return False
    except Exception as e:
        print(f'❌ {check_id}: Error - {e}')
        return False

def main():
    print("="*70)
    print("Adding Level 5 (State-of-the-Art) Thresholds")
    print("="*70)
    print()

    updated_count = 0

    for check_id in sorted(LEVEL5_ADDITIONS.keys()):
        if add_level5_threshold(check_id):
            updated_count += 1

    print()
    print("="*70)
    print(f"✅ Updated {updated_count} checks with Level 5 thresholds")
    print("="*70)

if __name__ == '__main__':
    main()
