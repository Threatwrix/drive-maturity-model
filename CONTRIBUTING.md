# Contributing to Netwrix DRIVE

Thank you for contributing to the Netwrix DRIVE (Data Risk and Identity Vulnerability Exposure) maturity model! This guide will help you add new security checks or update existing ones.

## Table of Contents

- [Quick Start](#quick-start)
- [Adding a New Check](#adding-a-new-check)
- [Updating an Existing Check](#updating-an-existing-check)
- [Check File Structure](#check-file-structure)
- [Validation and Testing](#validation-and-testing)
- [Submitting Changes](#submitting-changes)
- [Change History Tracking](#change-history-tracking)

## Quick Start

1. **Fork the repository** (or create a branch if you have write access)
2. **Create or edit a check** in the `/checks/` directory
3. **Validate your changes**: `python3 tools/validate_checks.py`
4. **Update the catalog**: `python3 tools/aggregate_checks.py`
5. **Commit with a descriptive message**
6. **Push and create a Pull Request**

## Adding a New Check

### 1. Choose a Check ID

Use the naming convention: `<PILLAR>-<CATEGORY>-<NUMBER>-<PLATFORM>.yaml`

**DRIVE Pillars:**
- `D` - Data Protection
- `R` - Risk Management
- `I` - Identity Security
- `V` - Vulnerability Management
- `E` - Exposure Analysis

**Example:** `I-MFA-003-AAD.yaml` (Identity, MFA category, check #3, Azure AD platform)

### 2. Create the YAML File

Create a new file in `/checks/` using this template:

```yaml
check_id: I-MFA-003-AAD
title: Standard users without MFA enrolled
short_description: Standard users without MFA enrolled
detailed_description: |
  Regular user accounts without multi-factor authentication are vulnerable to
  credential theft and account takeover attacks. While less critical than admin
  accounts, compromised user accounts can still access sensitive data.
category: Identity
platform: Azure AD
drive_pillars:
  - I
automatable: true
owner: DRIVE-Team
status: active
created_date: '2025-10-09'
last_updated: '2025-10-09'

detection:
  data_sources:
    - Microsoft Graph API
    - Azure AD Sign-in Logs
  query_logic: |
    Query all users where:
    - Account is enabled
    - User is not in administrative roles
    - MFA registration status = Not Registered
  data_points_required:
    - User account status
    - MFA registration state
    - Role assignments

level_thresholds:
  - level: 3
    threshold_id: I-MFA-003-AAD-L3
    threshold_condition: "users_without_mfa > 25% of total users"
    threshold_description: More than 25% of users lack MFA protection
    severity: Medium
    business_impact: |
      Significant portion of workforce vulnerable to phishing and credential
      stuffing attacks. Data breach risk from compromised user accounts.
    threat_timeline: Exploitable within weeks to months
    attacker_profile: Opportunistic attackers using phishing campaigns
    cvss_score: 5.3
    points_deduction: 8
    remediation_priority: 3

  - level: 4
    threshold_id: I-MFA-003-AAD-L4
    threshold_condition: "users_without_mfa > 10% of total users"
    threshold_description: More than 10% of users lack MFA protection
    severity: Low
    business_impact: |
      Remaining users without MFA create unnecessary risk in an otherwise
      mature security environment.
    threat_timeline: Strategic long-term risk
    attacker_profile: Patient attackers targeting specific individuals
    cvss_score: 3.5
    points_deduction: 3
    remediation_priority: 4

framework_mappings:
  nist_csf:
    function: PROTECT
    categories:
      - PR.AC-7
    controls:
      - PR.AC-7
  cis_v8:
    controls:
      - "6.3"
      - "6.5"
  cis_m365:
    version: v3.0
    recommendations:
      - "1.1.1"
  iso_27001:
    version: "2022"
    controls:
      - A.9.4.2
      - A.9.4.3
  nist_800_53:
    revision: rev5
    controls:
      - IA-2(1)
      - IA-2(2)

remediation:
  automated_fix_available: false
  1secure_remediable: true
  fix_complexity: Low
  estimated_time_minutes: 30
  prerequisites:
    - Global Administrator or Authentication Administrator role
    - MFA service enabled in tenant
  steps:
    - step: 1
      level_target:
        - 3
        - 4
      action: Enable MFA registration for all users
      details: |
        1. Navigate to Azure AD > Security > MFA
        2. Configure MFA registration policy
        3. Set scope to "All users"
        4. Enable policy
      requires_manual: false
      manual_reason: null

    - step: 2
      level_target:
        - 3
        - 4
      action: Communicate MFA requirement to users
      details: |
        1. Send organization-wide announcement
        2. Provide setup instructions and support resources
        3. Set deadline for MFA enrollment
      requires_manual: true
      manual_reason: Requires communication and change management

    - step: 3
      level_target:
        - 3
        - 4
      action: Monitor enrollment progress
      details: |
        1. Run weekly reports on MFA registration status
        2. Follow up with non-compliant users
        3. Enforce conditional access blocking after deadline
      requires_manual: true
      manual_reason: Requires ongoing monitoring and follow-up

validation:
  test_queries:
    - "Get-MsolUser -All | Where {$_.StrongAuthenticationMethods.Count -eq 0}"
    - "GET https://graph.microsoft.com/v1.0/users?$filter=accountEnabled eq true&$select=id,userPrincipalName,strongAuthenticationMethods"
  false_positive_scenarios:
    - Service accounts (should be excluded from MFA requirements)
    - Break-glass emergency access accounts
    - Accounts pending decommissioning

references:
  microsoft_docs:
    - https://docs.microsoft.com/en-us/azure/active-directory/authentication/howto-mfa-getstarted
    - https://docs.microsoft.com/en-us/azure/active-directory/conditional-access/howto-conditional-access-policy-all-users-mfa
  industry_guidance:
    - https://www.cisa.gov/mfa
  threat_intelligence:
    - https://attack.mitre.org/techniques/T1078/

metadata:
  version: 1.0.0
  schema_version: "2.0"
  last_reviewed: '2025-10-09'
  next_review_due: '2026-01-09'
  reviewed_by: YourName
  change_history:
    - date: '2025-10-09'
      version: 1.0.0
      change: Initial check creation
      author: YourName
```

### 3. Validate and Test

```bash
# Validate YAML syntax and required fields
python3 tools/validate_checks.py

# If validation passes, aggregate for the website
python3 tools/aggregate_checks.py
```

## Updating an Existing Check

### 1. Make Your Changes

Edit the appropriate YAML file in `/checks/`. You can update any section:
- Add or modify `level_thresholds`
- Update `remediation` steps
- Add `framework_mappings`
- Refine `detection` logic

### 2. Update Metadata

**Important:** Always update the metadata section when making changes:

```yaml
metadata:
  version: 1.1.0  # Increment version (see versioning guidelines below)
  schema_version: "2.0"
  last_reviewed: '2025-10-09'  # Today's date
  next_review_due: '2026-01-09'  # 3 months from now
  reviewed_by: YourName
  change_history:
    - date: '2025-10-09'
      version: 1.1.0
      change: "Added Level 2 threshold for high-risk scenarios with >50 users"
      author: YourName
    - date: '2025-09-15'  # Keep all previous entries
      version: 1.0.0
      change: "Initial check creation"
      author: PreviousAuthor
```

**Versioning Guidelines:**
- **Patch (1.0.0 → 1.0.1)**: Typo fixes, clarifications, minor wording changes
- **Minor (1.0.0 → 1.1.0)**: New thresholds, enhanced detection logic, additional framework mappings
- **Major (1.0.0 → 2.0.0)**: Breaking changes, complete check restructure, changed scoring model

### 3. Validate and Test

```bash
python3 tools/validate_checks.py
python3 tools/aggregate_checks.py
```

## Check File Structure

### Required Fields

Every check must include:
- `check_id`: Unique identifier
- `title`: Brief descriptive title
- `platform`: Target system (SharePoint, OneDrive, Teams, Exchange Online, Active Directory, File System)
- `drive_pillars`: Array of applicable DRIVE pillars
- `level_thresholds`: At least one threshold definition
- `metadata`: Version and change tracking information

### Level Thresholds

Each threshold defines when a check blocks a specific maturity level:

```yaml
level_thresholds:
  - level: 1  # Blocks Level 1 advancement
    threshold_id: UNIQUE-ID-L1
    threshold_condition: "critical_condition_met"  # Logical expression
    threshold_description: Human-readable condition
    severity: Critical  # Critical, High, Medium, Low, Info
    business_impact: What happens if exploited
    threat_timeline: How quickly exploitable
    attacker_profile: Who would exploit this
    cvss_score: 9.0  # CVSS v3.1 base score
    points_deduction: 30  # How many points deducted
    remediation_priority: 1  # 1-5 (1 = highest priority)
```

**Severity Levels:**
- **Critical**: Immediate threat, exploitable in hours/days → Blocks Level 1
- **High**: Exploitable within weeks → Blocks Level 2
- **Medium**: Exploitable within months → Blocks Level 3
- **Low**: Strategic/long-term risk → Blocks Level 4
- **Info**: State-of-the-art optimization → Blocks Level 5

### Framework Mappings

Map your check to relevant compliance frameworks:

```yaml
framework_mappings:
  nist_csf:
    function: PROTECT  # IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER
    categories:
      - PR.AC-1
    controls:
      - PR.AC-1

  cis_v8:
    controls:
      - "5.1"
      - "5.2"

  cis_m365:
    version: v3.0
    recommendations:
      - "1.1.1"

  iso_27001:
    version: "2022"
    controls:
      - A.9.1.1

  nist_800_53:
    revision: rev5
    controls:
      - AC-2
      - AC-3

  gdpr:
    articles:
      - "32"  # Security of processing

  hipaa:
    safeguards:
      - "164.312(a)(2)(i)"  # Access Control

  pci_dss:
    version: "4.0"
    requirements:
      - "8.3.1"

  soc2:
    trust_criteria:
      - CC6.1  # Common Criteria

  mitre_attack:
    tactics:
      - TA0006  # Credential Access
    techniques:
      - T1110  # Brute Force
```

## Validation and Testing

### Automated Validation

The validation script checks:
- YAML syntax correctness
- Required fields presence
- Valid severity values
- Logical threshold structure
- Framework mapping validity
- Metadata completeness

```bash
python3 tools/validate_checks.py

# Output examples:
# ✓ All 118 checks validated successfully
# ✗ Error in checks/I-MFA-003-AAD.yaml: Missing required field 'platform'
```

### Manual Testing

Before submitting:
1. **Review the aggregated catalog**: Check `docs/catalog/drive_risk_catalog.json`
2. **Test locally**: Open `docs/index.html` in a browser (may need local server)
3. **Verify display**: Check that your check appears correctly in the catalog

```bash
# Option 1: Python simple server
cd docs
python3 -m http.server 8000
# Visit http://localhost:8000

# Option 2: Node.js serve
npx serve docs
```

## Submitting Changes

### Commit Message Format

Use clear, descriptive commit messages:

```
Add: I-MFA-003-AAD - Standard users without MFA

- Created new check for non-admin MFA coverage
- Added Level 3 threshold (>25% users without MFA)
- Added Level 4 threshold (>10% users without MFA)
- Mapped to NIST CSF, CIS v8, ISO 27001, NIST 800-53
- Included remediation steps with change management guidance
```

```
Update: SP-ES-001 - Anonymous SharePoint Links (v1.2.0)

- Enhanced Level 1 threshold to catch any critical data exposure
- Added GDPR Article 32 mapping
- Updated detection logic to include Teams shared files
- Refined remediation steps with PowerShell examples
```

### Git Workflow

```bash
# 1. Create a feature branch
git checkout -b add-check-i-mfa-003

# 2. Stage your changes
git add checks/I-MFA-003-AAD.yaml
git add docs/catalog/  # Include aggregated catalog

# 3. Commit with descriptive message
git commit -m "Add: I-MFA-003-AAD - Standard users without MFA

- Created new check for non-admin MFA coverage
- Added Level 3 and Level 4 thresholds
- Mapped to major compliance frameworks"

# 4. Push to GitHub
git push origin add-check-i-mfa-003

# 5. Create a Pull Request on GitHub
```

### Pull Request Guidelines

Your PR description should include:
- **Summary**: Brief description of changes
- **Rationale**: Why this check/update is needed
- **Testing**: How you validated the changes
- **Framework Alignment**: Which compliance frameworks this supports

Example PR template:

```markdown
## Summary
Adds new check for standard user MFA coverage (I-MFA-003-AAD)

## Rationale
While admin MFA is covered by existing checks, this check ensures broad
workforce protection against credential-based attacks.

## Changes
- Created I-MFA-003-AAD.yaml with two thresholds:
  - Level 3: Blocks if >25% users without MFA
  - Level 4: Blocks if >10% users without MFA
- Mapped to NIST CSF PR.AC-7, CIS v8 6.3, ISO 27001 A.9.4.2

## Testing
- ✓ Validated with validate_checks.py
- ✓ Aggregated successfully
- ✓ Reviewed in local browser
- ✓ Verified framework mappings against official documentation

## Screenshots
[Optional: Add screenshots of the check appearing in the catalog]
```

## Change History Tracking

### Three Layers of Transparency

Every change is tracked at three levels:

#### 1. YAML Change History (in each check)
```yaml
metadata:
  change_history:
    - date: '2025-10-09'
      version: 1.2.0
      change: "Enhanced Level 1 threshold"
      author: YourName
    - date: '2025-09-15'
      version: 1.1.0
      change: "Added Level 4 threshold"
      author: PreviousAuthor
    - date: '2025-09-01'
      version: 1.0.0
      change: "Initial creation"
      author: OriginalAuthor
```

#### 2. Git Commit History
Every commit provides full diff visibility:
```bash
# View full history of a check
git log --follow -p checks/I-MFA-003-AAD.yaml

# View who changed what (line-by-line)
git blame checks/I-MFA-003-AAD.yaml

# View changes between versions
git diff v1.0.0 v1.1.0 checks/I-MFA-003-AAD.yaml
```

#### 3. GitHub Web Interface
- View commit history: `https://github.com/Threatwrix/drive-maturity-model/commits/main/checks/`
- Click any check to see its complete history with diffs
- Anyone can see who changed what and when

### Best Practices for Change History

**DO:**
- Be specific about what changed and why
- Include the person's name who requested/approved the change
- Reference related issues or tickets if applicable
- Explain the business justification

**DON'T:**
- Use vague descriptions like "Updated check" or "Fixed stuff"
- Skip the change_history when making updates
- Forget to increment the version number

**Good Examples:**
```yaml
change: "Added Level 2 threshold for >50 privileged accounts without MFA per customer feedback"
change: "Updated CVSS score from 7.5 to 8.1 based on new threat intel (CVE-2024-xxxxx)"
change: "Refined threshold condition to exclude service accounts per CISO review"
```

**Bad Examples:**
```yaml
change: "Updated"
change: "Fixed check"
change: "Changes requested"
```

## Questions or Help?

- **Issues**: [GitHub Issues](https://github.com/Threatwrix/drive-maturity-model/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Threatwrix/drive-maturity-model/discussions)
- **Email**: drive-team@netwrix.com

## Recognition

All contributors will be acknowledged in the project. Thank you for helping improve
data and identity security for organizations worldwide!

---

**License**: This project is licensed under the terms specified in the LICENSE file.
**Code of Conduct**: Please review our CODE_OF_CONDUCT.md before contributing.
