# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

The **DRIVE Risk Catalog** is a public, framework-mapped catalog of Microsoft 365 data and identity security checks used to compute the DRIVE maturity score. DRIVE stands for **Data Risk and Identity Vulnerability Exposure** maturity.

**Architecture: ANSSI/PingCastle-Inspired Multi-Level Thresholds**

This repository contains:
- **Risk catalog** of 117 security checks for M365 environments (SharePoint, OneDrive, Teams, Exchange, File System, AD)
- **Multi-level threshold model** where each check can define multiple severity thresholds across maturity levels (ANSSI-inspired)
- **Framework mappings** to NIST CSF, CIS v8, CIS M365, ISO 27001, GDPR, MITRE ATT&CK, SOC 2, and ANSSI/PingCastle
- **5 threat-focused maturity levels** (Critical Exposure → State-of-the-Art Security)
- **GitHub Pages website** with interactive visualization (ANSSI-style control graph)

## Architecture

### Core Components

**New Architecture (v2.1 - ANSSI-Inspired with PowerPoint Export)**

The repository now supports TWO catalog formats:
1. **Legacy CSV format** (`/catalog/*.csv`) - Single level assignment per check
2. **New YAML format** (`/checks/*.yaml`) - Multi-level thresholds per check with PowerPoint export tagging (PREFERRED)

**Check Definitions** (`/checks/` - NEW)
- Individual YAML files per check (e.g., `SP-ES-001.yaml`, `AD-FL-001.yaml`)
- Each check defines multiple `level_thresholds` array entries
- Same check can block different maturity levels with different severity thresholds
- **PowerPoint export tagging** (schema v2.1) - Prioritize checks for executive presentations
  - `1-PrimaryFocus`: Critical findings requiring executive attention
  - `2-SecondaryFocus`: Important findings for management review
  - `3-AdditionalFinding`: Supporting details and context
  - `4-Exclude`: Technical detail only (not for executives)
- Example: Anonymous links could be Critical (Level 1) with edit permissions, High (Level 2) with >10 confidential files, Medium (Level 3) with >50 permanent links

**Catalog Format** (`/catalog/` - LEGACY)
- `drive_risk_catalog.csv` - Authoritative source (preferred for editing)
- `drive_risk_catalog.json` - Auto-generated from CSV
- `Risks.csv` - Raw risk data for merging (legacy)

Each risk check includes:
- `check_id`, `title`, `category`, `platform`, `severity`, `description`
- `logic` (deterministic detection criteria), `data_points` (telemetry required)
- `drive_pillar` (D=Data, R=Risk, I=Identity, V=Vulnerability, E=Exposure)
- `drive_maturity_min` (1-5 minimum maturity level), `drive_weight` (0-1 impact weight)
- Framework mappings: `nist_csf_function`, `nist_csf_id`, `cis_v8_control`, `cis_m365_benchmark`, `iso_27001_annex`, etc.

**Maturity Levels** (`/levels/levels.yaml`)
- 5-level threat-focused binary advancement model
- Level 1: Critical Exposure (Immediate Threat) - 16 checks
- Level 2: High Risk Mitigated (Short-term Protection) - 42 checks
- Level 3: Standard Security Baseline (Default Plus) - 35 checks
- Level 4: Enhanced Security Posture (Proactive Management) - 12 checks
- Level 5: State-of-the-Art Security (Continuous Excellence) - 12 checks

**Scoring Model** (`/scoring/scoring.yaml`)
- Category weights: Sensitive Data Exposure (30), Access Hygiene (25), External Sharing (20), Classification (15), Configuration (10)
- Severity weights: Critical (5), High (4), Medium (3), Low (1)
- Exposure logistic function with k=18, midpoint=0.15

**Framework Mappings** (`/frameworks/*.csv`)
- `nist_csf.csv`, `cis_v8.csv`, `cis_m365.csv`, `iso_27001.csv`, `anssi_pingcastle.csv`
- Additional: `gdpr.csv`, `mitre_attack.csv`, `soc2.csv`
- Each file maps DRIVE checks to specific controls/articles/techniques

### Key Concepts

**Binary Advancement Model**
- Organizations must pass ALL checks at each level to advance
- Overall maturity = MIN(Data Security Level, Identity Security Level)
- No partial credit - focus on actual risk remediation

**Dual Scoring Domains**
- **Data Security** = D (Data Protection) + R (Risk Management) + V (Vulnerability Management) pillars
- **Identity Security** = I (Identity Security) + R (Risk Management) + E (Exposure Analysis) pillars
- Both domains must advance together (lowest determines overall level)

**Threat Timeline Mapping**
- Checks are mapped by exploitability timeline, not arbitrary progression
- Level 1 = hours/days, Level 2 = weeks/months, Level 3 = baseline, Level 4 = proactive, Level 5 = predictive

## Common Development Tasks

### Creating New Checks (v2.1 YAML Format - PREFERRED)

**1. Create YAML file for new check:**
```bash
# Copy example template
cp checks/SP-ES-001.yaml checks/YOUR-CHECK-ID.yaml

# Edit the check definition
vi checks/YOUR-CHECK-ID.yaml
```

**2. Define multi-level thresholds:**
```yaml
level_thresholds:
  # Level 1 - Critical exposure
  - level: 1
    threshold_id: "CHECK-ID-L1"
    threshold_condition: "Most severe condition"
    severity: "Critical"
    points_deduction: 30

  # Level 2 - High risk
  - level: 2
    threshold_id: "CHECK-ID-L2"
    threshold_condition: "High risk condition"
    severity: "High"
    points_deduction: 15
```

**3. Validate and aggregate:**
```bash
# Validate YAML syntax and schema
python3 tools/validate_checks.py checks/YOUR-CHECK-ID.yaml

# Aggregate all checks for website
python3 tools/aggregate_checks.py checks/

# Test locally
open docs/index.html
```

### Editing the Catalog (Legacy CSV Format)

**For backwards compatibility only:**
```bash
# Edit the CSV directly
vi catalog/drive_risk_catalog.csv

# Regenerate JSON
python3 tools/merge_catalog.py
```

### Migrating CSV to YAML

**Migrate existing checks to new format:**
```bash
# Migrate all checks from CSV to individual YAML files
python3 tools/migrate_csv_to_yaml.py

# Review generated files
ls -la checks/

# Enhance with multi-level thresholds
# (Manual editing required for nuanced threshold logic)
```

### Adding PowerPoint Export Tags (v2.1)

**Add PowerPoint export prioritization to all checks:**
```bash
# Preview changes (dry run)
python3 tools/add_powerpoint_export_tags.py --dry-run

# Apply to all checks
python3 tools/add_powerpoint_export_tags.py

# Apply to specific checks only
python3 tools/add_powerpoint_export_tags.py checks/SP-*.yaml checks/1S-*.yaml

# Use custom priority mapping
python3 tools/add_powerpoint_export_tags.py --priority-mapping custom_rules.json
```

**This migration:**
- Adds `powerpoint_export` section to each check
- Intelligently assigns priority (1-PrimaryFocus, 2-SecondaryFocus, 3-AdditionalFinding, 4-Exclude)
- Based on severity, maturity level, and business impact keywords
- Updates schema version from 2.0 → 2.1
- Preserves all existing check data

### Data Management Scripts

**Merge new risk data into DRIVE format:**
```bash
python3 tools/merge_catalog.py
```
- Reads `Risks.csv`, transforms to DRIVE catalog format
- Maps severity, platforms, DRIVE stages → pillars
- Generates both CSV and JSON outputs
- Shows summary statistics

**Remap maturity levels (threat-focused model):**
```bash
python3 tools/remap_maturity_levels.py
```
- Analyzes each check's severity, title, description
- Assigns threat-focused maturity level (1-5) based on:
  - Critical severity + immediate exploitability → Level 1
  - Anonymous access / weak admin credentials → Level 1
  - High severity privilege issues → Level 2
  - Guest/external sharing → Level 2
  - Medium severity baseline controls → Level 3
  - Advanced monitoring/automation → Level 4
  - Predictive/continuous security → Level 5
- Updates `drive_maturity_min` in catalog
- Shows level distribution and significant changes

### Validation and Quality Checks

**Current validation approach:**
- Check ID uniqueness (no duplicate `check_id` values)
- Required fields present (`check_id`, `title`, `severity`, `platform`, `drive_pillar`, `drive_maturity_min`)
- Valid severity values (Critical, High, Medium, Low)
- Valid platform values (SharePoint, OneDrive, Teams, Exchange Online, File System, AD)
- Valid drive_pillar values (D, R, I, V, E)
- Valid drive_maturity_min range (1-5)

**Future validation (PRD mentions coming soon):**
- Schema validation against formal JSON schema
- Referential integrity between catalog and framework mappings
- Cross-framework control overlap detection
- Automated GitHub Actions CI workflow

### Framework Mapping

**When adding/updating framework mappings:**
1. Edit relevant CSV in `/frameworks/` directory
2. Ensure `check_id` matches catalog entry
3. Provide authoritative references (control IDs, article numbers, technique IDs)
4. For NIST CSF: include both function (IDENTIFY/PROTECT/DETECT/RESPOND/RECOVER) and control ID
5. For CIS: reference both v8 control number and M365 benchmark section if applicable

## Repository Structure Notes

```
/catalog/
  drive_risk_catalog.csv      # Authoritative source - edit this
  drive_risk_catalog.json     # Auto-generated - do not edit directly
  Risks.csv                   # Legacy risk data for merging

/frameworks/
  nist_csf.csv               # NIST Cybersecurity Framework 2.0 mappings
  cis_v8.csv                 # CIS Critical Security Controls v8
  cis_m365.csv               # CIS Microsoft 365 Benchmark v5.0
  iso_27001.csv              # ISO/IEC 27001 Annex A controls
  anssi_pingcastle.csv       # ANSSI/PingCastle maturity model
  gdpr.csv                   # GDPR article mappings
  mitre_attack.csv           # MITRE ATT&CK technique mappings
  soc2.csv                   # SOC 2 criterion mappings

/levels/
  levels.yaml                # 5-level maturity model definitions
                             # Includes threat timelines, focus areas, advancement criteria

/scoring/
  scoring.yaml               # Scoring categories, severity weights, exposure model

/tools/
  merge_catalog.py                # Transform raw risks into DRIVE format
  remap_maturity_levels.py        # Assign threat-focused maturity levels
  add_powerpoint_export_tags.py   # Add PowerPoint export tagging (v2.0 → v2.1)
  validate_checks.py              # Validate YAML check definitions (supports v2.1)

/docs/
  DRIVE_PRD.md              # Comprehensive Product Requirements Document
                             # Includes Replit implementation guide
  YAML_SCHEMA_V2.1.md       # Schema v2.1 specification with PowerPoint export
```

## Data Model Patterns

**Risk Check Schema:**
- Automation-first: All checks must be measurable and API-driven
- Deterministic logic: Detection criteria must be precise and reproducible
- Framework-mapped: Every check should map to at least 2 frameworks (NIST + one other)
- Threat-focused: Maturity level determined by exploitability timeline, not arbitrary progression
- Dual-domain: Each check contributes to either Data Security or Identity Security scoring

**Maturity Level Determination Logic:**
```
Level 1: Critical severity OR (anonymous access | weak admin creds | critical AD misconfig)
Level 2: High severity + (admin | privileged | guest | external | MFA)
Level 3: Medium severity baseline controls (stale resources, missing owners, broken inheritance)
Level 4: Advanced controls (sensitive data monitoring, resource-based delegation, automation)
Level 5: State-of-the-art (predictive, continuous, AES keys, shared channels)
```

**Framework Mapping Priority:**
- NIST CSF 2.0 (required for all checks)
- CIS v8 (required for all checks)
- ISO 27001 Annex A (required for access control checks)
- CIS M365 Benchmark (required for platform-specific checks)
- MITRE ATT&CK (recommended for high/critical severity)
- GDPR (required for data protection checks)

## Important Principles

**When editing the catalog:**
- Always prefer editing `drive_risk_catalog.csv` directly
- Never edit `drive_risk_catalog.json` manually (it's auto-generated)
- Maintain CSV column order and structure
- Check ID format: `PLATFORM-CATEGORY-###` or `PLATFORM-###`
- All checks must be automation-friendly (measurable via API/telemetry)

**When determining maturity levels:**
- Focus on threat timeline (how quickly can this be exploited?)
- Critical/anonymous/weak admin = Level 1 (immediate threat)
- Privilege/guest/external = Level 2 (short-term threat)
- Baseline hygiene = Level 3 (standard security)
- Advanced automation = Level 4 (proactive)
- Predictive/continuous = Level 5 (state-of-the-art)

**When adding framework mappings:**
- Provide authoritative references (don't guess)
- Check for control overlap (one DRIVE check may satisfy multiple framework controls)
- Update all relevant framework CSVs
- Consider cross-framework mapping analysis for investment ROI

## Target Implementation

This catalog is designed to power the DRIVE Maturity Assessment platform with:
- Interactive level drilling (PingCastle-inspired UX)
- Binary pass/fail advancement model
- Separate Data and Identity Security scores
- Multi-framework compliance views
- Full-screen presentation mode for stakeholders
- 1Secure integration for automated remediation

See `/docs/DRIVE_PRD.md` for complete product requirements including Replit implementation guide.
