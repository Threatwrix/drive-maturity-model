#!/usr/bin/env python3
"""
Merge new risk data into DRIVE catalog format
"""
import csv
import json
from datetime import datetime
import os

def map_drive_stage_to_pillar(stage):
    """Map DRIVE Stage (1-3) to drive_pillar (D,R,I,V,E)"""
    # For now, mapping based on category and stage
    # This should be refined based on business logic
    stage_mapping = {
        1: "D",  # Data - foundational data protection
        2: "R",  # Risk - risk management and controls  
        3: "I"   # Identity - advanced identity controls
    }
    return stage_mapping.get(stage, "E")  # Default to E (Exposure)

def normalize_platform(platform):
    """Normalize platform names to match existing convention"""
    platform_map = {
        "Exchange Online": "Exchange Online",
        "File System": "File System", 
        "OneDrive": "OneDrive",
        "SharePoint": "SharePoint"
    }
    return platform_map.get(platform, platform)

def convert_severity(severity):
    """Ensure severity is properly formatted"""
    if not severity or severity == "":
        return "Medium"  # Default
    return severity.title()

def merge_catalogs():
    """Merge new risk data into DRIVE catalog format"""
    
    # Read the new comprehensive risk data
    new_risks = []
    with open('/Users/jeff.warren/Projects/drive-risk-catalog/catalog/Risks.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_risks.append(row)
    
    print(f"Found {len(new_risks)} risk checks to merge")
    
    # Transform to DRIVE catalog format
    drive_catalog = []
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    for risk in new_risks:
        # Skip empty rows
        if not risk.get('Check ID') or risk['Check ID'] == '':
            continue
            
        # Map DRIVE Stage to pillar
        drive_stage = risk.get('DRIVE Stage', '')
        try:
            stage_num = int(drive_stage) if drive_stage else 1
        except ValueError:
            stage_num = 1
            
        pillar = map_drive_stage_to_pillar(stage_num)
        
        # Calculate drive_weight from Check Score Deduction
        score_deduction = risk.get('Check Score Deduction (X)', '0')
        try:
            deduction = float(score_deduction) if score_deduction else 0
            # Normalize to 0-1 scale (assuming max deduction ~20)
            drive_weight = min(deduction / 20.0, 1.0) 
        except ValueError:
            drive_weight = 0.5  # Default weight
        
        # Create DRIVE catalog entry
        catalog_entry = {
            'version': '1.0.0',
            'last_updated_utc': current_time,
            'check_id': risk.get('Check ID', ''),
            'title': risk.get('Check', ''),
            'category': risk.get('Category', 'Access Control'),
            'platform': normalize_platform(risk.get('Platform', '')),
            'severity': convert_severity(risk.get('Severity', 'Medium')),
            'description': risk.get('Business-Friendly Description', ''),
            'logic': f"Exploitability: {risk.get('Exploitability', 'Medium')}, Business Impact: {risk.get('Business Impact Level', 'Medium')}",
            'data_points': f"Score Deduction: {score_deduction}",
            'automatable': 'true',  # Assume automatable per PRD
            'owner': 'DRIVE-Team',
            'status': 'active',
            'notes': '',
            'drive_pillar': pillar,
            'drive_maturity_min': stage_num,
            'drive_weight': round(drive_weight, 2),
            'nist_csf_function': 'PROTECT',  # Most are access control
            'nist_csf_id': risk.get('NIST SP 800-53 (Rev.5)', '').split(',')[0].strip() if risk.get('NIST SP 800-53 (Rev.5)') else '',
            'cis_v8_control': risk.get('CIS Controls v8', '').split(',')[0].strip() if risk.get('CIS Controls v8') else '',
            'cis_m365_benchmark': '',  # Could be derived from existing data
            'iso_27001_annex': risk.get('ISO 27001', '').split(',')[0].strip() if risk.get('ISO 27001') else '',
            'anssi_level': '',
            'pingcastle_topic': '',
            'tags': f"mitre:{risk.get('MITRE ATT&CK', '')}" if risk.get('MITRE ATT&CK') else ''
        }
        
        drive_catalog.append(catalog_entry)
    
    print(f"Converted {len(drive_catalog)} entries to DRIVE format")
    
    # Write merged catalog to CSV
    if drive_catalog:
        fieldnames = drive_catalog[0].keys()
        with open('/Users/jeff.warren/Projects/drive-risk-catalog/catalog/drive_risk_catalog.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(drive_catalog)
        
        print("✅ Updated drive_risk_catalog.csv")
        
        # Generate JSON version
        with open('/Users/jeff.warren/Projects/drive-risk-catalog/catalog/drive_risk_catalog.json', 'w') as f:
            json.dump(drive_catalog, f, indent=2)
        
        print("✅ Generated drive_risk_catalog.json")
        
        # Print summary stats
        platforms = {}
        severities = {}
        pillars = {}
        
        for entry in drive_catalog:
            platform = entry['platform']
            severity = entry['severity'] 
            pillar = entry['drive_pillar']
            
            platforms[platform] = platforms.get(platform, 0) + 1
            severities[severity] = severities.get(severity, 0) + 1
            pillars[pillar] = pillars.get(pillar, 0) + 1
        
        print(f"\n📊 DRIVE Catalog Summary:")
        print(f"Total checks: {len(drive_catalog)}")
        print(f"Platforms: {dict(platforms)}")
        print(f"Severities: {dict(severities)}")
        print(f"DRIVE Pillars: {dict(pillars)}")
    
    return True

if __name__ == "__main__":
    try:
        merge_catalogs()
        print("\n🎉 Catalog merge completed successfully!")
    except Exception as e:
        print(f"❌ Error during merge: {e}")
        raise