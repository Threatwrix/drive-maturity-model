# DRIVE Maturity Model - ANSSI-Inspired Multi-Level Architecture

## Overview

This document describes the redesigned DRIVE maturity model inspired by ANSSI/PingCastle's approach where:
- Each check can define multiple severity thresholds mapping to different maturity levels
- Organizations progress through levels 1-5 based on passing ALL checks at each level
- Visual control graph shows dependencies and progression paths

## Key Differences from Current Model

### Current Approach
- Each check maps to exactly ONE maturity level (`drive_maturity_min: 2`)
- Binary pass/fail per check
- Fixed level assignment

### New ANSSI-Inspired Approach
- Each check can define MULTIPLE thresholds across levels
- Progressive severity model (same check can block multiple levels with different thresholds)
- More nuanced measurement

## Example: Multi-Level Check Structure

### Example 1: Functional Forest Level (Inspired by ANSSI)

```yaml
check_id: AD-FL-001
title: "Functional levels of the forest"
category: "Configuration"
platform: "Active Directory"
description: "Forest functional level determines available AD features and security capabilities"

# Multi-level thresholds
level_thresholds:
  - level: 1
    threshold: "Forest functional level < Windows Server 2008"
    severity: "Critical"
    rationale: "Legacy functional levels lack modern security features (fine-grained password policies, advanced audit, etc.)"
    points_deduction: 20

  - level: 2
    threshold: "Forest functional level < Windows Server 2012 R2"
    severity: "High"
    rationale: "Missing authentication policies, protected users security group, and enhanced kerberos features"
    points_deduction: 10

  - level: 3
    threshold: "Forest functional level < Windows Server 2016"
    severity: "Medium"
    rationale: "Missing privileged access management features and enhanced credential protection"
    points_deduction: 5

  - level: 4
    threshold: "Forest functional level < Windows Server 2019"
    severity: "Low"
    rationale: "Missing latest security enhancements and modern authentication improvements"
    points_deduction: 2
```

### Example 2: Guest Account Access (Multi-Level)

```yaml
check_id: SP-ES-014
title: "Guest accounts with access to sensitive data"
category: "Access Control"
platform: "SharePoint"
description: "External guest accounts with access to classified or sensitive information"

level_thresholds:
  - level: 1
    threshold: "Guests have Full Control on sites containing Critical data"
    severity: "Critical"
    rationale: "External users can delete, modify, or exfiltrate critical business data"
    points_deduction: 25

  - level: 2
    threshold: "Guests have Edit permissions on sites containing Sensitive data"
    severity: "High"
    rationale: "External users can modify sensitive documents without proper governance"
    points_deduction: 15

  - level: 3
    threshold: "Guests have Read access to >100 files containing Confidential data"
    severity: "Medium"
    rationale: "Broad guest access increases exfiltration risk and compliance exposure"
    points_deduction: 8

  - level: 4
    threshold: "Guests exist without access review in past 90 days"
    severity: "Low"
    rationale: "Lack of periodic review may allow stale guest access to persist"
    points_deduction: 3
```

### Example 3: Anonymous Sharing Links (Multi-Level)

```yaml
check_id: SP-ES-001
title: "Anonymous sharing links enabled"
category: "Access Control"
platform: "SharePoint"
description: "Anyone links allow unauthenticated access to content"

level_thresholds:
  - level: 1
    threshold: "Anonymous links with Edit permissions exist on any content"
    severity: "Critical"
    rationale: "Unauthenticated users can modify or delete organizational data"
    points_deduction: 30

  - level: 1
    threshold: "Anonymous links exist for Critical or Highly Confidential data"
    severity: "Critical"
    rationale: "Public internet access to sensitive data creates immediate breach risk"
    points_deduction: 30

  - level: 2
    threshold: "Anonymous links exist for Confidential data (>10 files)"
    severity: "High"
    rationale: "Significant confidential data exposure through public links"
    points_deduction: 15

  - level: 3
    threshold: "Anonymous links exist without expiration (>50 links)"
    severity: "Medium"
    rationale: "Permanent public links create persistent exposure vectors"
    points_deduction: 8
```

## Updated Data Model

### Enhanced Check Schema

```yaml
# catalog/checks/SP-ES-001.yaml
check_id: "SP-ES-001"
title: "Anonymous sharing links enabled"
short_description: "Anyone links allow unauthenticated access"
detailed_description: |
  SharePoint and OneDrive support "Anyone" links that allow unauthenticated
  access from the public internet. This creates significant data exposure risk.

category: "Access Control"
platform: "SharePoint"
drive_pillars: ["D", "E"]  # Data Protection + Exposure Analysis
automatable: true
owner: "DRIVE-Team"
status: "active"

# Detection logic
detection:
  data_sources:
    - "SharePoint sharing links API"
    - "Microsoft Graph API - /shares"
  query_logic: |
    1. Enumerate all sharing links across tenant
    2. Filter for scope = 'anonymous'
    3. Check data classification labels
    4. Count links and assess permissions
  data_points_required:
    - "Sharing link scope"
    - "Link permissions (Read/Edit)"
    - "Target item classification"
    - "Link expiration date"
    - "Link creation date"

# Multi-level thresholds (ANSSI-style)
level_thresholds:
  - level: 1
    threshold_condition: "anonymous_links_with_edit > 0 OR anonymous_links_to_critical_data > 0"
    threshold_description: "Anonymous Edit links OR links to Critical data"
    severity: "Critical"
    business_impact: "Immediate data breach risk - public can modify/delete data"
    threat_timeline: "Exploitable within hours"
    points_deduction: 30
    remediation_priority: 1

  - level: 2
    threshold_condition: "anonymous_links_to_confidential_data > 10"
    threshold_description: ">10 anonymous links to Confidential data"
    severity: "High"
    business_impact: "Significant confidential data exposed to public internet"
    threat_timeline: "Exploitable within days"
    points_deduction: 15
    remediation_priority: 2

  - level: 3
    threshold_condition: "permanent_anonymous_links > 50"
    threshold_description: ">50 anonymous links without expiration"
    severity: "Medium"
    business_impact: "Persistent exposure vectors for data exfiltration"
    threat_timeline: "Exploitable within weeks/months"
    points_deduction: 8
    remediation_priority: 3

# Framework mappings
framework_mappings:
  nist_csf:
    function: "PROTECT"
    categories: ["PR.AC-4", "PR.DS-5"]
  cis_v8:
    controls: ["3.3", "14.6"]
  cis_m365:
    recommendations: ["2.1.1", "7.2.2"]
  iso_27001:
    controls: ["A.9.1.2", "A.13.2.1"]
  mitre_attack:
    techniques: ["T1530", "T1567"]
  gdpr:
    articles: ["Article 32 (Security of Processing)"]

# Remediation guidance
remediation:
  automated_fix_available: true
  fix_complexity: "Medium"
  estimated_time: "1-2 hours"
  prerequisites:
    - "SharePoint admin role"
    - "Data classification labels defined"
  steps:
    - step: 1
      action: "Review all anonymous links and identify business need"
      commands: []
    - step: 2
      action: "Disable anonymous sharing at tenant level"
      commands:
        - "Set-SPOTenant -SharingCapability ExternalUserSharingOnly"
    - step: 3
      action: "Configure link expiration policies"
      commands:
        - "Set-SPOTenant -RequireAnonymousLinksExpireInDays 30"
    - step: 4
      action: "Enable data classification requirements"
      commands:
        - "Set-SPOTenant -ConditionalAccessPolicy AllowLimitedAccess"

  policy_template: |
    # 1Secure Policy Template
    policy:
      name: "Disable Anonymous Sharing"
      scope: "SharePoint Online Tenant"
      settings:
        SharingCapability: "ExternalUserSharingOnly"
        RequireAnonymousLinksExpireInDays: 30
        DefaultSharingLinkType: "Direct"
```

## Maturity Level Definitions (Updated)

```yaml
# levels/levels.yaml
maturity_levels:
  - id: 1
    name: "Critical Exposure Eliminated"
    score_range: [0, 20]
    description: |
      Organization has eliminated critical security exposures that pose
      immediate threat (hours to days). All critical-severity thresholds
      across all checks must pass.

    advancement_criteria:
      type: "binary"
      requirement: "ALL level-1 thresholds must pass across all checks"
      blocking_behavior: "Any single level-1 threshold failure blocks advancement"

    threat_characteristics:
      timeline: "Hours to days"
      attacker_skill: "Low - script kiddie"
      attack_complexity: "Low"
      exploit_availability: "Public exploits available"

    example_blocking_conditions:
      - "Any anonymous edit links to any content"
      - "Any anonymous links to Critical/Highly Confidential data"
      - "Admin accounts without MFA"
      - "Clear-text password storage anywhere"
      - "Unconstrained delegation on domain controllers"
      - "Forest functional level < Windows Server 2008"

    typical_findings_to_remediate: "15-25 critical issues"

  - id: 2
    name: "High Risk Mitigated"
    score_range: [21, 40]
    description: |
      Organization has addressed high-risk exposures exploitable within
      weeks. All level-1 AND level-2 thresholds must pass.

    advancement_criteria:
      type: "binary"
      requirement: "ALL level-1 AND level-2 thresholds pass"
      blocking_behavior: "Any level-1 or level-2 failure blocks advancement"

    threat_characteristics:
      timeline: "Weeks to months"
      attacker_skill: "Medium - skilled attacker"
      attack_complexity: "Medium"
      exploit_availability: "Some public exploits, requires customization"

    example_blocking_conditions:
      - ">10 anonymous links to Confidential data"
      - "Privileged accounts without MFA"
      - "Guest accounts with Edit on Sensitive data"
      - "External sharing to consumer domains (>50 shares)"
      - "Stale admin accounts (inactive >90 days)"
      - "Forest functional level < Windows Server 2012 R2"

    typical_findings_to_remediate: "30-50 high-risk issues"

  - id: 3
    name: "Security Baseline Established"
    score_range: [41, 60]
    description: |
      Organization meets industry baseline security practices.
      All level-1, level-2, AND level-3 thresholds pass.

    advancement_criteria:
      type: "binary"
      requirement: "ALL level-1, level-2, AND level-3 thresholds pass"
      blocking_behavior: "Any failure at levels 1-3 blocks advancement"

    threat_characteristics:
      timeline: "Months to a year"
      attacker_skill: "Advanced - persistent threat actor"
      attack_complexity: "High"
      exploit_availability: "Custom exploits required"

    example_blocking_conditions:
      - ">50 permanent anonymous links"
      - "Guests with Read to >100 Confidential files"
      - "Missing data classification on >20% of sensitive data"
      - "No conditional access policies for risky locations"
      - "Legacy authentication enabled"
      - "Forest functional level < Windows Server 2016"

    typical_findings_to_remediate: "40-60 medium-risk issues"

  - id: 4
    name: "Enhanced Security Posture"
    score_range: [61, 80]
    description: |
      Organization demonstrates proactive security management with
      automation and advanced controls. All level-1 through level-4
      thresholds pass.

    advancement_criteria:
      type: "binary"
      requirement: "ALL level-1 through level-4 thresholds pass"
      blocking_behavior: "Any failure at levels 1-4 blocks advancement"

    threat_characteristics:
      timeline: "Long-term strategic threats"
      attacker_skill: "Expert - APT groups"
      attack_complexity: "Very High"
      exploit_availability: "Zero-day exploits"

    example_blocking_conditions:
      - "Guests without access review in past 90 days"
      - "No automated data labeling"
      - "No privileged identity management (PIM)"
      - "No insider risk monitoring"
      - "Manual permission management"
      - "Forest functional level < Windows Server 2019"

    typical_findings_to_remediate: "20-30 low-risk issues"

  - id: 5
    name: "State-of-the-Art Security"
    score_range: [81, 100]
    description: |
      Organization implements state-of-the-art security with predictive
      capabilities and continuous optimization. All checks at all levels pass.

    advancement_criteria:
      type: "binary"
      requirement: "ALL thresholds across ALL levels pass (perfect score)"
      blocking_behavior: "Any failure prevents level 5"

    threat_characteristics:
      timeline: "Future-proofed security"
      attacker_skill: "Nation-state actors"
      attack_complexity: "Extreme"
      exploit_availability: "Unknown/future threats"

    example_requirements:
      - "Zero anonymous links of any kind"
      - "Zero guest access without active business justification"
      - "Automated policy-as-code enforcement"
      - "Predictive threat analytics active"
      - "Continuous compliance validation"
      - "Latest forest functional level + all security features enabled"

    typical_state: "0-5 findings (continuous improvement)"

# Scoring calculation
scoring_model:
  approach: "Threshold-based deduction"

  base_score: 100

  calculation: |
    1. Start with 100 points
    2. For each check, evaluate all level thresholds
    3. Deduct points for highest-severity threshold that fails
    4. Sum all point deductions
    5. Final score = 100 - total_deductions
    6. Maturity level = highest level where ALL thresholds pass

  example:
    check: "SP-ES-001 (Anonymous Links)"
    results:
      - threshold: "Level 1 - Edit OR Critical data"
        status: "PASS"
        deduction: 0
      - threshold: "Level 2 - >10 Confidential"
        status: "FAIL (found 15 links)"
        deduction: 15
      - threshold: "Level 3 - >50 Permanent"
        status: "FAIL (found 120 links)"
        deduction: 8

    scoring_logic: "Take highest deduction from failed threshold = 15 points"
    result: "Blocks Level 2 advancement, deducts 15 points from score"
```

## Migration Strategy

### Phase 1: Schema Enhancement
1. Create new YAML-based check format with `level_thresholds` array
2. Maintain backward compatibility with existing CSV
3. Build validation tooling

### Phase 2: Check Migration
1. Convert existing 117 checks to new format
2. Add threshold logic for multi-level checks
3. For simple checks, create single-threshold definition

### Phase 3: Visualization
1. Build GitHub Pages site with ANSSI-style control graph
2. Interactive level navigation
3. Drill-down to individual checks
4. Visual dependency mapping

## Benefits of New Approach

1. **More Nuanced Assessment**: Same risk can have different severity at different scales
2. **Clearer Progression**: Organizations see exactly what's blocking each level
3. **Better Prioritization**: Multiple thresholds help focus remediation efforts
4. **ANSSI Alignment**: Matches proven, government-grade assessment methodology
5. **Visual Clarity**: Control graph shows security posture at a glance

## Implementation Timeline

- Week 1: Schema design and validation tooling
- Week 2: Convert top 25 checks to new format
- Week 3: Build GitHub Pages visualization
- Week 4: Migrate remaining checks + documentation
