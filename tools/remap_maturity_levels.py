#!/usr/bin/env python3
"""
Remap DRIVE risk checks to new threat-focused maturity levels
Based on threat timeline and exploitability rather than arbitrary progression
"""
import csv
from datetime import datetime

def determine_threat_level(row):
    """
    Map risk to threat-focused maturity level based on:
    - Severity (Critical, High, Medium, Low)
    - Exploitability timeline 
    - Risk type and impact
    """
    check_id = row.get('check_id', '')
    title = row.get('title', '').lower()
    severity = row.get('severity', 'Medium')
    description = row.get('description', '').lower()
    
    # Level 1: Critical Exposure (Immediate Threat)
    # Critical severity + immediate exploitability
    if severity == 'Critical':
        return 1
    
    # Anonymous access = immediate threat
    if any(keyword in title or keyword in description for keyword in [
        'anonymous', 'anyone links', 'open access', 'public', 'anyone link',
        'clear text password', 'unconstrained delegation', 'admin$ share',
        'password not required', 'reversible encryption'
    ]):
        return 1
        
    # Critical AD misconfigurations
    if any(keyword in check_id for keyword in ['AD-008', 'AD-011', 'AD-016']) or \
       any(keyword in title for keyword in ['krbtgt', 'unconstrained delegation', 'domain admin']):
        return 1
    
    # Level 2: High Risk Mitigated (Short-term Protection) 
    # High severity privilege/access issues
    if severity == 'High':
        # Admin/privilege related high risks
        if any(keyword in title or keyword in description for keyword in [
            'admin', 'privileged', 'password never expires', 'mfa', 'delegation',
            'guest', 'external', 'service account', 'spn', 'kerberoasting'
        ]):
            return 2
        # Other high severity that could be level 3
        return 3
    
    # Guest and external sharing (even if medium severity)
    if any(keyword in title for keyword in [
        'guest', 'external', 'sharing', 'recipient', 'visitor'
    ]):
        return 2
        
    # Level 3: Standard Security Baseline (Default Plus)
    # Medium severity baseline controls
    if severity == 'Medium':
        # Stale/inactive resources - Level 3 baseline
        if any(keyword in title for keyword in [
            'stale', 'inactive', 'old', 'missing owner', 'orphaned site',
            'broken inheritance', 'excessive', 'bloat'
        ]):
            return 3
        return 3
    
    # Level 4: Enhanced Security Posture (Proactive Management)  
    # Advanced controls and monitoring
    if any(keyword in title or keyword in description for keyword in [
        'recently created', 'resource-based', 'trusted for delegation',
        'sensitive data', 'multiple domains', 'personal employee drives'
    ]):
        return 4
        
    # Level 5: State-of-the-Art Security (Continuous Excellence)
    # Predictive and advanced security
    if any(keyword in title for keyword in [
        'risky constrained delegation', 'preauthentication', 'aes keys',
        'communication sites', 'shared channels'
    ]):
        return 5
    
    # Default cases
    if severity == 'Low':
        return 3  # Most low severity = baseline
    
    return 3  # Default to baseline level

def remap_catalog():
    """Remap all 117 risk checks to new maturity levels"""
    
    # Read current catalog
    risks = []
    with open('catalog/drive_risk_catalog.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            risks.append(row)
    
    print(f"Processing {len(risks)} risk checks...")
    
    # Track level changes
    level_changes = {}
    level_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    # Remap each risk
    for risk in risks:
        old_level = risk.get('drive_maturity_min', '1')
        new_level = determine_threat_level(risk)
        
        # Update the record
        risk['drive_maturity_min'] = str(new_level)
        
        # Track changes
        if old_level != str(new_level):
            level_changes[risk['check_id']] = {
                'old': old_level,
                'new': new_level,
                'title': risk['title'][:50] + '...' if len(risk['title']) > 50 else risk['title'],
                'severity': risk['severity']
            }
        
        level_distribution[new_level] += 1
    
    # Write updated catalog
    fieldnames = risks[0].keys()
    with open('catalog/drive_risk_catalog.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(risks)
    
    # Print summary
    print(f"\n✅ Remapped {len(risks)} risk checks to threat-focused levels")
    print(f"\n📊 New Level Distribution:")
    for level, count in level_distribution.items():
        level_names = {
            1: "Critical Exposure (Immediate Threat)",
            2: "High Risk Mitigated (Short-term Protection)", 
            3: "Standard Security Baseline (Default Plus)",
            4: "Enhanced Security Posture (Proactive Management)",
            5: "State-of-the-Art Security (Continuous Excellence)"
        }
        print(f"  Level {level}: {count:2d} checks - {level_names[level]}")
    
    # Show significant changes
    if level_changes:
        print(f"\n🔄 Significant Level Changes ({len(level_changes)} total):")
        for check_id, change in list(level_changes.items())[:10]:  # Show first 10
            print(f"  {check_id}: L{change['old']} → L{change['new']} | {change['severity']:8} | {change['title']}")
        if len(level_changes) > 10:
            print(f"  ... and {len(level_changes) - 10} more changes")
    
    return True

if __name__ == "__main__":
    try:
        remap_catalog()
        print(f"\n🎉 Catalog remapping completed successfully!")
        print(f"Updated catalog available at: catalog/drive_risk_catalog.csv")
    except Exception as e:
        print(f"❌ Error during remapping: {e}")
        raise