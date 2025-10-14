# 1Secure Integration PRD for DRIVE Maturity Model
## Product Requirements Document

**Version:** 1.0
**Date:** October 2025
**Author:** DRIVE Team
**Status:** Draft for Replit Prototype

---

## Executive Summary

This PRD defines how Netwrix 1Secure's current 52 risk metrics integrate with the DRIVE (Data Risk and Identity Vulnerability Exposure) maturity model to provide customers with an ANSSI/PingCastle-inspired security maturity assessment.

### Key Statistics

- **1Secure Risks:** 52 total (9 Data, 20 Identity, 23 Infrastructure)
- **DRIVE Checks Supported:** 52+ checks (expanded from base 118 catalog)
- **Data Sources:** SharePoint Online, OneDrive, Entra ID, Active Directory
- **Maturity Levels:** 5-level binary advancement model
- **Scoring Domains:** Data Security + Identity Security (dual-domain model)

---

## 1. Product Vision

### 1.1 Problem Statement

Organizations using Netwrix 1Secure need a standardized way to:
1. **Quantify security maturity** across M365 and AD environments
2. **Communicate risk** to executives and boards using industry-standard frameworks
3. **Track progress** toward security excellence with clear advancement criteria
4. **Prioritize remediation** based on threat exploitability timelines

### 1.2 Solution Overview

Integrate 1Secure's 52 risk metrics into the DRIVE maturity model to provide:
- **ANSSI-inspired multi-level thresholds** - Same risk at different severity levels
- **Binary level advancement** - Pass ALL checks or remain at current level
- **Threat-focused progression** - Level determined by exploitability timeline
- **Interactive visualization** - PingCastle-style control graph with drill-down
- **Framework mapping** - NIST CSF, CIS v8, ISO 27001, MITRE ATT&CK

---

## 2. 1Secure Risk Catalog

### 2.1 Data Category (9 risks)

| 1Secure Metric | Measure | Low | Medium | High | Maps to DRIVE |
|----------------|---------|-----|---------|------|---------------|
| Third-Party Applications Allowed | Binary | No risk | - | Risk | SP-ES-006, OD-ES-003 |
| High Risk Permissions on Documents | % | <5 | 5-15 | >15 | AC-001-SPO, AC-001-OD |
| Stale Direct User Permissions | % | <5 | 5-15 | >15 | AC-001-SPO, AC-001-OD |
| Sites with Broken Permissions Inheritance | % | <60 | 60-100 | >100 | AC-006 |
| External and Anonymous Sharing of Sensitive Data | % | <5 | 5-15 | >15 | SP-ES-001, SP-ES-002, ES-001-SPO, ES-001-OD |
| Unlabeled Sensitive Files | % | <10 | 10-30 | >30 | DC-001-SPO, DC-001-OD |
| Stale User Access to Sensitive Data | % | <5 | 5-15 | >15 | AC-001-SPO, AC-001-OD (filtered for sensitive) |
| Open Access to Sensitive Data | % | <0 | <2 | ≥2 | DE-003, AC-002-SPO, AC-002-OD |
| High-Risk Permissions to Sensitive Data | % | <0 | <2 | ≥2 | AC-001-SPO, AC-001-OD (Full Control) |

**Platform Coverage:** SharePoint Online, OneDrive
**Maturity Levels:** Primarily Level 1-3 (Critical → Baseline)

### 2.2 Identity Category (20 risks)

| 1Secure Metric | Measure | Low | Medium | High | Maps to DRIVE |
|----------------|---------|-----|---------|------|---------------|
| User Accounts with "Password Never Expires" | Num | 0 | 1-6 | >6 | AD-010 |
| User Accounts with "Password Not Required" | Num | 0 | 1-3 | >3 | AD-005 |
| Inactive User Accounts | % | <0.01 | 0.01-1 | >1 | AD-001 |
| User Accounts with Administrative Permissions | % | <2 | 2-3 | >3 | AD-011, AD-012 |
| Administrative Groups | % | <2 | 2-3 | >3 | AD-013 |
| Empty Security Groups | % | <1 | 1-2 | >2 | AD-019 |
| Dangerous Default Permissions | Binary | No risk | - | Risk | AD-038 |
| Improper Number of Global Administrators | Binary | No risk | - | Risk | AD-016 |
| Conditional Access Policy Disables Admin Token Persistence | Binary | No risk | - | Risk | AD-035 |
| Self-Serve Password Reset is Not Enabled | Binary | No risk | - | Risk | AD-034 |
| MS Graph Powershell Service Principal Assignment Not Enforced | Binary | No risk | - | Risk | AD-046 |
| Stale Guest Accounts | Num | 0 | 1-5 | >5 | AD-002 |
| User Accounts with "No MFA Configured" | Num | 0 | 1-5 | >5 | AD-014 |
| User Accounts Created via Email Verified Self-Service Creation | Num | 0 | 1-5 | >5 | AD-036 |
| Global Administrators | Num | <4 | 4 | ≥5 | AD-016 |
| Unusual Primary Group on Computer Account | Num | <5 | 5-10 | >10 | AD-027 |
| Restriction of Dangerous Privileges for Standard Users | Num | 0 | 1-5 | >5 | AD-038 |
| Review of Delegated Permissions for Standard Users on OUs | Num | <5 | 5-10 | >10 | AD-039 |
| Same Domain SID History Association | Num | 0 | - | ≥1 | AD-041 |
| Well-Known SIDs in SID History | Num | 0 | - | ≥1 | AD-041 |
| Administrative Accounts Susceptible to Kerberoasting | Num | 0 | - | ≥1 | AD-030 |
| Domain Controller RPC Coercion | Num | 0 | - | ≥1 | AD-049 |
| Admin Accounts with Email Access | Num | <5 | ≥5 | - | AD-023 |

**Platform Coverage:** Entra ID, Active Directory
**Maturity Levels:** Primarily Level 1-2 (Critical → High Risk)

### 2.3 Infrastructure Category (23 risks)

| 1Secure Metric | Measure | Low | Medium | High | Maps to DRIVE |
|----------------|---------|-----|---------|------|---------------|
| Disabled Computer Accounts | % | <1 | 1-3 | >3 | AD-002 (computers) |
| Inactive Computer Accounts | % | <0.01 | 0.01-3 | >3 | AD-001 (computers) |
| Unified Audit Log Search is Not Enabled | Binary | No risk | - | Risk | AD-034 |
| Conditional Access Policies and MS Secure Defaults status | Binary | No risk | - | Risk | AD-035 |
| Expired Domain Registrations Found | Binary | No risk | - | Risk | AD-056 |
| MS Graph Powershell Service Principal Configuration Missing | Binary | No risk | - | Risk | AD-046 |
| Legacy authentication protocols enabled | Num | 0 | - | ≥1 | AD-034 |
| Domain Controller SMB v1 Vulnerability | Num | 0 | - | ≥1 | AD-060 |
| Domain Controller Registration Status | Num | 0 | 1-3 | >3 | AD-047 |
| Domain Controller Logon Privileges Restriction | Num | 0 | - | ≥1 | AD-048 |
| Domain Controller Ownership Verification | Num | 0 | 1-5 | >5 | AD-050 |
| ESC1: Vulnerable Subject Control in Certificate Templates | Num | 0 | - | ≥1 | AD-052 |
| ESC2: Vulnerable EKU Configurations in Certificate Templates | Num | 0 | - | ≥1 | AD-053 |
| ESC3: Misconfigured Agent Enrollment Templates | Num | 0 | - | ≥1 | AD-054 |
| ESC4: Low-Privileged User Access to Published Certificate Templates | Num | 0 | - | ≥1 | AD-055 |
| Obsolete Windows Server 2012 Member Servers | Num | <6 | 6-21 | >21 | AD-057 |
| Obsolete Windows 2012 Domain Controllers | Num | 0 | - | ≥1 | AD-058 |
| OU Accidental Deletion Protection | Num | 0 | ≥1 | - | AD-059 |
| Weak TLS Protocols used by LDAPS | Num | 0 | ≥1 | - | AD-060 |
| Outdated Domain Functional Level (2012R2) | Num | 0 | ≥1 | - | AD-061 |

**Platform Coverage:** Active Directory, Entra ID, M365 Infrastructure
**Maturity Levels:** Primarily Level 1-3 (Critical → Baseline)

---

## 3. DRIVE Integration Architecture

### 3.1 Multi-Level Threshold Model

Each 1Secure risk maps to one or more DRIVE checks with **multiple severity thresholds**:

```yaml
# Example: External and Anonymous Sharing of Sensitive Data
1secure_metric: "External and Anonymous Sharing of Sensitive Data"
thresholds:
  - level: 1  # Critical Exposure
    condition: "≥15% of sensitive files shared externally/anonymously"
    severity: "Critical"
    drive_checks: ["SP-ES-001", "SP-ES-002"]
    points_deduction: 45

  - level: 2  # High Risk
    condition: "5-15% of sensitive files shared externally/anonymously"
    severity: "High"
    drive_checks: ["ES-001-SPO", "ES-001-OD"]
    points_deduction: 25

  - level: 3  # Medium Risk
    condition: "<5% of sensitive files shared externally/anonymously"
    severity: "Medium"
    drive_checks: ["ES-002-SPO", "ES-002-OD"]
    points_deduction: 10
```

### 3.2 Binary Level Advancement

Organizations must **pass ALL checks** at a level to advance:

```
Level 1 (Critical Exposure) - PASSED if ALL Level 1 checks pass:
  ✅ SP-ES-001: No anonymous links to sensitive data (High threshold)
  ✅ SP-ES-002: No edit permissions on anonymous links
  ✅ AD-010: Zero "Password Never Expires" accounts (High threshold)
  ✅ AD-005: Zero "Password Not Required" accounts
  ✅ AD-030: Zero Kerberoastable admin accounts
  ... (all Level 1 checks must pass)

Level 2 (High Risk Mitigated) - PASSED if Level 1 + ALL Level 2 checks pass:
  ✅ All Level 1 checks (inherited)
  ✅ ES-001-SPO: Guest access to sensitive SharePoint content controlled
  ✅ AD-014: All users have MFA configured
  ✅ AD-016: Global Admin count ≤4
  ... (all Level 2 checks must pass)
```

### 3.3 Dual Scoring Domains

Organizations receive two separate scores that must **both advance** together:

**Data Security Domain** (D+R+V pillars):
- SharePoint sensitive data exposure
- OneDrive sharing controls
- Data classification hygiene
- Access control maturity

**Identity Security Domain** (I+R+E pillars):
- Entra ID misconfigurations
- Active Directory vulnerabilities
- Authentication weaknesses
- Privilege escalation risks

**Overall Maturity = MIN(Data Security Level, Identity Security Level)**

---

## 4. Replit Prototype Specifications

### 4.1 Architecture

```
┌─────────────────────────────────────────────────┐
│         Replit Frontend (React + Vite)          │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │   ANSSI-Style Control Graph               │ │
│  │   - PingCastle-inspired visualization     │ │
│  │   - Interactive level drilling            │ │
│  │   - Dual-domain scoring display           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │   Check Detail View                       │ │
│  │   - Multi-level threshold display         │ │
│  │   - Framework mappings (NIST, CIS, ISO)   │ │
│  │   - Remediation guidance                  │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │   Reports & Exports                       │ │
│  │   - Executive summary (PDF)               │ │
│  │   - Compliance gap analysis               │ │
│  │   - Remediation roadmap                   │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                       ↕
┌─────────────────────────────────────────────────┐
│     Replit Backend (Node.js + Express)          │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │   1Secure API Integration Layer           │ │
│  │   - Fetch risk metrics                    │ │
│  │   - Transform to DRIVE format             │ │
│  │   - Cache responses                       │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │   DRIVE Scoring Engine                    │ │
│  │   - Multi-level threshold evaluation      │ │
│  │   - Binary level advancement logic        │ │
│  │   - Dual-domain score calculation         │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │   YAML Catalog Parser                     │ │
│  │   - Load 52+ 1Secure-mapped checks        │ │
│  │   - Framework mapping enrichment          │ │
│  │   - Remediation guidance assembly         │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
                       ↕
┌─────────────────────────────────────────────────┐
│     Netwrix 1Secure API (External)              │
│                                                 │
│  - GET /api/organizations/{orgId}/risks         │
│  - GET /api/organizations/{orgId}/metrics       │
│  - GET /api/connectors/{connectorId}/status     │
└─────────────────────────────────────────────────┘
```

### 4.2 Data Models

#### 4.2.1 1Secure Risk Response

```typescript
interface OneSecureRiskMetric {
  category: 'Data' | 'Identity' | 'Infrastructure';
  metric: string;
  measureType: 'Binary' | 'Num' | '%';
  currentValue: number | boolean;
  thresholds: {
    low: string;
    medium: string;
    high: string;
  };
  currentSeverity: 'Low' | 'Medium' | 'High' | 'None';
  lastUpdated: string;
  affectedResources?: number;
  remediationAvailable: boolean;
}

interface OneSecureOrganizationScan {
  organizationId: string;
  organizationName: string;
  scanDate: string;
  connectors: {
    name: string;
    status: 'Healthy' | 'Warning' | 'Error';
    lastSync: string;
  }[];
  risks: OneSecureRiskMetric[];
}
```

#### 4.2.2 DRIVE Maturity Assessment

```typescript
interface DRIVECheck {
  checkId: string;
  title: string;
  platform: 'SharePoint' | 'OneDrive' | 'Active Directory' | 'Entra ID';
  category: string;
  drivePillars: ('D' | 'R' | 'I' | 'V' | 'E')[];

  // Multi-level thresholds
  levelThresholds: {
    level: 1 | 2 | 3 | 4 | 5;
    thresholdId: string;
    condition: string;
    severity: 'Critical' | 'High' | 'Medium' | 'Low';
    businessImpact: string;
    threatTimeline: string;
    pointsDeduction: number;
    remediationPriority: number;
  }[];

  // 1Secure integration
  oneSecureMapping?: {
    metric: string;
    measureType: string;
    evaluationLogic: string;
  };

  // Framework mappings
  frameworkMappings: {
    nistCsf?: { function: string; controls: string[] };
    cisV8?: { controls: string[] };
    cisM365?: { recommendations: string[] };
    iso27001?: { controls: string[] };
    mitreAttack?: { techniques: string[] };
  };

  // Remediation
  remediation: {
    automatedFixAvailable: boolean;
    oneSecureRemediable: boolean;
    fixComplexity: 'Low' | 'Medium' | 'High';
    estimatedTimeMinutes: number;
    steps: RemediationStep[];
  };
}

interface DRIVEMaturityScore {
  organizationId: string;
  assessmentDate: string;

  // Overall scoring
  overallLevel: 1 | 2 | 3 | 4 | 5;
  dataSecurityLevel: 1 | 2 | 3 | 4 | 5;
  identitySecurityLevel: 1 | 2 | 3 | 4 | 5;

  // Level-by-level breakdown
  levelResults: {
    level: number;
    totalChecks: number;
    passedChecks: number;
    failedChecks: number;
    blockedBy: string[];  // Check IDs blocking advancement
    pointsDeducted: number;
  }[];

  // Domain breakdown
  dataDomain: {
    totalPoints: number;
    pointsDeducted: number;
    score: number;
    failedChecks: DRIVECheckResult[];
  };

  identityDomain: {
    totalPoints: number;
    pointsDeducted: number;
    score: number;
    failedChecks: DRIVECheckResult[];
  };

  // Remediation roadmap
  nextLevelRequirements: {
    targetLevel: number;
    checksToRemediate: DRIVECheckResult[];
    estimatedEffortHours: number;
    estimatedCost: number;
  };
}

interface DRIVECheckResult {
  check: DRIVECheck;
  status: 'pass' | 'fail' | 'not_applicable';
  failedThreshold?: {
    level: number;
    condition: string;
    currentValue: any;
    expectedValue: any;
  };
  affectedResources: number;
  remediationPriority: number;
}
```

### 4.3 API Endpoints

#### 4.3.1 1Secure Integration APIs

```
GET /api/1secure/organizations
  → List available 1Secure organizations

GET /api/1secure/organizations/:orgId/scan
  → Fetch latest 1Secure risk scan for organization
  Response: OneSecureOrganizationScan

POST /api/1secure/organizations/:orgId/sync
  → Trigger fresh sync from 1Secure API
  Response: { jobId: string, status: 'queued' }

GET /api/1secure/sync/:jobId
  → Check status of sync job
  Response: { status: 'running'|'completed'|'failed', progress: number }
```

#### 4.3.2 DRIVE Maturity APIs

```
GET /api/drive/checks
  → List all DRIVE checks with 1Secure mappings
  Query params: ?platform=SharePoint&level=1
  Response: DRIVECheck[]

GET /api/drive/checks/:checkId
  → Get detailed check definition
  Response: DRIVECheck

POST /api/drive/assess/:orgId
  → Run DRIVE maturity assessment for organization
  Request: { includeRemediation: boolean }
  Response: DRIVEMaturityScore

GET /api/drive/assess/:orgId/latest
  → Get most recent assessment results
  Response: DRIVEMaturityScore

GET /api/drive/assess/:orgId/history
  → Get historical assessment trend
  Response: DRIVEMaturityScore[]
```

#### 4.3.3 Reporting APIs

```
GET /api/reports/:orgId/executive-summary
  → Generate executive summary (PDF)
  Response: application/pdf

GET /api/reports/:orgId/compliance-gap/:framework
  → Framework-specific gap analysis (NIST CSF, CIS v8, ISO 27001)
  Response: ComplianceGapReport

GET /api/reports/:orgId/remediation-roadmap
  → Prioritized remediation plan
  Response: RemediationRoadmap
```

### 4.4 UI/UX Requirements

#### 4.4.1 Landing Page (ANSSI-Style)

```
┌────────────────────────────────────────────────────┐
│  [Netwrix Logo]    DRIVE Maturity Assessment       │
│                                                    │
│  Organization: Gobias Industries                   │
│  Last Scan: 2025-10-14 12:34 UTC                  │
│  [Refresh Scan]                                    │
├────────────────────────────────────────────────────┤
│                                                    │
│   ┌──────────────────────────────────────────┐   │
│   │  Overall Maturity: Level 2 / 5           │   │
│   │  ████████░░░░░░░░░░░░░░░░░░░░  40%      │   │
│   │                                          │   │
│   │  Data Security:     Level 3 / 5          │   │
│   │  Identity Security: Level 2 / 5 ⚠️       │   │
│   │                                          │   │
│   │  Blocked by: 8 Identity checks          │   │
│   └──────────────────────────────────────────┘   │
│                                                    │
│   ┌──────────────────────────────────────────┐   │
│   │  PingCastle-Style Control Graph          │   │
│   │                                          │   │
│   │    [1]──────[2]──────[3]──────[4]──────[5]│   │
│   │     ✅      ❌       ⏭️       ⏭️       ⏭️  │   │
│   │   Critical  High   Medium   Low  State-of-│   │
│   │   Exposure  Risk   Baseline Enhanced  Art │   │
│   │                                          │   │
│   │   Click level for detail view →         │   │
│   └──────────────────────────────────────────┘   │
│                                                    │
│  [View Full Report]  [Download PDF]  [Remediate]  │
└────────────────────────────────────────────────────┘
```

#### 4.4.2 Level Detail View

```
┌────────────────────────────────────────────────────┐
│  ← Back to Overview                                │
│                                                    │
│  Level 2: High Risk Mitigated                     │
│  ████████████░░░░░░░░░  42 checks (34 passed)     │
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  ❌ Blocking Advancement (8 checks)       │    │
│  │                                          │    │
│  │  🔴 AD-014: Users with No MFA Configured │    │
│  │     5 users found (threshold: 0)          │    │
│  │     Pillar: Identity | Points: -15        │    │
│  │     [View Details] [Remediate in 1Secure] │    │
│  │                                          │    │
│  │  🔴 AD-016: Excessive Global Admins      │    │
│  │     5 admins found (threshold: ≤4)        │    │
│  │     Pillar: Identity | Points: -20        │    │
│  │     [View Details] [Remediate in 1Secure] │    │
│  │                                          │    │
│  │  ... 6 more checks                        │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ┌──────────────────────────────────────────┐    │
│  │  ✅ Passed Checks (34 checks)             │    │
│  │                                          │    │
│  │  ✓ AD-010: Password Never Expires         │    │
│  │  ✓ AD-005: Password Not Required          │    │
│  │  ✓ AD-030: Kerberoastable Admins          │    │
│  │  ... 31 more                              │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  [Generate Remediation Plan]  [Export to CSV]     │
└────────────────────────────────────────────────────┘
```

#### 4.4.3 Check Detail Modal

```
┌────────────────────────────────────────────────────┐
│  AD-014: User Accounts with "No MFA Configured"    │
│  Platform: Entra ID | Category: Identity           │
│  [Close X]                                         │
├────────────────────────────────────────────────────┤
│                                                    │
│  📊 Current Status: FAIL                           │
│  🔴 5 accounts without MFA (Level 2 threshold: 0)  │
│                                                    │
│  📈 Multi-Level Thresholds:                        │
│  ┌──────────────────────────────────────────┐    │
│  │ Level 1: N/A                             │    │
│  │ Level 2: 0 accounts → HIGH (-15 pts) ❌  │    │
│  │ Level 3: ≤3 accounts → MEDIUM (-8 pts)   │    │
│  │ Level 4: ≤1 account → LOW (-3 pts)        │    │
│  └──────────────────────────────────────────┘    │
│                                                    │
│  ⚠️ Business Impact:                               │
│  Accounts without MFA are vulnerable to           │
│  credential stuffing and password spray attacks.  │
│  Expected exploitation timeline: Days to weeks.   │
│                                                    │
│  🗂️ Framework Mappings:                            │
│  • NIST CSF: IA-5 (Authenticator Management)      │
│  • CIS v8: Control 6.5 (MFA for All Users)        │
│  • ISO 27001: A.9.4.2 (Secure log-on)             │
│  • MITRE ATT&CK: T1078 (Valid Accounts)           │
│                                                    │
│  🛠️ Remediation Steps:                             │
│  1. Identify accounts: Export user list without MFA│
│  2. Contact users: Email security awareness       │
│  3. Enable MFA: Use Entra ID conditional access   │
│  4. Verify: Re-scan to confirm                    │
│                                                    │
│  Time: ~120 minutes | Complexity: Medium          │
│                                                    │
│  [Remediate in 1Secure] [Export Affected Users]   │
└────────────────────────────────────────────────────┘
```

### 4.5 Technology Stack

**Frontend:**
- React 18 + TypeScript
- Vite (build tool)
- TanStack Query (data fetching)
- Recharts (visualization)
- Tailwind CSS + shadcn/ui components
- React Router (navigation)

**Backend:**
- Node.js 20+ LTS
- Express.js
- TypeScript
- Axios (1Secure API client)
- js-yaml (YAML parsing)
- node-cache (in-memory caching)

**Deployment:**
- Replit deployment
- Environment variables for 1Secure API credentials
- GitHub integration for YAML catalog sync

### 4.6 Configuration

#### 4.6.1 Environment Variables

```bash
# 1Secure API Configuration
ONESECURE_API_URL=https://1secure-qc.nwxcorp.com
ONESECURE_API_KEY=<your-api-key>
ONESECURE_ORGANIZATION_ID=<default-org-id>

# DRIVE Configuration
DRIVE_CATALOG_PATH=./checks
DRIVE_ENABLE_CACHING=true
DRIVE_CACHE_TTL_SECONDS=3600

# Feature Flags
ENABLE_1SECURE_REMEDIATION=true
ENABLE_PDF_EXPORT=true
ENABLE_MULTI_ORG=false
```

#### 4.6.2 1Secure API Integration

```typescript
// services/onesecure-client.ts
import axios from 'axios';

class OneSecureClient {
  private baseUrl: string;
  private apiKey: string;

  constructor() {
    this.baseUrl = process.env.ONESECURE_API_URL!;
    this.apiKey = process.env.ONESECURE_API_KEY!;
  }

  async getOrganizationRisks(orgId: string): Promise<OneSecureRiskMetric[]> {
    const response = await axios.get(
      `${this.baseUrl}/api/organizations/${orgId}/risks`,
      {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data.risks;
  }

  async getConnectorStatus(orgId: string): Promise<ConnectorStatus[]> {
    // Implementation
  }

  async triggerRescan(orgId: string): Promise<ScanJob> {
    // Implementation
  }
}
```

---

## 5. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Replit project structure
- [ ] Implement YAML catalog parser
- [ ] Create 1Secure API client
- [ ] Build DRIVE scoring engine (multi-level thresholds)
- [ ] Implement binary level advancement logic
- [ ] Create dual-domain scoring calculation

### Phase 2: Core Features (Week 3-4)
- [ ] Build landing page with overall score
- [ ] Implement PingCastle-style control graph
- [ ] Create level detail view
- [ ] Build check detail modal
- [ ] Add framework mapping display
- [ ] Implement remediation guidance

### Phase 3: Integration (Week 5-6)
- [ ] Connect to 1Secure QC environment
- [ ] Map all 52 1Secure risks to DRIVE checks
- [ ] Implement real-time sync
- [ ] Add caching layer
- [ ] Test with production data

### Phase 4: Reporting (Week 7-8)
- [ ] Executive summary PDF generation
- [ ] Compliance gap analysis (NIST, CIS, ISO)
- [ ] Remediation roadmap export
- [ ] Historical trend tracking
- [ ] Email report scheduling

### Phase 5: Polish (Week 9-10)
- [ ] UI/UX refinement (ANSSI styling)
- [ ] Performance optimization
- [ ] Error handling and edge cases
- [ ] User documentation
- [ ] Stakeholder demo preparation

---

## 6. Success Metrics

### 6.1 Technical Metrics
- **API Response Time:** <2 seconds for full assessment
- **Sync Reliability:** >99% successful 1Secure API calls
- **Cache Hit Rate:** >80% for repeated queries
- **Data Freshness:** <5 minutes latency from 1Secure

### 6.2 User Metrics
- **Time to Insight:** <30 seconds from landing page to understanding current maturity
- **Remediation Clarity:** 100% of failing checks have actionable remediation steps
- **Framework Coverage:** 100% of checks mapped to ≥2 frameworks
- **Export Usage:** >50% of users export remediation roadmap

### 6.3 Business Metrics
- **Customer Adoption:** >80% of 1Secure customers use DRIVE assessment
- **Maturity Improvement:** Average 1-level increase within 6 months
- **Remediation Rate:** >60% of failing checks remediated within 90 days
- **Executive Engagement:** >40% of assessments shared with C-level

---

## 7. Risks and Mitigations

### 7.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| 1Secure API changes break integration | High | Medium | Version API client, implement robust error handling, maintain backward compatibility |
| YAML catalog drift from 1Secure capabilities | Medium | High | Automate mapping validation, CI/CD checks for consistency |
| Performance issues with large datasets | Medium | Medium | Implement pagination, lazy loading, server-side aggregation |
| Replit resource limits | Low | Low | Optimize bundle size, use CDN for assets, consider upgrade |

### 7.2 Product Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| Customers don't understand multi-level thresholds | High | Medium | Interactive tutorial, tooltips, video walkthrough |
| Binary advancement feels too strict | Medium | High | Educational content on threat-focused model, show partial progress |
| Framework mappings confuse users | Low | Medium | Progressive disclosure, hide by default with "Show more" |
| Remediation steps too generic | High | Medium | Partner with 1Secure team for product-specific guidance |

---

## 8. Open Questions

1. **1Secure API Access:** Do we have full API documentation for risk metrics endpoint?
2. **Remediation Integration:** Can 1Secure API accept remediation actions programmatically?
3. **Multi-Tenancy:** Should prototype support multiple organizations or single-org POC?
4. **Authentication:** SSO integration with 1Secure or separate auth?
5. **Pricing Model:** Will DRIVE assessment be bundled with 1Secure or separate SKU?
6. **Data Residency:** Any compliance requirements for storing assessment results?
7. **Historical Data:** How many months of trend data should we display?
8. **Alert Threshold:** Should we alert when maturity level drops?

---

## 9. Appendix

### 9.1 1Secure Risk to DRIVE Check Mapping (Detailed)

See `/analysis/1secure_integration.json` for full programmatic mapping.

### 9.2 YAML Check Format Specification

See `/checks/README.md` for detailed check format documentation.

### 9.3 Scoring Algorithm Pseudocode

```python
def calculate_drive_maturity(org_risks: List[OneSecureRisk]) -> DRIVEScore:
    # Load DRIVE catalog
    checks = load_yaml_catalog()

    # Map 1Secure risks to DRIVE checks
    check_results = []
    for risk in org_risks:
        mapped_checks = get_mapped_checks(risk)
        for check in mapped_checks:
            result = evaluate_check(check, risk)
            check_results.append(result)

    # Calculate level advancement
    data_domain_checks = [c for c in check_results if c.pillar in ['D', 'R', 'V']]
    identity_domain_checks = [c for c in check_results if c.pillar in ['I', 'R', 'E']]

    data_level = calculate_domain_level(data_domain_checks)
    identity_level = calculate_domain_level(identity_domain_checks)

    # Overall = minimum of both domains
    overall_level = min(data_level, identity_level)

    return DRIVEScore(
        overall_level=overall_level,
        data_level=data_level,
        identity_level=identity_level,
        check_results=check_results
    )

def calculate_domain_level(checks: List[CheckResult]) -> int:
    # Binary advancement: must pass ALL checks at level to advance
    for level in range(1, 6):
        level_checks = [c for c in checks if c.min_level == level]
        failed_checks = [c for c in level_checks if c.status == 'fail']

        if len(failed_checks) > 0:
            # Blocked at this level
            return level - 1 if level > 1 else 0

    # Passed all levels
    return 5
```

---

## 10. References

- ANSSI Maturity Model: https://www.cert.ssi.gouv.fr/
- PingCastle Methodology: https://pingcastle.com/
- NIST Cybersecurity Framework 2.0: https://www.nist.gov/cyberframework
- CIS Controls v8: https://www.cisecurity.org/controls/v8
- ISO/IEC 27001:2022: https://www.iso.org/standard/27001
- MITRE ATT&CK: https://attack.mitre.org/
- Netwrix 1Secure: https://www.netwrix.com/1secure.html

---

**Document Status:** Draft for Review
**Next Review:** Weekly during implementation
**Feedback:** Contact DRIVE team or open issue in GitHub repo
