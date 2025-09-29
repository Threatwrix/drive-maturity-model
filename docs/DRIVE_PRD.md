# DRIVE Maturity & Risk Scoring Platform – Product Requirements Document (PRD)

## 1. Objective

Build the **DRIVE Risk & Maturity Assessment** platform that helps organizations evaluate and improve their Microsoft 365 data and identity security posture.  

**DRIVE** stands for **Data Risk and Identity Vulnerability Exposure** maturity - a comprehensive assessment model focused on both data protection and identity security risks.

The solution consolidates 117 security checks into a unified **DRIVE maturity assessment** and maps them to a 5-level **threat-focused maturity model**.  

Goals:
- Provide **clear maturity progression** for data risk and identity vulnerability exposure.
- Enable customers to understand both **current security posture** and **actionable next steps** across data and identity domains.
- Map results to industry frameworks (NIST CSF, CIS v8, CIS M365 Benchmark, ISO 27001, ANSSI/PingCastle).
- Support **automation-first** (all checks measurable and API-driven).
- Address both **data protection** (sensitive data exposure, classification, sharing) and **identity security** (access controls, permissions, authentication).
- Focus on **threat timeline** - immediate threats first, then progressive security improvement.

---

## 2. Scope of Version 1

### 2.1 Supported Platforms
- SharePoint Online (SPO)
- OneDrive (OD)
- Teams
- Exchange Online (EX)

### 2.2 DRIVE Maturity Assessment Model

**Threat-Focused Binary Advancement:** Organizations progress through 5 maturity levels based on **binary pass/fail** criteria for each level. All required checks must pass to advance.

**Five Maturity Levels:**
1. **Critical Exposure (Immediate Threat)** - 16 checks
   - Anonymous access, weak admin credentials, critical AD misconfigurations
   - *Risk Timeline: Exploitable within hours/days*

2. **High Risk Mitigated (Short-term Protection)** - 42 checks  
   - Privileged access controls, guest lifecycle, external sharing governance
   - *Risk Timeline: Exploitable within weeks/months*

3. **Standard Security Baseline (Default Plus)** - 35 checks
   - Conditional access, data classification, regular reviews, baseline policies  
   - *Risk Timeline: Standard security practices*

4. **Enhanced Security Posture (Proactive Management)** - 12 checks
   - Advanced automation, behavioral analytics, Zero Trust implementation
   - *Risk Timeline: Proactive threat prevention*

5. **State-of-the-Art Security (Continuous Excellence)** - 12 checks
   - Predictive security, policy-as-code, continuous optimization
   - *Risk Timeline: Future-proofed security*

**Advancement Criteria:**
```
Customer Maturity Level = Highest level where ALL required checks pass

Examples:
- Pass all Level 1 & 2 checks, fail 1 Level 3 check → Level 2
- Pass all Level 1-4 checks, fail 1 Level 5 check → Level 4  
- Pass all 117 checks → Level 5
```

**No Complex Scoring:** Simple binary model eliminates confusing point calculations and focuses on actual risk remediation.

### 2.3 Framework Mapping

Each check is mapped to external standards:  
- **NIST CSF 2.0** (Identify, Protect, Detect, Respond, Recover).  
- **CIS Critical Security Controls v8** (esp. identity, data, and access).  
- **CIS Microsoft 365 Benchmark v5.0** (baseline technical guidance).  
- **ISO/IEC 27001 Annex A** (control mappings).  
- **ANSSI / PingCastle maturity model** (heuristic identity/data hygiene).  

Mappings are maintained in `/frameworks/*.csv` files (per standard).

---

## 3. Data Model

Each check includes:  
- `check_id` (unique, e.g. DRS-001)  
- `title`  
- `category`  
- `platform`  
- `severity`  
- `description`  
- `logic` (deterministic detection)  
- `data_points` (required telemetry)  
- `drive_pillar` (D, R, I, V, E)  
- `drive_maturity_min` (lowest maturity level required)  
- `drive_weight` (0–1)  
- Framework references (nist_csf_id, cis_v8_control, etc.)
- `remediation_guidance` (step-by-step fix instructions)
- `1secure_remediable` (boolean - can 1Secure automatically fix this)
- `1secure_policy_template` (policy configuration template if applicable)
- `threat_timeline` (immediate, short_term, baseline, advanced, optimal)  

### 3.1 Data & Identity Score Calculation

**Data Security DRIVE Score** includes checks from:
- **D** (Data Protection): Data classification, encryption, retention, sharing controls
- **R** (Risk Management): Risk identification, assessment, mitigation, monitoring
- **V** (Vulnerability Management): Security gaps, misconfigurations, exposure assessment

**Identity Security DRIVE Score** includes checks from:
- **I** (Identity Security): Authentication, authorization, access management, lifecycle  
- **R** (Risk Management): Risk identification, assessment, mitigation, monitoring
- **E** (Exposure Analysis): Attack surface, external access, behavioral anomalies

**Overall DRIVE Score** = Average of Data Security and Identity Security scores

**Binary Advancement per Domain:**
```
Data Maturity Level = Highest level where ALL data-related checks pass
Identity Maturity Level = Highest level where ALL identity-related checks pass
Overall Maturity Level = MIN(Data Maturity Level, Identity Maturity Level)
```

**Example:**
- Data Security: Pass all L1-L3 data checks, fail L4 → Data DRIVE = 3.0
- Identity Security: Pass all L1-L2 identity checks, fail L3 → Identity DRIVE = 2.0  
- Overall DRIVE: MIN(3.0, 2.0) = 2.0 (blocked by weakest domain)

### 3.2 Assessment Results Data Model

**Per-Organization Assessment:**
- `org_id`, `org_size` (Small/Medium/Large), `industry`
- `assessment_date`, `drive_data_score`, `drive_identity_score`, `drive_overall_score`
- `findings[]` - array of finding results per check_id
- `remediation_plan[]` - prioritized actions with 1Secure integration flags

**Finding Result:**
- `check_id`, `status` (pass/fail), `finding_details`, `evidence`
- `remediation_status` (not_started/planned/in_progress/completed)
- `remediation_assignee`, `target_date`, `completion_date`
- `1secure_policy_applied` (boolean), `validation_date`

**Benchmarking Data:**
- Anonymized aggregate scores by org_size and industry
- Percentile calculations updated monthly from customer base
- Maturity level distribution statistics for peer comparison

**Organization Configuration:**
- `org_id`, `disabled_checks[]` - array of check_ids that are disabled
- `check_weights{}` - custom weightings per check_id (default 1.0)
- `assessment_schedule` (daily/weekly/monthly)
- `catalog_last_updated` - timestamp of last GitHub sync
- `disabled_count` - total number of disabled checks for dashboard display

---

## 4. Repo & Tooling

### 4.1 Catalog
- Authoritative source: `catalog/drive_risk_catalog.csv`
- JSON export auto-generated (`drive_risk_catalog.json`).

### 4.2 Frameworks
- CSV files for mappings (`nist_csf.csv`, `cis_v8.csv`, `cis_m365.csv`, `iso_27001.csv`, `anssi_pingcastle.csv`).

### 4.3 Levels
- `levels/levels.yaml` defines 5 maturity levels with required controls.  

### 4.4 Scoring
- `scoring/scoring.yaml` defines categories, severity weights, exposure logistic function.  

### 4.5 Validation Tool
- `tools/validate_and_build.py`: schema validation, ID uniqueness, severity/type checks, JSON regeneration.

---

## 5. UI Requirements

### 5.1 DRIVE Score Dashboard
- **Overall DRIVE Maturity Level** (1–5 with level badge and name)
- **Data Security DRIVE Score** (1.0–5.0) - based on data-focused risk checks
- **Identity Security DRIVE Score** (1.0–5.0) - based on identity-focused risk checks
- **Combined DRIVE Score** calculation methodology display

### 5.2 Score Calculation Display
```
Example Customer View:
┌─────────────────────────────────────────┐
│ Overall DRIVE Maturity: Level 3.0       │
│ Standard Security Baseline (Default+)   │
├─────────────────────────────────────────┤
│ Data Security DRIVE: 3.5                │
│ │ ████████████████████░░░░ 70% complete  │
│ │ Blocked by: Missing DLP policies       │
│                                         │
│ Identity Security DRIVE: 2.5            │
│ │ ████████████░░░░░░░░░░░░ 50% complete  │
│ │ Blocked by: MFA gaps for admins       │
│                              [Present] │
└─────────────────────────────────────────┘
```

### 5.3 Presentation Mode
- **Full-screen presentation** triggered by "Present" button
- **Executive-friendly visuals** with large fonts and clear metrics
- **Auto-advancing slides** showing key areas (optional timer)
- **Slide navigation** with arrow keys or click controls
- **Presenter notes** overlay with talking points (toggle on/off)

```
Presentation Flow (Full Screen):
Slide 1: Executive Summary
├─ Overall DRIVE Score: 3.0/5.0
├─ Risk Reduction: 45% (last 90 days)
└─ Key Achievement: Level 2 → 3 advancement

Slide 2: Data Security Domain
├─ Current Level: 3.5/5.0 (75th percentile)
├─ Recent Progress: +0.5 improvement
└─ Next Priority: Implement DLP policies

Slide 3: Identity Security Domain  
├─ Current Level: 2.5/5.0 (45th percentile)
├─ Critical Gap: Admin MFA enforcement
└─ Timeline: 30 days to Level 3

Slide 4: Remediation Progress
├─ Completed: 12 findings (last quarter)
├─ In Progress: 8 findings
└─ 1Secure Automation: 67% of fixes

Slide 5: Peer Comparison
├─ Industry Ranking: Top 25%
├─ Improvement Velocity: 2x peer average
└─ Compliance Readiness: 85% NIST CSF
```

### 5.4 Detailed Breakdown
- **Per-domain risk findings** (Data vs Identity focused)
- **Platform coverage** (SharePoint, OneDrive, Teams, Exchange, AD)
- **Threat timeline view** (Immediate → Short-term → Baseline → Advanced → Optimal)
- **Key blocking findings** with remediation priorities
- **Framework compliance** mapped to each domain

### 5.5 Organizational Benchmarking
- **Peer comparison** by organization size (Small <500, Medium 500-5K, Large 5K+)
- **Industry benchmarks** showing percentile ranking per domain
- **Maturity distribution** showing where customer stands vs peers
```
Example Benchmark View:
Your Organization (Medium, 2,500 employees)
┌─────────────────────────────────────────────────┐
│ Data Security DRIVE: 3.5 (75th percentile)     │
│ Industry Average: 2.8 │ Top Quartile: 4.1     │
│                                                 │
│ Identity Security DRIVE: 2.5 (45th percentile) │
│ Industry Average: 2.7 │ Top Quartile: 3.8     │
└─────────────────────────────────────────────────┘
```

### 5.6 Detailed Findings Management
- **All checks view** with pass/fail status and severity filtering
- **Finding details** with full description, detection logic, and impact
- **Framework mappings** showing NIST CSF, CIS, ISO 27001 alignments per finding
- **Search and filtering** by platform, severity, maturity level, DRIVE pillar
- **Bulk actions** for findings management and tracking

### 5.7 Remediation Workflow
- **Recommended Actions** dashboard prioritized by threat timeline
- **1Secure Integration** - direct links to policy configuration for remediable findings
- **External Remediation** - step-by-step guidance for manual fixes
- **Implementation Tracking** - mark actions as planned/in-progress/completed
- **Validation** - re-run specific checks to verify remediation

```
Example Remediation Flow:
Finding: "Admin accounts without MFA" → 
Action: "Enable MFA for privileged accounts" →
1Secure Can Fix: YES → 
"Configure Conditional Access Policy" [Button] →
Policy Configuration UI → 
Apply Policy → 
Re-validate Finding
```

### 5.8 Progress Tracking & Analytics
- **Historical trendlines** (90-day retention) with milestone markers
- **Remediation velocity** showing findings resolved per time period
- **Domain improvement** tracking Data vs Identity progress separately
- **ROI metrics** showing security posture improvement over time
- **Compliance readiness** trending for each framework
- **Executive reporting** with high-level metrics and key achievements

### 5.9 Assessment Configuration Management
- **Check catalog view** showing all 117 checks with metadata
- **Individual check toggle** - enable/disable specific checks per organization
- **Disabled checks counter** prominently displayed on dashboard
- **Check update history** showing when catalog was last refreshed from GitHub
- **Custom check weightings** for organization-specific risk priorities
- **Assessment schedule** configuration (daily/weekly/monthly)

```
Example Configuration View:
┌─────────────────────────────────────────────────┐
│ Assessment Configuration                        │
│ Last Updated: 2024-01-15 | ⚠️ 3 checks disabled │
├─────────────────────────────────────────────────┤
│ [✓] DRS-001: Anonymous sharing enabled         │
│ [✗] DRS-003: Guest access review cadence       │
│ [✓] IDS-012: Admin MFA enforcement             │
│ [✗] DRS-045: Data classification labels        │
│                           [View All 117 Checks]│
└─────────────────────────────────────────────────┘
```

### 5.10 Export and Integration
- **CSV export** of all findings with Data/Identity classification and remediation status
- **PDF reports** for executive briefings and compliance documentation
- **API endpoints** for integration with SIEM/SOAR platforms
- **Webhook notifications** for critical finding alerts and remediation milestones  

---

## 6. Success Criteria

| Metric | Target |
|--------|--------|
| Catalog maintained in GitHub | Yes |
| JSON regenerated on validation | Yes |
| <5% false positives per check | Yes |
| Separate Data & Identity DRIVE scores | Yes |
| Organizational benchmarking by size/industry | Yes |
| Detailed findings view with framework mappings | Yes |
| 1Secure integration for automatic remediation | Yes |
| Progress tracking and analytics (90-day retention) | Yes |
| Remediation workflow with validation | Yes |
| Executive reporting and PDF export | Yes |
| Assessment configuration management | Yes |
| Individual check disable/enable functionality | Yes |
| Full-screen Presentation Mode for stakeholder briefings | Yes |
| UI dashboard functional prototype in Replit | Yes |

---

## 7. Future Phases / Backlog

- Automated CI validation workflow (GitHub Actions).  
- React dashboard (Replit) for visualization.  
- Integration with Netwrix DSPM detection engines.  
- API for exporting findings.  
- Expansion beyond M365 (Azure AD, Google Workspace, etc.).  

---

## 8. References

- CIS Microsoft 365 Foundations Benchmark v5.0  
- NIST CSF 2.0  
- CIS Critical Security Controls v8  
- PingCastle ANSSI maturity model  
- Copilot Readiness Assessment PRD (risk scoring logic)
