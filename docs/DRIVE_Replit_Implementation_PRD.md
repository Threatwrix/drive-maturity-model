# DRIVE Replit Implementation PRD - Maturity Assessment Platform

## 1. Executive Summary

Build a **DRIVE Maturity Assessment** web application in Replit that integrates with this GitHub repository to provide real-time security maturity scoring for Microsoft 365, Active Directory, and related platforms.

**DRIVE** = **Data Risk and Identity Vulnerability Exposure** maturity assessment

**Target URL**: https://1securexspm.replit.app/maturity-level

## 2. Core Requirements

### 2.1 Data Integration
- **Pull catalog data** from this GitHub repository (`drive-risk-catalog`)
- **Real-time updates** when catalog changes are pushed
- **JSON API endpoints** to serve risk checks and maturity definitions
- **Version tracking** to ensure data consistency

### 2.2 Assessment Simulation Engine
```javascript
// Core simulation logic structure
const assessmentEngine = {
  platforms: ['M365', 'ActiveDirectory', 'Exchange', 'SharePoint', 'OneDrive', 'Teams'],
  riskChecks: 117, // Total from catalog
  scoringModel: 'logistic_exposure', // Per PRD formula
  maturityLevels: 5
}
```

### 2.3 User Experience Flow
1. **Platform Selection** - Choose which platforms to assess
2. **Risk Simulation** - Generate realistic risk scenarios  
3. **Score Calculation** - Apply DRIVE scoring methodology
4. **Maturity Level Display** - Show current level + path to next level
5. **Remediation Guidance** - Actionable steps to improve score

## 3. Technical Architecture 

### 3.1 Frontend (React/Next.js)
```
/components
  ├── AssessmentDashboard.jsx
  ├── MaturityLevelCard.jsx  
  ├── RiskCheckList.jsx
  ├── ScoreVisualization.jsx
  └── RemediationPanel.jsx

/pages
  ├── index.js (Landing)
  ├── maturity-level.js (Main Assessment)
  └── api/
      ├── catalog.js (GitHub data proxy)
      ├── assessment.js (Scoring engine)
      └── simulation.js (Risk generation)
```

### 3.2 Data Layer Integration
```javascript
// GitHub integration
const CATALOG_BASE_URL = 'https://raw.githubusercontent.com/Threatwrix/drive-maturity-model/main'

const endpoints = {
  riskCatalog: `${CATALOG_BASE_URL}/catalog/drive_risk_catalog.json`,
  maturityLevels: `${CATALOG_BASE_URL}/levels/levels.yaml`, 
  scoringConfig: `${CATALOG_BASE_URL}/scoring/scoring.yaml`
}
```

### 3.3 Simulation Engine Logic
```javascript
const SimulationEngine = {
  generateRiskScenario: (platform, userProfile) => {
    // Create realistic risk distribution based on:
    // - Platform type (M365 vs AD vs hybrid)
    // - Organization size 
    // - Industry vertical
    // - Current maturity level estimate
  },
  
  calculateDRIVEScore: (riskFindings, policyChecks) => {
    // Apply logistic exposure formula from PRD
    // Risk Points = SeverityWeight × ExposureFactor
    // ExposureFactor = 1 / (1 + e^(-k × (PctAffected – 0.15)))
  },
  
  determinateMaturityLevel: (score, controlsPass) => {
    // Level gating logic - both score AND required controls
    // From levels.yaml required_controls + policy_checks
  }
}
```

## 4. DRIVE Maturity Model Implementation

### 4.1 Five-Level Structure
Each level requires **both** score threshold AND control validation:

**Level 1: Foundational (0-19 points)**
- Focus: Basic hygiene, reactive posture
- Key Controls: Strong admin passwords, no anonymous sharing
- Policy Checks: Password policy, external sharing restrictions
- Measurement: Pass/fail on security basics

**Level 2: Baseline (20-39 points)**  
- Focus: MFA and guest management
- Key Controls: Privileged MFA, guest expiration, audit logging
- Policy Checks: Conditional access exists, external sharing requires auth
- Measurement: Policy configuration + risk coverage

**Level 3: Managed (40-59 points)**
- Focus: Consistent enforcement, data classification  
- Key Controls: CA policies, sensitivity labels, access reviews
- Policy Checks: DLP active, legacy auth blocked, break-glass tested
- Measurement: Policy effectiveness + enforcement + review cycles

**Level 4: Advanced (60-79 points)**
- Focus: Automation and behavioral analytics
- Key Controls: PIM, auto-labeling, continuous monitoring
- Policy Checks: Zero Trust, Cloud App Security, insider risk management
- Measurement: Automation coverage + MTTR + policy adherence

**Level 5: Optimized (80-100 points)**
- Focus: Predictive security, policy-as-code
- Key Controls: ML risk scoring, infrastructure as code, automated retention
- Policy Checks: GitOps, AI anomaly detection, predictive recommendations
- Measurement: Predictive accuracy + automation + business alignment

### 4.2 Scoring Methodology
```yaml
total_score_calculation:
  risk_assessment: 70  # 0-70 points from 117 risk checks
  policy_bonus: 20     # 0-20 points from policy implementation
  automation_bonus: 10 # 0-10 points from automation level
  
level_gating:
  score_threshold: true    # Must meet minimum score
  required_controls: true  # Must pass all required controls
  policy_checks: true      # Must have policy configurations
```

## 5. User Interface Requirements

### 5.1 Assessment Dashboard
- **Current DRIVE Score** (0-100 with level badge)
- **Platform Coverage** (which systems assessed)
- **Risk Distribution** (by severity: Critical, High, Medium, Low)
- **Level Progress** (current level + next level requirements)

### 5.2 Interactive Elements
- **Platform toggles** (M365, AD, Exchange, etc.)
- **Organizational inputs** (size, industry, current security tools)
- **Scenario generation** ("Run assessment" button)
- **Remediation roadmap** (prioritized action items)

### 5.3 Visualization Components
```javascript
const visualizations = [
  'RadialScoreGauge',      // 0-100 DRIVE score
  'MaturityLevelSteps',    // 5-step progress indicator  
  'RiskHeatmap',          // Platform × severity matrix
  'TrendLine',            // Historical or projected improvement
  'ComplianceRadar'       // Framework coverage (NIST, CIS, ISO)
]
```

## 6. Data Requirements from GitHub

### 6.1 Required Files to Pull
```javascript
const requiredData = {
  'catalog/drive_risk_catalog.json': 'All 117 risk checks with metadata',
  'levels/levels.yaml': 'Maturity level definitions and requirements',
  'scoring/scoring.yaml': 'Scoring categories and weights',
  'frameworks/*.csv': 'Compliance framework mappings'
}
```

### 6.2 API Endpoints to Create
```javascript
// Replit API routes
GET /api/catalog           // Full risk catalog
GET /api/levels           // Maturity level definitions  
GET /api/assessment       // Run assessment simulation
POST /api/simulate        // Generate risk scenario
GET /api/frameworks       // Compliance mappings
```

## 7. Assessment Simulation Logic

### 7.1 Threat-Focused Risk Simulation
```javascript
const generateRealisticRisks = (inputs) => {
  const { platforms, orgSize, industry, currentTools } = inputs
  
  // Generate risk scenarios based on threat timeline
  const risksByLevel = {
    level1: generateCriticalExposure(inputs),    // Immediate threats
    level2: generateHighRiskScenarios(inputs),   // Short-term risks  
    level3: generateBaselineGaps(inputs),        // Standard security gaps
    level4: generateProactiveNeeds(inputs),      // Advanced automation gaps
    level5: generateOptimizationGaps(inputs)     // State-of-the-art gaps
  }
  
  return {
    riskFindings: combineRiskLevels(risksByLevel),
    maturityLevel: calculateDRIVELevel(risksByLevel),
    remediationPlan: generateThreatFocusedPlan(risksByLevel),
    complianceGaps: mapToFrameworks(risksByLevel)
  }
}

const generateCriticalExposure = (inputs) => {
  // Level 1: Immediate threats (exploitable in hours/days)
  const criticalRisks = [
    'anonymous-sharing-enabled',
    'admin-password-never-expires', 
    'anyone-links-present',
    'unconstrained-delegation',
    'clear-text-passwords'
  ]
  
  return simulateRiskPresence(criticalRisks, inputs)
}
```

### 7.2 Binary Maturity Level Calculation
```javascript
const calculateDRIVEMaturityLevel = (riskFindings) => {
  // New simplified binary model
  const levelChecks = {
    1: filterRisksByLevel(riskFindings, 1),  // 16 critical exposure checks
    2: filterRisksByLevel(riskFindings, 2),  // 42 high risk checks
    3: filterRisksByLevel(riskFindings, 3),  // 35 baseline checks
    4: filterRisksByLevel(riskFindings, 4),  // 12 proactive checks
    5: filterRisksByLevel(riskFindings, 5)   // 12 state-of-art checks
  }
  
  // Calculate highest level where ALL checks pass
  let maturityLevel = 0
  
  for (let level = 1; level <= 5; level++) {
    const levelRisks = levelChecks[level]
    const allPassed = levelRisks.every(risk => risk.status === 'pass')
    
    if (allPassed) {
      maturityLevel = level
    } else {
      // Failed at this level - return previous level
      break
    }
  }
  
  return {
    currentLevel: maturityLevel,
    levelName: getLevelName(maturityLevel),
    blockers: getFailedChecks(levelChecks[maturityLevel + 1]),
    nextSteps: generateRemediationSteps(maturityLevel + 1),
    threatTimeline: getThreatTimeline(maturityLevel)
  }
}

const getLevelName = (level) => {
  const names = {
    0: "Unassessed",
    1: "Critical Exposure (Immediate Threat)", 
    2: "High Risk Mitigated (Short-term Protection)",
    3: "Standard Security Baseline (Default Plus)",
    4: "Enhanced Security Posture (Proactive Management)", 
    5: "State-of-the-Art Security (Continuous Excellence)"
  }
  return names[level]
}
```

## 8. Success Metrics

### 8.1 Technical KPIs
- **Data sync latency**: < 5 minutes from GitHub push to Replit update
- **Assessment speed**: < 3 seconds to generate full simulation
- **Accuracy**: Realistic risk distributions matching real customer patterns
- **Coverage**: All 117 risk checks properly weighted and scored

### 8.2 User Experience KPIs  
- **Assessment completion rate**: > 80%
- **Time to insight**: < 2 minutes from start to DRIVE score
- **Actionability**: Clear next steps for each maturity level
- **Framework mapping**: Clear compliance posture across 16+ standards

## 9. Implementation Roadmap

### Phase 1: Core Assessment Engine (Week 1)
- GitHub integration and data pull
- Basic scoring algorithm implementation  
- Simple UI with score display

### Phase 2: Enhanced UX (Week 2)
- Interactive platform selection
- Risk scenario generation
- Maturity level visualization with progress indicators

### Phase 3: Advanced Features (Week 3)
- Remediation roadmaps
- Compliance framework reporting
- Historical tracking and trends

### Phase 4: Production Polish (Week 4)
- Performance optimization
- Error handling and edge cases
- Documentation and API specifications

## 10. Integration Points

### 10.1 GitHub Repository Structure
```
Threatwrix/drive-maturity-model/
├── catalog/drive_risk_catalog.json    # 117 risk checks
├── levels/levels.yaml                 # 5 maturity levels  
├── scoring/scoring.yaml              # Scoring methodology
├── frameworks/                       # Compliance mappings
└── docs/                            # Implementation guides
```

### 10.2 Replit Integration
- **Environment variables** for GitHub token/access
- **Cron jobs** or webhooks for data synchronization  
- **Caching strategy** for performance optimization
- **Error handling** for GitHub API failures

This PRD provides the complete roadmap for implementing your DRIVE maturity assessment in Replit, pulling live data from the GitHub repository we're building together.