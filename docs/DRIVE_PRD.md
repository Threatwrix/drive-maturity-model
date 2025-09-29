# DRIVE Maturity & Risk Scoring Platform – Product Requirements Document (PRD)

## 1. Objective

Build the **DRIVE Risk & Maturity Assessment** platform that helps organizations evaluate and improve their Microsoft 365 data and identity security posture.  

**DRIVE** stands for **Data Risk and Identity Vulnerability Exposure** maturity - a comprehensive assessment model focused on both data protection and identity security risks.

The solution consolidates ~90 security checks into a unified **DRIVE Score** (0–100) and maps them to a 5-level **maturity model**.  

Goals:
- Provide a **quantitative score** for data risk and identity vulnerability exposure.
- Enable customers to understand both **risk exposure** and **maturity level** across data and identity domains.
- Map results to industry frameworks (NIST CSF, CIS v8, CIS M365 Benchmark, ISO 27001, ANSSI/PingCastle).
- Support **automation-first** (all checks measurable and API-driven).
- Address both **data protection** (sensitive data exposure, classification, sharing) and **identity security** (access controls, permissions, authentication).

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

### 2.3 Maturity Levels

1. **Foundational (Reactive)** – minimal hygiene, unmanaged risks.  
2. **Baseline (Defined)** – core protections in place, inconsistent coverage.  
3. **Managed (Preventive)** – policies enforced, risks measured, frameworks adopted.  
4. **Advanced (Adaptive)** – automation + monitoring, strong identity & classification coverage.  
5. **Optimized (Proactive)** – continuous risk scoring, policy-as-code, predictive security.  

Levels are determined by:  
- **Score threshold** (e.g. L3 ≥ 40, L5 ≥ 80).  
- **Control gating** (e.g. cannot reach L3 without MFA, cannot reach L5 without continuous risk pipeline).  

### 2.4 Risk vs Controls

- **Risk Assessment**: presence of risky findings lowers the score.  
- **Control Adoption**: mandatory controls required to unlock higher levels.  
- This hybrid model ensures tenants can’t achieve high maturity with risky misconfigs.  

### 2.5 Framework Mapping

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

- Dashboard:  
  - Overall DRIVE Score (0–100)  
  - Maturity Level (1–5 badge)  
  - Per-category breakdown  
  - Key risky findings + remediation guidance  
- CSV export of results  
- Historical trendline (90-day retention)  

---

## 6. Success Criteria

| Metric | Target |
|--------|--------|
| Catalog maintained in GitHub | Yes |
| JSON regenerated on validation | Yes |
| <5% false positives per check | Yes |
| 90-day historical reporting | Yes |
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
