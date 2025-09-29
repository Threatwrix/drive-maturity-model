# DRIVE Replit Implementation PRD - Maturity Assessment Platform

## 1. Executive Summary

Build a **DRIVE Maturity Assessment** web application in Replit that integrates with this GitHub repository to provide real-time threat-focused maturity assessment for Microsoft 365, Active Directory, and related platforms.

**DRIVE** = **Data Risk and Identity Vulnerability Exposure** maturity assessment using PingCastle-inspired binary advancement model

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
  assessmentModel: 'threat_focused_binary', // PingCastle-inspired binary advancement
  maturityLevels: 5,
  levelDistribution: {
    1: 16, // Critical Exposure (Immediate Threat)
    2: 42, // High Risk Mitigated (Short-term Protection)
    3: 35, // Standard Security Baseline (Default Plus)
    4: 12, // Enhanced Security Posture (Proactive Management)
    5: 12  // State-of-the-Art Security (Continuous Excellence)
  }
}
```

### 2.3 User Experience Flow
1. **Platform Selection** - Choose which platforms to assess
2. **Risk Simulation** - Generate realistic risk scenarios based on threat timeline
3. **Binary Assessment** - Check pass/fail status for each threat level
4. **Maturity Level Display** - Show current level + specific blockers to next level
5. **Threat-Focused Remediation** - Actionable steps prioritized by threat timeline

## 3. Technical Architecture 

### 3.1 Frontend (React/Next.js)
```
/components
  ├── AssessmentDashboard.jsx
  ├── MaturityLevelCard.jsx  
  ├── ThreatTimelineView.jsx
  ├── BinaryCheckStatus.jsx
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

### 3.3 Binary Assessment Engine Logic
```javascript
const ThreatFocusedEngine = {
  generateThreatScenario: (platform, userProfile) => {
    // Create realistic risk scenarios by threat timeline:
    // - Level 1: Immediate threats (hours/days)
    // - Level 2: Short-term risks (weeks/months)  
    // - Level 3: Baseline security gaps
    // - Level 4: Advanced automation needs
    // - Level 5: State-of-the-art optimization gaps
  },
  
  assessMaturityLevel: (riskFindings) => {
    // Binary advancement model - NO complex scoring
    // Pass ALL checks at level = advance to next level
    // Fail ANY check at level = blocked at previous level
    return getHighestLevelWhereAllCheckPass(riskFindings)
  },
  
  identifyBlockers: (targetLevel, riskFindings) => {
    // Show specific failed checks preventing advancement
    // Prioritize by threat timeline (immediate threats first)
  }
}
```

## 4. DRIVE Threat-Focused Maturity Model

### 4.1 Binary Advancement Structure
Each level requires **ALL** checks to pass - no scoring thresholds:

**Level 1: Critical Exposure (Immediate Threat)** - 16 checks
- Focus: Stop immediate data leaks and admin compromises  
- Threat Timeline: Exploitable within hours/days
- Key Risks: Anonymous sharing, weak admin passwords, critical AD delegation
- Advancement: Pass ALL 16 critical exposure checks

**Level 2: High Risk Mitigated (Short-term Protection)** - 42 checks  
- Focus: Secure privileged access and external collaboration
- Threat Timeline: Exploitable within weeks/months
- Key Risks: Unmanaged guests, missing MFA, stale admin accounts
- Advancement: Pass ALL Level 1 + Level 2 checks (58 total)

**Level 3: Standard Security Baseline (Default Plus)** - 35 checks
- Focus: Implement industry standard security practices
- Threat Timeline: Standard security foundation
- Key Risks: Missing conditional access, no data classification, weak monitoring
- Advancement: Pass ALL Level 1-3 checks (93 total)

**Level 4: Enhanced Security Posture (Proactive Management)** - 12 checks
- Focus: Advanced automation and behavioral analytics
- Threat Timeline: Proactive threat prevention
- Key Risks: Manual processes, missing Zero Trust, no behavioral monitoring
- Advancement: Pass ALL Level 1-4 checks (105 total)

**Level 5: State-of-the-Art Security (Continuous Excellence)** - 12 checks
- Focus: Predictive security and policy-as-code
- Threat Timeline: Future-proofed security
- Key Risks: Reactive security, manual policy management, no prediction
- Advancement: Pass ALL 117 checks

### 4.2 Binary Assessment Methodology
```javascript
// No complex scoring - simple binary logic
const maturityLevel = assessBinaryProgression(riskFindings)

function assessBinaryProgression(findings) {
  for (let level = 1; level <= 5; level++) {
    const levelChecks = getLevelChecks(level)
    const allPassed = levelChecks.every(check => check.status === 'pass')
    
    if (!allPassed) {
      return {
        currentLevel: level - 1,
        blockedAt: level,
        failedChecks: getFailedChecks(levelChecks),
        threatPriority: getThreatTimeline(level)
      }
    }
  }
  return { currentLevel: 5, status: 'optimal' }
}
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
- **Coverage**: All 117 risk checks properly mapped to threat levels

### 8.2 User Experience KPIs  
- **Assessment completion rate**: > 80%
- **Time to insight**: < 2 minutes from start to DRIVE maturity level
- **Actionability**: Clear next steps for each maturity level
- **Framework mapping**: Clear compliance posture across 16+ standards

## 9. Implementation Roadmap

### Phase 1: Core Assessment Engine (Week 1)
- GitHub integration and data pull
- Binary assessment algorithm implementation  
- Simple UI with maturity level display

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
├── scoring/scoring.yaml              # Binary assessment methodology
├── frameworks/                       # Compliance mappings
└── docs/                            # Implementation guides
```

### 10.2 Replit Integration
- **Environment variables** for GitHub token/access
- **Cron jobs** or webhooks for data synchronization  
- **Caching strategy** for performance optimization
- **Error handling** for GitHub API failures

This PRD provides the complete roadmap for implementing your DRIVE maturity assessment in Replit, pulling live data from the GitHub repository we're building together.