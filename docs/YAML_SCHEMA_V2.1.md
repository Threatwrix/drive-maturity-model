# YAML Check Schema v2.1 - PowerPoint Export Enhancement

## Overview

Schema version 2.1 adds PowerPoint export tagging to support executive presentation generation capabilities inspired by Netwrix 1Secure's risk reporting.

## New Field: `powerpoint_export`

### Purpose
Control which checks appear in executive PowerPoint presentations and how they are prioritized.

### Schema Definition

```yaml
powerpoint_export:
  include: boolean           # Required: Whether to include in PowerPoint export
  priority: enum             # Required: Presentation priority level
  slide_section: string      # Optional: Which slide section to place finding
  executive_summary: string  # Optional: One-sentence summary for executives
  chart_visualization: enum  # Optional: Recommended chart type
```

### Field Specifications

#### `include` (boolean, required)
- **Values:** `true` | `false`
- **Default:** `true`
- **Purpose:** Master switch to include/exclude check from PowerPoint export
- **Example:** `include: true`

#### `priority` (enum, required)
- **Values:**
  - `1-PrimaryFocus` - Critical findings requiring immediate executive attention
  - `2-SecondaryFocus` - Important findings for management review
  - `3-AdditionalFinding` - Supporting details and context
  - `4-Exclude` - Exclude from PowerPoint (technical detail only)
- **Purpose:** Determine prominence and placement in executive presentation
- **Example:** `priority: 1-PrimaryFocus`

#### `slide_section` (string, optional)
- **Values:** Free text, but recommended values:
  - `"Executive Summary"`
  - `"Critical Findings"`
  - `"High Priority Risks"`
  - `"Compliance Gaps"`
  - `"Quick Wins"`
  - `"Long-term Roadmap"`
  - `"Technical Details"`
- **Purpose:** Group related findings in presentation
- **Default:** Auto-assigned based on priority
- **Example:** `slide_section: "Critical Findings"`

#### `executive_summary` (string, optional)
- **Values:** 1-2 sentence plain English summary (max 200 characters)
- **Purpose:** Executive-friendly description for presentation slides
- **Default:** Uses `short_description` if not provided
- **Example:** `executive_summary: "Anonymous links expose sensitive data to public internet without authentication"`

#### `chart_visualization` (enum, optional)
- **Values:**
  - `"trend"` - Line chart showing metric over time
  - `"gauge"` - Speedometer/gauge showing current vs threshold
  - `"bar"` - Bar chart comparing current vs target
  - `"heatmap"` - Risk heatmap (severity x likelihood)
  - `"table"` - Data table with details
  - `"none"` - No visualization, text only
- **Purpose:** Recommend chart type for this finding
- **Default:** `"gauge"` for threshold-based checks, `"bar"` for counts
- **Example:** `chart_visualization: "trend"`

## Priority Assignment Guidelines

### 1-PrimaryFocus
**Criteria:**
- Critical severity (Level 1 blocking checks)
- High business impact (data breach, compliance violation)
- Immediate remediation required (threat timeline: hours/days)
- Executive decision required

**Examples:**
- Anonymous links with edit permissions on confidential data
- No MFA on Global Administrator accounts
- Stale Global Admin accounts with active tokens
- Public internet exposure of sensitive databases

**Typical Count:** 3-7 findings per organization

### 2-SecondaryFocus
**Criteria:**
- High severity (Level 2 blocking checks)
- Moderate business impact
- Short-term remediation timeline (weeks)
- Management attention required

**Examples:**
- Guest users with admin roles
- External sharing >10% on confidential data
- Missing resource owners on critical systems
- Privileged access without monitoring

**Typical Count:** 10-20 findings per organization

### 3-AdditionalFinding
**Criteria:**
- Medium/Low severity (Level 3-4 checks)
- Supporting context for primary findings
- Longer remediation timeline (months)
- Technical team remediation

**Examples:**
- Stale permissions on non-critical resources
- Missing sensitivity labels on low-risk files
- Password complexity not meeting best practices
- Audit logging gaps on non-critical systems

**Typical Count:** 30-50 findings per organization

### 4-Exclude
**Criteria:**
- Technical detail not relevant to executives
- Informational only (no remediation required)
- Duplicate/related to higher priority finding
- Too granular for executive presentation

**Examples:**
- Individual file-level permission anomalies
- Low-severity configuration drift
- Noise-level findings with minimal business impact
- Technical metrics without business context

**Typical Count:** Any findings marked as technical deep-dive only

## Migration Strategy

### Phase 1: Add Default Values
- All Level 1 checks → `1-PrimaryFocus`
- All Level 2 checks → `2-SecondaryFocus`
- Level 3-4 checks → `3-AdditionalFinding`
- Level 5 checks → `3-AdditionalFinding` (state-of-the-art is context)

### Phase 2: Manual Refinement
- Review Critical severity checks for executive relevance
- Demote technical/noisy checks to `4-Exclude`
- Promote high-impact Medium severity checks to `2-SecondaryFocus`
- Add executive_summary for all `1-PrimaryFocus` checks

### Phase 3: Slide Section Assignment
- Group related findings into logical slide sections
- Ensure slide flow tells coherent story
- Balance slide density (5-7 findings per section max)

## Example: Complete Check with PowerPoint Export

```yaml
check_id: SP-ES-001
title: Sharepoint open access (anyone links present)
short_description: Anonymous links allow public internet access
detailed_description: 'Anyone' links allow anonymous access from the internet. If exploited, sensitive documents leak publicly and can be indexed by search engines.
category: Access Control
platform: SharePoint
drive_pillars:
- R
automatable: true
owner: DRIVE-Team
status: active
created_date: '2024-01-15'
last_updated: '2025-10-16T10:30:00Z'

detection:
  data_sources:
  - Microsoft 365 API
  - SharePoint API
  query_logic: 'Exploitability: High, Business Impact: High'
  data_points_required:
  - Count of 'Anyone' links with edit permissions

level_thresholds:
- level: 1
  threshold_id: SP-ES-001-L1
  threshold_condition: Any 'Anyone' links with edit permissions on Confidential+ data
  threshold_description: Critical data exposure via anonymous links
  severity: Critical
  business_impact: 'Anyone' links allow anonymous access from the internet. If exploited, sensitive documents leak publicly and can be indexed by search engines.
  threat_timeline: Exploitable within hours
  attacker_profile: Low skill - script kiddie
  cvss_score: 9.0
  remediation_priority: 1

- level: 2
  threshold_id: SP-ES-001-L2
  threshold_condition: >10 'Anyone' links with edit permissions on Internal data
  threshold_description: High risk of data exposure
  severity: High
  business_impact: Moderate data exposure risk on internal documents
  threat_timeline: Exploitable within days
  attacker_profile: Opportunistic attacker
  cvss_score: 7.5
  remediation_priority: 2

framework_mappings:
  nist_csf:
    function: PROTECT
    categories:
    - AC-14
    controls:
    - AC-14
  cis_v8:
    controls:
    - '15'
  iso_27001:
    version: '2022'
    controls:
    - 'Annex A: Access control; Annex A: Information classification & handling'

remediation:
  automated_fix_available: true
  1secure_remediable: true
  fix_complexity: Low
  estimated_time_minutes: 15
  prerequisites:
  - SharePoint Administrator access
  steps:
  - step: 1
    level_target: [1, 2]
    action: Identify all 'Anyone' links via 1Secure
    details: Use 1Secure dashboard to list all anonymous sharing links
    requires_manual: false
  - step: 2
    level_target: [1]
    action: Remove or convert to 'Specific People' links
    details: Prioritize links on Confidential+ labeled data
    requires_manual: true
    manual_reason: Requires business approval for access change

validation:
  test_queries:
  - Verify zero 'Anyone' links with edit permissions on Confidential+ data (Level 1)
  - Verify <10 'Anyone' links with edit permissions on Internal data (Level 2)
  false_positive_scenarios:
  - Public marketing materials intentionally shared via 'Anyone' links

references:
  microsoft_docs:
  - https://learn.microsoft.com/en-us/sharepoint/turn-external-sharing-on-or-off
  industry_guidance:
  - CIS Microsoft 365 Foundations Benchmark v5.0
  threat_intelligence:
  - MITRE ATT&CK T1530 - Data from Cloud Storage

# NEW SECTION: PowerPoint Export Configuration
powerpoint_export:
  include: true
  priority: 1-PrimaryFocus
  slide_section: "Critical Findings"
  executive_summary: "Anonymous links expose confidential documents to public internet without authentication, enabling data breaches"
  chart_visualization: "gauge"

metadata:
  version: 2.1.0
  schema_version: '2.1'
  last_reviewed: '2025-10-16'
  next_review_due: '2026-01-16'
  reviewed_by: DRIVE-Team
  change_history:
  - date: '2025-10-16'
    version: 2.1.0
    change: Added PowerPoint export tagging for executive presentations
    author: DRIVE-Team
  - date: '2025-10-09'
    version: 1.0.0
    change: Migrated from CSV to YAML multi-level format
    author: Migration Script
```

## Backward Compatibility

### Schema Version Detection
- `schema_version: '2.0'` → No `powerpoint_export` section (use defaults)
- `schema_version: '2.1'` → Has `powerpoint_export` section (explicit config)

### Default Behavior (v2.0 checks)
If `powerpoint_export` section is missing:
```python
# Pseudo-code for default behavior
if not check.get('powerpoint_export'):
    level = min([lt['level'] for lt in check['level_thresholds']])
    severity = check['level_thresholds'][0]['severity']

    if level == 1 and severity == 'Critical':
        priority = '1-PrimaryFocus'
    elif level <= 2 and severity in ['Critical', 'High']:
        priority = '2-SecondaryFocus'
    else:
        priority = '3-AdditionalFinding'

    return {
        'include': True,
        'priority': priority,
        'slide_section': None,  # Auto-assign
        'executive_summary': check['short_description'],
        'chart_visualization': 'gauge'
    }
```

## Validation Rules

### Required Fields
- `powerpoint_export.include` must be boolean
- `powerpoint_export.priority` must be one of: `1-PrimaryFocus`, `2-SecondaryFocus`, `3-AdditionalFinding`, `4-Exclude`

### Consistency Rules
- If `priority: 4-Exclude`, then `include` should be `false` (warning if mismatch)
- If `include: false`, then `priority` should be `4-Exclude` (warning if mismatch)
- If `priority: 1-PrimaryFocus`, `executive_summary` is highly recommended (warning if missing)

### Best Practices
- Limit `1-PrimaryFocus` to <10% of total checks (3-7 per organization typical)
- Ensure `2-SecondaryFocus` is <20% of total checks (10-20 per organization typical)
- All Critical severity Level 1 checks should be `1-PrimaryFocus` or `2-SecondaryFocus`
- Executive summaries should be <200 characters for slide readability

## Implementation Notes

### PowerPoint Generation Logic
1. **Filter:** Only include checks where `powerpoint_export.include = true`
2. **Sort:** Group by `priority` (1-PrimaryFocus first)
3. **Section:** Group by `slide_section` within each priority
4. **Visualize:** Use `chart_visualization` to render data
5. **Summarize:** Use `executive_summary` for slide text

### Slide Template Structure
```
Slide 1: Executive Summary
  - Overall DRIVE maturity level
  - Count of 1-PrimaryFocus findings
  - Top 3-5 critical risks (executive_summary)

Slide 2-3: Critical Findings (1-PrimaryFocus)
  - One finding per slide or 2-3 per slide
  - Chart visualization (gauge/trend)
  - Executive summary
  - Recommended action

Slide 4-6: High Priority Risks (2-SecondaryFocus)
  - Multiple findings per slide (grouped by slide_section)
  - Bar charts or tables
  - Remediation timeline

Slide 7: Additional Context (3-AdditionalFinding)
  - Summary table of supporting findings
  - Link to full technical report

Slide 8: Roadmap
  - Remediation timeline
  - Quick wins vs long-term investments
```

## Migration Command

```bash
# Add PowerPoint export tags to all checks with intelligent defaults
python3 tools/add_powerpoint_export_tags.py

# Options:
python3 tools/add_powerpoint_export_tags.py --priority-mapping custom_mapping.json
python3 tools/add_powerpoint_export_tags.py --dry-run  # Preview changes
python3 tools/add_powerpoint_export_tags.py --checks checks/SP-*.yaml  # Specific files
```

## Future Enhancements (v2.2+)

### Potential Additions
- `powerpoint_export.slide_notes` - Speaker notes for presenter
- `powerpoint_export.animation_type` - How finding appears on slide
- `powerpoint_export.comparison_data` - Peer benchmark comparison
- `powerpoint_export.remediation_cost` - Estimated cost/effort
- `powerpoint_export.compliance_impact` - Which frameworks affected

---

**Version:** 2.1.0
**Last Updated:** October 16, 2025
**Author:** DRIVE Team
**Status:** Proposed Schema Extension
