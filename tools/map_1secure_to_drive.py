#!/usr/bin/env python3
"""
Map 1Secure risks to DRIVE catalog checks and generate integration analysis.
"""

import os
import yaml
import csv
import json
from collections import defaultdict

# 1Secure risk mappings to DRIVE check IDs
MAPPINGS = {
    # Data Category (SharePoint/OneDrive)
    "Third-Party Applications Allowed": ["SP-ES-006"],  # Third-Party App Access
    "High Risk Permissions on Documents": ["SP-AC-001", "OD-AC-001"],  # Overly Permissive Access
    "Stale Direct User Permissions": ["SP-AC-006", "OD-AC-003"],  # Stale Access Rights
    "Sites with Broken Permissions Inheritance": ["SP-AC-009"],  # Broken Permission Inheritance
    "External and Anonymous Sharing of Sensitive Data": ["SP-ES-001", "SP-ES-002", "OD-ES-001"],  # Anonymous/External Links to Sensitive
    "Unlabeled Sensitive Files": ["SP-DC-001", "OD-DC-001"],  # Unlabeled Sensitive Content
    "Stale User Access to Sensitive Data": ["SP-AC-006", "OD-AC-003"],  # Stale Access to Sensitive
    "Open Access to Sensitive Data": ["SP-AC-002", "OD-AC-002"],  # Everyone Access to Sensitive
    "High-Risk Permissions to Sensitive Data": ["SP-AC-001", "OD-AC-001"],  # Full Control to Sensitive

    # Identity Category (Entra ID / Active Directory)
    "User Accounts with \"Password Never Expires\"": ["AD-PW-001"],  # Password Never Expires
    "User Accounts with \"Password Not Required\"": ["AD-PW-002"],  # Password Not Required
    "Inactive User Accounts": ["AD-AC-001"],  # Inactive User Accounts
    "User Accounts with Administrative Permissions": ["AD-PR-001"],  # Excessive Admin Rights
    "Administrative Groups": ["AD-PR-002"],  # Excessive Admin Groups
    "Empty Security Groups": ["AD-AC-007"],  # Empty Security Groups
    "Dangerous Default Permissions": ["AD-PR-005"],  # Dangerous Default Privileges
    "Improper Number of Global Administrators": ["AD-PR-003"],  # Excessive Global Admins
    "Conditional Access Policy Disables Admin Token Persistence": ["AD-CF-001"],  # Missing Conditional Access
    "Self-Serve Password Reset is Not Enabled": ["AD-CF-002"],  # SSPR Not Enabled
    "MS Graph Powershell Service Principal Assignment Not Enforced": ["AD-CF-003"],  # Service Principal Misconfiguration
    "Stale Guest Accounts": ["AD-AC-002"],  # Stale Guest Accounts
    "User Accounts with \"No MFA Configured\"": ["AD-AU-001"],  # MFA Not Configured
    "User Accounts Created via Email Verified Self-Service Creation": ["AD-AC-008"],  # Self-Service Account Creation
    "Global Administrators": ["AD-PR-003"],  # Global Admin Count
    "Unusual Primary Group on Computer Account": ["AD-AC-009"],  # Computer Account Misconfiguration
    "Restriction of Dangerous Privileges for Standard Users": ["AD-PR-005"],  # Dangerous Privileges
    "Review of Delegated Permissions for Standard Users on Organizational Units": ["AD-PR-006"],  # OU Delegation Issues
    "Same Domain SID History Association": ["AD-VL-001"],  # SID History Abuse
    "Well-Known SIDs in SID History": ["AD-VL-001"],  # SID History Abuse
    "Administrative Accounts Susceptible to Kerberoasting": ["AD-VL-002"],  # Kerberoasting Vulnerability
    "Domain Controller RPC Coercion": ["AD-VL-003"],  # DC RPC Coercion
    "Admin Accounts with Email Access": ["AD-PR-007"],  # Admin Email Access

    # Infrastructure Category
    "Disabled Computer Accounts": ["AD-AC-010"],  # Disabled Computer Accounts
    "Inactive Computer Accounts": ["AD-AC-011"],  # Inactive Computer Accounts
    "Unified Audit Log Search is Not Enabled": ["AD-CF-004"],  # Audit Logging Not Enabled
    "Conditional Access Policies and Microsoft Secure Defaults status": ["AD-CF-001"],  # Conditional Access Missing
    "Expired Domain Registrations Found": ["AD-CF-005"],  # Domain Registration Issues
    "MS Graph Powershell Service Principal Configuration Missing": ["AD-CF-003"],  # Service Principal Config
    "Legacy authentication protocols enabled": ["AD-AU-002"],  # Legacy Auth Protocols
    "Domain Controller SMB v1 Vulnerability": ["AD-VL-004"],  # SMBv1 Vulnerability
    "Domain Controller Registration Status": ["AD-CF-006"],  # DC Registration
    "Domain Controller Logon Privileges Restriction": ["AD-PR-008"],  # DC Logon Restrictions
    "Domain Controller Ownership Verification": ["AD-CF-007"],  # DC Ownership
    "ESC1: Vulnerable Subject Control in Certificate Templates": ["AD-VL-005"],  # ADCS ESC1
    "ESC2: Vulnerable EKU Configurations in Certificate Templates": ["AD-VL-006"],  # ADCS ESC2
    "ESC4: Low-Privileged User Access to Published Certificate Templates": ["AD-VL-007"],  # ADCS ESC4
    "ESC3: Misconfigured Agent Enrollment Templates": ["AD-VL-008"],  # ADCS ESC3
    "Obsolete Windows Server 2012 Member Servers": ["AD-CF-008"],  # Obsolete OS Versions
    "Obsolete Windows 2012 Domain Controllers": ["AD-CF-009"],  # Obsolete DC OS
    "OU Accidental Deletion Protection": ["AD-CF-010"],  # OU Protection
    "Weak TLS Protocols used by LDAPS": ["AD-VL-009"],  # Weak TLS
    "Outdated Domain Functional Level (2012R2)": ["AD-CF-011"],  # Outdated Functional Level
}

def load_drive_checks(checks_dir='checks'):
    """Load all DRIVE checks from YAML files."""
    checks = {}
    for filename in os.listdir(checks_dir):
        if filename.endswith('.yaml'):
            filepath = os.path.join(checks_dir, filename)
            with open(filepath, 'r') as f:
                check = yaml.safe_load(f)
                checks[check['check_id']] = check
    return checks

def load_1secure_risks(csv_path='analysis/1secure_risks.csv'):
    """Load 1Secure risks from CSV."""
    risks = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            risks.append(row)
    return risks

def analyze_coverage(mappings, drive_checks, secure_risks):
    """Analyze coverage of 1Secure risks against DRIVE catalog."""

    # Statistics
    total_1secure_risks = len(secure_risks)
    mapped_1secure_risks = len([r for r in secure_risks if r['Metric'] in mappings])

    # Get unique DRIVE check IDs that are covered
    covered_drive_checks = set()
    for check_ids in mappings.values():
        covered_drive_checks.update(check_ids)

    total_drive_checks = len(drive_checks)
    covered_count = len([c for c in covered_drive_checks if c in drive_checks])

    # Platform breakdown
    platform_coverage = defaultdict(lambda: {'covered': 0, 'total': 0})
    for check_id, check in drive_checks.items():
        platform = check['platform']
        platform_coverage[platform]['total'] += 1
        if check_id in covered_drive_checks:
            platform_coverage[platform]['covered'] += 1

    # Category breakdown
    category_coverage = defaultdict(lambda: {'covered': 0, 'total': 0})
    for check_id, check in drive_checks.items():
        category = check['category']
        category_coverage[category]['total'] += 1
        if check_id in covered_drive_checks:
            category_coverage[category]['covered'] += 1

    return {
        '1secure_total': total_1secure_risks,
        '1secure_mapped': mapped_1secure_risks,
        'drive_total': total_drive_checks,
        'drive_covered': covered_count,
        'platform_coverage': dict(platform_coverage),
        'category_coverage': dict(category_coverage),
        'covered_check_ids': sorted(covered_drive_checks)
    }

def generate_mapping_report(mappings, drive_checks, secure_risks):
    """Generate detailed mapping report."""

    report = []
    report.append("# 1Secure to DRIVE Catalog Mapping Report\n")
    report.append("## Executive Summary\n")

    analysis = analyze_coverage(mappings, drive_checks, secure_risks)

    report.append(f"**1Secure Risks:** {analysis['1secure_total']} total")
    report.append(f"**1Secure Mapped:** {analysis['1secure_mapped']} ({analysis['1secure_mapped']/analysis['1secure_total']*100:.1f}%)\n")

    report.append(f"**DRIVE Checks:** {analysis['drive_total']} total")
    report.append(f"**DRIVE Covered by 1Secure:** {analysis['drive_covered']} ({analysis['drive_covered']/analysis['drive_total']*100:.1f}%)\n")

    report.append("## Platform Coverage\n")
    for platform, stats in sorted(analysis['platform_coverage'].items()):
        pct = stats['covered']/stats['total']*100 if stats['total'] > 0 else 0
        report.append(f"- **{platform}**: {stats['covered']}/{stats['total']} ({pct:.1f}%)")

    report.append("\n## Category Coverage\n")
    for category, stats in sorted(analysis['category_coverage'].items()):
        pct = stats['covered']/stats['total']*100 if stats['total'] > 0 else 0
        report.append(f"- **{category}**: {stats['covered']}/{stats['total']} ({pct:.1f}%)")

    report.append("\n## Detailed Mappings\n")

    # Group by 1Secure category
    by_category = defaultdict(list)
    for risk in secure_risks:
        by_category[risk['Category']].append(risk)

    for category in ['Data', 'Identity', 'Infrastructure']:
        report.append(f"\n### {category}\n")

        for risk in by_category[category]:
            metric = risk['Metric']
            report.append(f"\n**{metric}**")

            if metric in mappings:
                check_ids = mappings[metric]
                report.append(f"- Measure: {risk['Measure In']}")
                report.append(f"- Thresholds: Low={risk['Low']}, Medium={risk['Medium']}, High={risk['High']}")
                report.append(f"- Maps to DRIVE checks:")

                for check_id in check_ids:
                    if check_id in drive_checks:
                        check = drive_checks[check_id]
                        report.append(f"  - `{check_id}`: {check['title']} (Level {check.get('drive_maturity_min', 'N/A')})")
            else:
                report.append("- **NOT MAPPED** - May require new DRIVE check")

    report.append("\n## Unmapped DRIVE Checks (Available for Future Integration)\n")

    unmapped = [check_id for check_id in drive_checks.keys() if check_id not in analysis['covered_check_ids']]

    platform_unmapped = defaultdict(list)
    for check_id in sorted(unmapped):
        check = drive_checks[check_id]
        platform_unmapped[check['platform']].append((check_id, check))

    for platform, checks in sorted(platform_unmapped.items()):
        report.append(f"\n### {platform} ({len(checks)} checks)\n")
        for check_id, check in checks[:10]:  # Show first 10
            report.append(f"- `{check_id}`: {check['title']}")
        if len(checks) > 10:
            report.append(f"- ... and {len(checks)-10} more")

    return '\n'.join(report)

def generate_integration_data(mappings, drive_checks):
    """Generate JSON data for Replit integration."""

    integration_data = {
        'version': '1.0',
        'source': '1Secure',
        'mappings': []
    }

    for metric, check_ids in sorted(mappings.items()):
        mapping_entry = {
            '1secure_metric': metric,
            'drive_checks': []
        }

        for check_id in check_ids:
            if check_id in drive_checks:
                check = drive_checks[check_id]
                mapping_entry['drive_checks'].append({
                    'check_id': check_id,
                    'title': check.get('title', 'Unknown'),
                    'platform': check.get('platform', 'Unknown'),
                    'category': check.get('category', 'Unknown'),
                    'severity': check.get('severity', 'Medium'),
                    'drive_maturity_min': check.get('drive_maturity_min', 3),
                    'drive_pillar': check.get('drive_pillar', 'D'),
                    'level_thresholds': check.get('level_thresholds', [])
                })

        integration_data['mappings'].append(mapping_entry)

    return integration_data

def main():
    print("Loading DRIVE checks...")
    drive_checks = load_drive_checks()
    print(f"Loaded {len(drive_checks)} DRIVE checks")

    print("\nLoading 1Secure risks...")
    secure_risks = load_1secure_risks()
    print(f"Loaded {len(secure_risks)} 1Secure risks")

    print("\nGenerating mapping report...")
    report = generate_mapping_report(MAPPINGS, drive_checks, secure_risks)

    with open('analysis/1secure_mapping_report.md', 'w') as f:
        f.write(report)
    print("Report saved to: analysis/1secure_mapping_report.md")

    print("\nGenerating integration data...")
    integration_data = generate_integration_data(MAPPINGS, drive_checks)

    with open('analysis/1secure_integration.json', 'w') as f:
        json.dump(integration_data, f, indent=2)
    print("Integration data saved to: analysis/1secure_integration.json")

    # Print summary
    analysis = analyze_coverage(MAPPINGS, drive_checks, secure_risks)
    print("\n" + "="*60)
    print("COVERAGE SUMMARY")
    print("="*60)
    print(f"1Secure Risks Mapped: {analysis['1secure_mapped']}/{analysis['1secure_total']} ({analysis['1secure_mapped']/analysis['1secure_total']*100:.1f}%)")
    print(f"DRIVE Checks Covered: {analysis['drive_covered']}/{analysis['drive_total']} ({analysis['drive_covered']/analysis['drive_total']*100:.1f}%)")
    print("="*60)

if __name__ == '__main__':
    main()
