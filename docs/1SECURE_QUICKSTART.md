# 1Secure + DRIVE Integration Quick Start
## Get Started in 5 Minutes

---

## What You Have Now

✅ **52 1Secure risks mapped** to DRIVE maturity model
✅ **Comprehensive PRD** with full technical specifications
✅ **Integration JSON** ready for Replit consumption
✅ **Mapping analysis** showing coverage and gaps
✅ **Implementation roadmap** with 10-week timeline

---

## Key Files Created

| File | Purpose | Use For |
|------|---------|---------|
| **1SECURE_INTEGRATION_PRD.md** | 60-page comprehensive product spec | Replit development, stakeholder alignment |
| **1SECURE_INTEGRATION_SUMMARY.md** | Executive summary with key stats | Quick reference, team briefings |
| **1secure_integration.json** | Programmatic mapping data | Direct import into Replit app |
| **1secure_mapping_report.md** | Detailed mapping analysis | Gap analysis, validation |
| **1secure_risks.csv** | Original 52 1Secure risks | Data reference |
| **map_1secure_to_drive.py** | Mapping generation script | Regenerate when catalog changes |

All files located in:
- `/docs/` - Documentation and PRD
- `/analysis/` - Data files and reports
- `/tools/` - Python scripts

---

## Quick Start: Replit Prototype

### Step 1: Review the PRD (15 min)

```bash
open docs/1SECURE_INTEGRATION_PRD.md
```

**Focus on:**
- Section 2: 1Secure Risk Catalog (tables with all 52 risks)
- Section 4: Replit Prototype Specifications (architecture, APIs, UI)
- Section 9.3: Scoring Algorithm Pseudocode

### Step 2: Set Up Replit Project (30 min)

**Create new Replit:**
- Template: Node.js + React
- Name: `drive-maturity-assessment`

**Initialize:**
```bash
# Backend (Node.js + Express)
npm init -y
npm install express axios js-yaml node-cache cors dotenv

# Frontend (React + TypeScript)
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install @tanstack/react-query recharts tailwindcss
```

**Environment variables:**
```bash
# .env
ONESECURE_API_URL=https://1secure-qc.nwxcorp.com
ONESECURE_API_KEY=<your-key-here>
ONESECURE_ORGANIZATION_ID=<gobias-industries-id>
DRIVE_CATALOG_PATH=./checks
```

### Step 3: Load DRIVE Catalog (15 min)

**Copy YAML checks to Replit:**
```bash
# In your Replit project
mkdir checks
# Upload all .yaml files from this repo's /checks/ directory
```

**Test loading:**
```javascript
// server.js
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');

function loadDriveCatalog() {
  const checksDir = './checks';
  const checks = [];

  fs.readdirSync(checksDir)
    .filter(f => f.endsWith('.yaml'))
    .forEach(file => {
      const content = fs.readFileSync(path.join(checksDir, file), 'utf8');
      const check = yaml.load(content);
      checks.push(check);
    });

  console.log(`Loaded ${checks.length} DRIVE checks`);
  return checks;
}
```

### Step 4: Integrate 1Secure API (30 min)

**Test API connection:**
```javascript
// services/onesecure-client.js
const axios = require('axios');

class OneSecureClient {
  constructor() {
    this.baseUrl = process.env.ONESECURE_API_URL;
    this.apiKey = process.env.ONESECURE_API_KEY;
  }

  async getOrganizationRisks(orgId) {
    try {
      const response = await axios.get(
        `${this.baseUrl}/api/organizations/${orgId}/risks`,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );
      return response.data;
    } catch (error) {
      console.error('1Secure API Error:', error.message);
      throw error;
    }
  }
}

module.exports = OneSecureClient;
```

**Test with Gobias Industries:**
```bash
node -e "
const OneSecure = require('./services/onesecure-client');
const client = new OneSecure();
client.getOrganizationRisks(process.env.ONESECURE_ORGANIZATION_ID)
  .then(data => console.log(JSON.stringify(data, null, 2)))
  .catch(err => console.error(err));
"
```

### Step 5: Implement Scoring Engine (45 min)

**Use the integration JSON:**
```javascript
// services/drive-scoring.js
const mappings = require('../analysis/1secure_integration.json');

function calculateMaturityScore(oneSecureRisks, driveCatalog) {
  const checkResults = [];

  // Map 1Secure risks to DRIVE checks
  mappings.mappings.forEach(mapping => {
    const risk = oneSecureRisks.find(r => r.metric === mapping['1secure_metric']);

    if (risk) {
      mapping.drive_checks.forEach(driveCheck => {
        const result = evaluateCheck(driveCheck, risk);
        checkResults.push(result);
      });
    }
  });

  // Calculate level advancement (binary model)
  const dataChecks = checkResults.filter(c => ['D','R','V'].includes(c.pillar));
  const identityChecks = checkResults.filter(c => ['I','R','E'].includes(c.pillar));

  const dataLevel = calculateDomainLevel(dataChecks);
  const identityLevel = calculateDomainLevel(identityChecks);

  return {
    overallLevel: Math.min(dataLevel, identityLevel),
    dataLevel,
    identityLevel,
    checkResults
  };
}

function calculateDomainLevel(checks) {
  // Binary advancement: must pass ALL checks at level
  for (let level = 1; level <= 5; level++) {
    const levelChecks = checks.filter(c => c.minLevel === level);
    const failed = levelChecks.filter(c => c.status === 'fail');

    if (failed.length > 0) {
      return level - 1; // Blocked at this level
    }
  }

  return 5; // Passed all levels
}

module.exports = { calculateMaturityScore };
```

### Step 6: Create Simple UI (60 min)

**Landing page component:**
```typescript
// frontend/src/components/MaturityDashboard.tsx
import { useQuery } from '@tanstack/react-query';

export function MaturityDashboard() {
  const { data: assessment } = useQuery({
    queryKey: ['maturity'],
    queryFn: () => fetch('/api/drive/assess').then(r => r.json())
  });

  if (!assessment) return <div>Loading...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">DRIVE Maturity Assessment</h1>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-blue-100 p-6 rounded">
          <h2 className="text-xl">Overall Maturity</h2>
          <div className="text-4xl font-bold">
            Level {assessment.overallLevel} / 5
          </div>
        </div>

        <div className="bg-green-100 p-6 rounded">
          <h2 className="text-xl">Data Security</h2>
          <div className="text-4xl font-bold">
            Level {assessment.dataLevel} / 5
          </div>
        </div>

        <div className="bg-yellow-100 p-6 rounded">
          <h2 className="text-xl">Identity Security</h2>
          <div className="text-4xl font-bold">
            Level {assessment.identityLevel} / 5
          </div>
        </div>
      </div>

      <div>
        <h2 className="text-2xl mb-4">Failed Checks Blocking Advancement</h2>
        <ul>
          {assessment.checkResults
            .filter(c => c.status === 'fail')
            .map(c => (
              <li key={c.checkId} className="mb-2">
                ❌ {c.checkId}: {c.title}
              </li>
            ))}
        </ul>
      </div>
    </div>
  );
}
```

---

## Key Concepts to Understand

### 1. Multi-Level Thresholds

Same 1Secure risk can block multiple DRIVE levels:

```
External Sharing of Sensitive Data:
  15%+ → Blocks Level 1 (Critical)
  5-15% → Blocks Level 2 (High)
  <5% → Blocks Level 3 (Medium)

Current value: 12%
  ✅ Level 1: PASS (12% < 15%)
  ❌ Level 2: FAIL (12% ≥ 5%) → Stuck at Level 1
```

### 2. Binary Advancement

Must pass **ALL** checks at a level to proceed:

```
Level 1: 10 checks total
  ✅ 8 passed
  ❌ 2 failed
  → Cannot advance to Level 2 until ALL 10 pass
```

### 3. Dual Domain Scoring

Two independent scores that both must advance:

```
Data Security:     Level 3 ✅
Identity Security: Level 1 ❌ (blocker)
Overall Maturity:  Level 1 (minimum of both)
```

---

## Testing Your Implementation

### Test 1: Load Catalog

```bash
curl http://localhost:3000/api/drive/checks | jq
# Should return 118 DRIVE checks
```

### Test 2: Fetch 1Secure Data

```bash
curl http://localhost:3000/api/1secure/organizations/<orgId>/scan | jq
# Should return 52 risk metrics
```

### Test 3: Run Assessment

```bash
curl -X POST http://localhost:3000/api/drive/assess/<orgId> | jq
# Should return maturity score with levels 0-5
```

### Test 4: Verify Multi-Level Logic

```javascript
// Check that same risk maps to multiple levels
const externalSharingRisk = {
  metric: "External and Anonymous Sharing of Sensitive Data",
  currentValue: 12  // 12% of files
};

// Should create check results for BOTH:
// - SP-ES-001 at Level 1 (threshold 15%) → PASS
// - SP-ES-002 at Level 2 (threshold 5%) → FAIL
```

---

## Common Issues & Solutions

### Issue: Can't connect to 1Secure API

**Solution:** Verify credentials and network access
```bash
curl -H "Authorization: Bearer <your-key>" \
  https://1secure-qc.nwxcorp.com/api/organizations
```

### Issue: YAML files not loading

**Solution:** Check file paths and permissions
```javascript
const fs = require('fs');
console.log(fs.readdirSync('./checks').filter(f => f.endsWith('.yaml')));
```

### Issue: Scoring logic wrong

**Solution:** Add debug logging
```javascript
function calculateDomainLevel(checks) {
  console.log(`Evaluating ${checks.length} checks`);

  for (let level = 1; level <= 5; level++) {
    const levelChecks = checks.filter(c => c.minLevel === level);
    const failed = levelChecks.filter(c => c.status === 'fail');

    console.log(`Level ${level}: ${failed.length}/${levelChecks.length} failed`);

    if (failed.length > 0) {
      console.log(`Blocked at level ${level}`);
      return level - 1;
    }
  }

  return 5;
}
```

---

## Next Steps After MVP

1. **Add PingCastle-style visualization** (see PRD Section 4.4.1)
2. **Implement framework mappings display** (NIST, CIS, ISO tabs)
3. **Create remediation guidance views** (see PRD Section 4.4.3)
4. **Build PDF export** (executive summary report)
5. **Add historical trending** (track maturity over time)
6. **Enhance with ANSSI styling** (blue/white government aesthetic)

---

## Resources

**Documentation:**
- Full PRD: `/docs/1SECURE_INTEGRATION_PRD.md`
- Summary: `/analysis/1SECURE_INTEGRATION_SUMMARY.md`
- Mapping Report: `/analysis/1secure_mapping_report.md`

**Data Files:**
- Integration JSON: `/analysis/1secure_integration.json` (import this!)
- Risk Catalog: `/analysis/1secure_risks.csv`
- DRIVE Checks: `/checks/*.yaml` (copy all to Replit)

**Code Examples:**
- Scoring algorithm: PRD Section 9.3 (pseudocode)
- API endpoints: PRD Section 4.3
- UI wireframes: PRD Section 4.4

---

## Support

**Questions?** Review:
1. PRD Section 10 (Open Questions)
2. PRD Section 7 (Risks and Mitigations)
3. This repo's CLAUDE.md for development workflow

**Ready to build?** Follow the 6 steps above and you'll have a working prototype in ~3 hours!

---

**Status:** Ready for Implementation
**Estimated MVP Time:** 2-3 hours for basic prototype, 8-10 weeks for full product
**Complexity:** Medium (well-defined requirements, clear data model)
**Primary Risk:** 1Secure API access (ensure credentials work before starting)
