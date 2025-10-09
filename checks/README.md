# DRIVE Security Checks - YAML Format

This directory contains individual YAML files for each security check in the DRIVE maturity model.

## Format

Each check is defined in a separate YAML file following the ANSSI-inspired multi-level threshold model.

### File Naming Convention

`{CHECK_ID}.yaml`

Examples:
- `SP-ES-001.yaml` - SharePoint anonymous links
- `AD-FL-001.yaml` - Active Directory functional level
- `OD-AX-005.yaml` - OneDrive access control

## Schema

See example files for complete schema:
- [`SP-ES-001.yaml`](./SP-ES-001.yaml) - SharePoint check with 4 level thresholds
- [`AD-FL-001.yaml`](./AD-FL-001.yaml) - Active Directory check with 4 level thresholds

### Key Sections

```yaml
check_id: "UNIQUE-ID"
title: "Human-readable title"
short_description: "Brief summary"
detailed_description: "Full explanation"

category: "Access Control"
platform: "SharePoint"
drive_pillars: ["D", "E"]  # Data Protection, Exposure Analysis

# Multi-level thresholds (ANSSI-inspired)
level_thresholds:
  - level: 1              # Critical exposure
    threshold_condition: "Most severe condition"
    severity: "Critical"
    points_deduction: 30

  - level: 2              # High risk
    threshold_condition: "High risk condition"
    severity: "High"
    points_deduction: 15

# Framework mappings
framework_mappings:
  nist_csf: {...}
  cis_v8: {...}
  iso_27001: {...}

# Remediation guidance
remediation:
  steps: [...]

# Validation
validation:
  test_queries: [...]

# References
references:
  microsoft_docs: [...]
```

## Creating New Checks

1. **Copy template:**
   ```bash
   cp SP-ES-001.yaml YOUR-CHECK-ID.yaml
   ```

2. **Edit check definition:**
   - Update check_id, title, description
   - Define platform and category
   - Set DRIVE pillars
   - Define level thresholds (1-5)
   - Map to frameworks
   - Add remediation steps
   - Include validation logic

3. **Validate:**
   ```bash
   python3 ../tools/validate_checks.py YOUR-CHECK-ID.yaml
   ```

## Multi-Level Threshold Guidelines

### When to Use Multiple Thresholds

A check should have multiple thresholds when:
- The risk **scales** with quantity (e.g., 1 anonymous link vs 100)
- The severity **varies** with scope (e.g., public access to Internal vs Critical data)
- The impact **depends** on context (e.g., Read vs Edit permissions)
- The exploitability changes over time (e.g., recent vs stale resources)

### Example Patterns

**Pattern 1: Quantity-Based Escalation**
```yaml
level_thresholds:
  - level: 1
    threshold_condition: "anonymous_links > 0 AND target_classification = 'Critical'"
  - level: 2
    threshold_condition: "anonymous_links > 10 AND target_classification = 'Confidential'"
  - level: 3
    threshold_condition: "anonymous_links > 50"
```

**Pattern 2: Permission-Based Escalation**
```yaml
level_thresholds:
  - level: 1
    threshold_condition: "external_users_with_full_control > 0"
  - level: 2
    threshold_condition: "external_users_with_edit > 0"
  - level: 3
    threshold_condition: "external_users_with_read > 10"
```

**Pattern 3: Version/Configuration-Based**
```yaml
level_thresholds:
  - level: 1
    threshold_condition: "version < minimum_supported_version"
  - level: 2
    threshold_condition: "version < recommended_version"
  - level: 3
    threshold_condition: "version < latest_version"
```

## Validation

All checks must pass validation before deployment:

```bash
# Validate single check
python3 ../tools/validate_checks.py SP-ES-001.yaml

# Validate all checks
python3 ../tools/validate_checks.py .

# Expected output:
# ✅ SP-ES-001.yaml: PASSED
# ✅ AD-FL-001.yaml: PASSED
```

## Aggregation for Website

After creating or updating checks, aggregate for the website:

```bash
python3 ../tools/aggregate_checks.py .
```

This generates:
- `/docs/catalog/drive_risk_catalog.json` - All checks for website
- `/docs/catalog/stats.json` - Summary statistics

## Maturity Level Definitions

Use these guidelines when assigning level thresholds:

### Level 1: Critical Exposure (Immediate Threat)
- **Timeline:** Hours to days
- **Severity:** Critical
- **Examples:**
  - Anonymous edit permissions
  - Critical data exposed publicly
  - Admin accounts without MFA
  - Clear-text password storage

### Level 2: High Risk (Short-term Threat)
- **Timeline:** Weeks to months
- **Severity:** High
- **Examples:**
  - Privileged accounts without MFA
  - Guest accounts with edit permissions
  - Stale admin accounts
  - External sharing without authentication

### Level 3: Security Baseline (Standard Practice)
- **Timeline:** Months to year
- **Severity:** Medium
- **Examples:**
  - Missing data classification
  - Excessive permissions
  - Lack of access reviews
  - Legacy authentication enabled

### Level 4: Enhanced Security (Proactive)
- **Timeline:** Strategic threats
- **Severity:** Low
- **Examples:**
  - No automated labeling
  - Manual permission management
  - Guests without recent reviews
  - Missing advanced monitoring

### Level 5: State-of-the-Art (Optimal)
- **Timeline:** Future-proofed
- **Severity:** Info
- **Examples:**
  - No predictive analytics
  - Manual policy management
  - Lack of continuous optimization
  - Missing latest security features

## Framework Mapping Requirements

Every check should map to at minimum:
- **NIST CSF 2.0** (function + control ID)
- **CIS v8** (control number)

Recommended additional mappings:
- **ISO 27001** (Annex A control)
- **CIS M365 Benchmark** (recommendation number)
- **MITRE ATT&CK** (technique ID for Critical/High severity)
- **GDPR** (article number for data protection checks)

## Example Checks

### SP-ES-001: Anonymous Sharing Links
- 4 level thresholds (Levels 1-4)
- Progressive severity based on permissions and data classification
- Complete remediation guidance with PowerShell commands
- Full framework mappings

### AD-FL-001: Active Directory Functional Level
- 4 level thresholds (Levels 1-4)
- Version-based progression (Windows 2008 → 2019)
- Missing security features at each level
- Infrastructure remediation guidance

## Status

- ✅ Schema defined
- ✅ Validation script created
- ✅ Aggregation script created
- ✅ 2 example checks created
- ⏳ 115 checks to be migrated from CSV

## Migration from CSV

To migrate existing checks:

```bash
# Run migration script
python3 ../tools/migrate_csv_to_yaml.py

# This will:
# 1. Read catalog/drive_risk_catalog.csv
# 2. Generate YAML file per check in this directory
# 3. Create single-threshold definition as starting point
# 4. Require manual enhancement for multi-level thresholds
```

## Resources

- [NEW_ARCHITECTURE.md](../docs/NEW_ARCHITECTURE.md) - Architecture design document
- [CLAUDE.md](../CLAUDE.md) - Development guide
- [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) - Implementation status
- [DRIVE_PRD.md](../docs/DRIVE_PRD.md) - Product requirements
