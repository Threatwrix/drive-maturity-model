# 1Secure DRIVE Maturity Model - MVP PRD
## Minimal Viable Product for Team Review

**Version:** 1.0 MVP
**Date:** October 14, 2025
**Status:** Draft for Team Review
**Goal:** Add DRIVE maturity scoring to 1Secure with MINIMAL changes to existing architecture

---

## Executive Summary

### The Problem
1Secure currently shows risks as **Low/Medium/High** severity, but customers want to understand their **overall security maturity** and **track progress over time** toward industry-standard benchmarks.

### The Solution (MVP)
Add a **DRIVE Maturity Score** (Levels 1-5) by **reusing the existing Low/Medium/High thresholds** without changing the backend risk engine. Map severity thresholds to maturity levels in the UI layer only.

### Key Insight from Screenshot
The existing UI already has:
- ✅ Configurable thresholds per risk (Low: 0-5%, Medium: 5-15%, High: 15%+)
- ✅ Category grouping (Data, Identity, Infrastructure)
- ✅ Percentage and numeric measurement types
- ✅ Risk profile configuration

**We can leverage all of this WITHOUT backend changes!**

---

## Current State Analysis

### Existing 1Secure Architecture (From Screenshot)

```
┌─────────────────────────────────────────────────────────────┐
│  Current 1Secure Risk Model (52 risks)                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Each Risk Has:                                              │
│  - Name (e.g., "High Risk Permissions on Documents")        │
│  - Category (Data, Identity, Infrastructure)                │
│  - Measurement Type (Percentage or Numbers)                 │
│  - Three Thresholds:                                        │
│    • Low: <5%                                               │
│    • Medium: 5% to 15%                                      │
│    • High: 15% and above                                    │
│                                                              │
│  Risk Evaluation:                                            │
│  1. Scan runs and measures current value (e.g., 12%)       │
│  2. Compare to thresholds → Result: "Medium" severity       │
│  3. Show in UI with yellow/orange/red indicator             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### What We Keep (No Changes)
- ✅ Risk engine scans (SharePoint State, Entra ID Activity, etc.)
- ✅ 52 risk definitions with Low/Medium/High thresholds
- ✅ Risk configuration UI (shown in screenshot)
- ✅ Threshold evaluation logic (compare current value to L/M/H)
- ✅ Category grouping (Data, Identity, Infrastructure)

### What We Add (UI Layer Only)
- 🆕 Maturity level mapping (L/M/H → Levels 1-5)
- 🆕 Overall DRIVE score calculation (aggregation logic)
- 🆕 Maturity dashboard view (new page/tab)
- 🆕 Level progression visualization (control graph)

---

## MVP Design: Severity-to-Maturity Mapping

### Core Concept

**Map existing severity thresholds to maturity levels using simple rules:**

| Risk Severity | Maps To | Maturity Interpretation |
|---------------|---------|-------------------------|
| **High** | Blocks **Level 1 or 2** | Critical/High risk must be fixed first |
| **Medium** | Blocks **Level 2 or 3** | Must fix to reach standard baseline |
| **Low** | Allows **Level 3+** | Good hygiene, enables advanced levels |
| **Passing** (below Low) | Enables **Level 4-5** | State-of-the-art security |

### Mapping Strategy (Minimal Configuration)

We add ONE new field to each risk: **`maturity_level_blocked`**

```yaml
Risk: High Risk Permissions on Documents
Current Thresholds:
  Low: Below 5%
  Medium: 5% to 15%
  High: 15% and above

NEW Field (added to risk profile):
  maturity_level_blocked:
    High: 1        # If High severity → blocks Level 1 advancement
    Medium: 2      # If Medium severity → blocks Level 2 advancement
    Low: 3         # If Low severity → blocks Level 3 advancement
    # Passing (below Low) → Level 4+ achievable
```

### Example: How It Works

**Scenario 1: Organization has 18% high-risk permissions**
- Current 1Secure: Shows "High" severity (red) ✅ No change
- NEW Maturity Score:
  - Risk severity = High
  - High maps to maturity_level_blocked = 1
  - **Result: Organization is BLOCKED at Level 0** (cannot achieve Level 1)
  - Message: "Fix 7 High severity risks to achieve Level 1"

**Scenario 2: Organization reduces to 10% high-risk permissions**
- Current 1Secure: Shows "Medium" severity (yellow) ✅ No change
- NEW Maturity Score:
  - Risk severity = Medium
  - Medium maps to maturity_level_blocked = 2
  - **Result: Organization achieves Level 1, BLOCKED at Level 2**
  - Message: "Fix 15 Medium severity risks to achieve Level 2"

**Scenario 3: Organization reduces to 3% high-risk permissions**
- Current 1Secure: Shows "Low" severity (green) ✅ No change
- NEW Maturity Score:
  - Risk severity = Low
  - Low maps to maturity_level_blocked = 3
  - **Result: Organization achieves Levels 1-2, BLOCKED at Level 3**
  - Message: "Fix 8 Low severity risks to achieve Level 3"

---

## MVP Architecture (No Backend Changes!)

### Current Flow (Unchanged)
```
1. Connectors scan → Collect metrics
2. Risk engine evaluates → Compare to L/M/H thresholds
3. Store results → Database (severity per risk)
4. UI displays → Risk list with severity indicators
```

### NEW Flow (UI Layer Addition)
```
5. Maturity calculator reads → Risk results from database
6. Apply mapping logic → L/M/H → Blocked levels
7. Aggregate by category → Data vs Identity scores
8. Calculate overall → MIN(Data level, Identity level)
9. Display maturity dashboard → NEW UI page
```

### Where Code Changes Happen

**NO CHANGES NEEDED:**
- ❌ Risk engine scanning logic
- ❌ Threshold evaluation logic
- ❌ Database schema (current severity storage is sufficient)
- ❌ Risk configuration backend
- ❌ API endpoints for risk data

**MINIMAL CHANGES NEEDED:**
- 🟢 Add `maturity_level_blocked` field to risk profile configuration (UI config only)
- 🟢 New UI component: Maturity Dashboard (read-only view)
- 🟢 New calculation service: Maturity score aggregator (reads existing risk results)
- 🟢 New visualization: Control graph (PingCastle-style)

---

## MVP Feature Specification

### Feature 1: Risk Profile Enhancement (Minimal Config Change)

**Add one new field to the existing Risk Profile configuration UI:**

```
Current UI (from screenshot):
┌────────────────────────────────────────────────────┐
│ High Risk Permissions on Documents                  │
│ Category: Data                                      │
│ Measure in: ⦿ Percentage (%) ○ Numbers            │
│                                                     │
│ 🟢 Low:    [0] — [5.00]                           │
│ 🟡 Medium: [5.00] — [15.00]                       │
│ 🔴 High:   [15.00] and above                      │
└────────────────────────────────────────────────────┘

NEW UI (add collapsible section):
┌────────────────────────────────────────────────────┐
│ ▼ DRIVE Maturity Mapping (optional)                │
│                                                     │
│ When this risk is High severity, it blocks:        │
│ [Level 1 ▼] (Critical Exposure)                    │
│                                                     │
│ When this risk is Medium severity, it blocks:      │
│ [Level 2 ▼] (High Risk)                            │
│                                                     │
│ When this risk is Low severity, it blocks:         │
│ [Level 3 ▼] (Baseline Security)                    │
│                                                     │
│ ℹ️ Defaults: High→L1, Medium→L2, Low→L3            │
└────────────────────────────────────────────────────┘
```

**Defaults (Pre-Configured):**
- Most Data risks: High→L1, Medium→L2, Low→L3
- Most Identity risks: High→L1, Medium→L2, Low→L3
- Infrastructure risks: High→L2, Medium→L3, Low→L4
- Admins can override per risk

### Feature 2: Maturity Dashboard (New Page)

**New navigation item: "DRIVE Maturity" under Risk Profiles section**

#### Landing View (Top of Page)

```
┌─────────────────────────────────────────────────────────────┐
│  DRIVE Maturity Assessment - Gobias Industries               │
│  Last Scan: Oct 14, 2025 12:34 UTC   [Refresh Score]        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Overall Maturity: Level 1 / 5                              │
│  ████████░░░░░░░░░░░░░░░░░░░░  20%                         │
│                                                              │
│  Data Security:     Level 2 / 5  ████████████░░░░░  40%    │
│  Identity Security: Level 1 / 5  ████████░░░░░░░░  20% ⚠️  │
│                                                              │
│  ⚠️ Blocked by: 8 High severity risks in Identity category  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Control Graph (Middle of Page - PingCastle Style)

```
┌─────────────────────────────────────────────────────────────┐
│  Maturity Level Progress                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│    [1]──────[2]──────[3]──────[4]──────[5]                 │
│     ✅      ❌       ⏭️       ⏭️       ⏭️                    │
│  Critical   High   Baseline Enhanced State-of-             │
│  Exposure   Risk              Security  the-Art             │
│                                                              │
│  Click level for detailed breakdown →                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Blocking Risks (Bottom of Page)

```
┌─────────────────────────────────────────────────────────────┐
│  Risks Blocking Level 2 Advancement (8 risks)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔴 User Accounts with "Password Never Expires"             │
│     Current: 8 accounts | Threshold: 0 (High)               │
│     Category: Identity | [View Details] [Remediate]         │
│                                                              │
│  🔴 User Accounts with "No MFA Configured"                  │
│     Current: 12 accounts | Threshold: 0 (High)              │
│     Category: Identity | [View Details] [Remediate]         │
│                                                              │
│  🔴 High Risk Permissions on Documents                       │
│     Current: 18% | Threshold: <15% (High)                   │
│     Category: Data | [View Details] [Remediate]             │
│                                                              │
│  ... 5 more risks                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Feature 3: Level Detail View (Drill-Down)

**Click on Level 2 in control graph → Modal/Slide-out:**

```
┌─────────────────────────────────────────────────────────────┐
│  Level 2: High Risk Mitigated                               │
│  ████████████░░░░░░░  34 of 42 checks passed (81%)         │
│                                                              │
│  Requirements to advance to Level 3:                         │
│  - Pass ALL 42 checks at this level                         │
│  - Currently blocked by 8 High severity risks               │
│                                                              │
│  ❌ Blocking Risks (8):                                      │
│     [List of 8 High severity risks preventing Level 2]      │
│                                                              │
│  ✅ Passed Checks (34):                                      │
│     [Collapsible list of passing checks]                    │
│                                                              │
│  [Generate Remediation Plan] [Export to CSV]                │
└─────────────────────────────────────────────────────────────┘
```

---

## MVP Scoring Algorithm (Simple)

### Binary Advancement Logic

```python
def calculate_maturity_level(risk_results, domain='overall'):
    """
    Calculate maturity level using binary advancement.
    Must pass ALL risks at each level to advance.

    risk_results: List of {risk_id, category, severity, maturity_level_blocked}
    domain: 'data', 'identity', or 'overall'
    """

    # Filter by domain
    if domain == 'data':
        risks = [r for r in risk_results if r['category'] == 'Data']
    elif domain == 'identity':
        risks = [r for r in risk_results if r['category'] in ['Identity', 'Infrastructure']]
    else:
        # Overall = calculate both and take minimum
        data_level = calculate_maturity_level(risk_results, 'data')
        identity_level = calculate_maturity_level(risk_results, 'identity')
        return min(data_level, identity_level)

    # Binary advancement: check each level
    for level in range(1, 6):  # Levels 1-5
        blocking_risks = []

        for risk in risks:
            # Get the level this risk blocks based on current severity
            severity = risk['severity']  # 'High', 'Medium', 'Low', or 'Passing'

            if severity == 'High' and risk['maturity_level_blocked']['High'] == level:
                blocking_risks.append(risk)
            elif severity == 'Medium' and risk['maturity_level_blocked']['Medium'] == level:
                blocking_risks.append(risk)
            elif severity == 'Low' and risk['maturity_level_blocked']['Low'] == level:
                blocking_risks.append(risk)

        # If any risks block this level, we're stuck here
        if len(blocking_risks) > 0:
            return level - 1  # Blocked at this level, so we're at previous level

    # Passed all levels!
    return 5
```

### Default Mapping (Pre-Configured for MVP)

```json
{
  "default_mappings": {
    "data_critical": {
      "High": 1,
      "Medium": 2,
      "Low": 3
    },
    "identity_critical": {
      "High": 1,
      "Medium": 2,
      "Low": 3
    },
    "infrastructure_baseline": {
      "High": 2,
      "Medium": 3,
      "Low": 4
    }
  },

  "risk_assignments": {
    "High Risk Permissions on Documents": "data_critical",
    "External and Anonymous Sharing of Sensitive Data": "data_critical",
    "User Accounts with Password Never Expires": "identity_critical",
    "Disabled Computer Accounts": "infrastructure_baseline"
  }
}
```

**Pre-configure all 52 risks with sensible defaults based on YAML catalog we created.**

---

## MVP Implementation Plan

### Phase 1: Configuration (Week 1)
**Goal:** Add maturity mapping to risk profiles

- [ ] Add `maturity_level_blocked` field to Risk Profile data model (config only, not scans)
- [ ] Extend Risk Profile configuration UI with collapsible "DRIVE Maturity Mapping" section
- [ ] Pre-configure all 52 risks with default mappings (import from YAML catalog)
- [ ] Add validation: ensure level 1-5, defaults to High→1, Medium→2, Low→3

**Deliverable:** Admins can view/edit maturity mappings per risk

### Phase 2: Calculation Service (Week 2)
**Goal:** Calculate maturity scores from existing risk results

- [ ] Create `MaturityCalculatorService` that reads risk results from database
- [ ] Implement binary advancement algorithm (Python/TypeScript)
- [ ] Calculate Data domain score (category='Data' risks)
- [ ] Calculate Identity domain score (category='Identity'+'Infrastructure' risks)
- [ ] Calculate overall score (minimum of both domains)
- [ ] Identify blocking risks per level

**Deliverable:** Backend API endpoint `/api/maturity/score/{orgId}` returns scores

### Phase 3: Dashboard UI (Week 3-4)
**Goal:** Display maturity scores in new UI page

- [ ] Add "DRIVE Maturity" navigation item under Risk Profiles
- [ ] Build landing view: overall score, data/identity breakdown
- [ ] Build control graph component (PingCastle-style visualization)
- [ ] Build blocking risks list with drill-down
- [ ] Build level detail modal
- [ ] Add "Refresh Score" button (recalculates from latest scan)

**Deliverable:** Full maturity dashboard accessible in 1Secure UI

### Phase 4: Testing & Refinement (Week 5)
**Goal:** Validate with real customer data

- [ ] Test with Gobias Industries organization
- [ ] Verify scoring logic with edge cases
- [ ] Validate threshold mappings make sense
- [ ] Collect user feedback
- [ ] Adjust default mappings if needed
- [ ] Write user documentation

**Deliverable:** MVP ready for beta customers

---

## What We're NOT Building (MVP Scope Cuts)

### Out of Scope for MVP

- ❌ Framework mappings (NIST, CIS, ISO) - Just show maturity levels
- ❌ Remediation automation - Just link to existing risk details
- ❌ Historical trending - Just current score (add later)
- ❌ PDF export - Use existing reporting (add later)
- ❌ Multi-level thresholds - Just use L/M/H (already have this!)
- ❌ Custom maturity models - Just DRIVE (add later)
- ❌ API changes - Just read existing data
- ❌ Scan changes - Use existing risk results

### Can Add Later (Post-MVP)

- Historical maturity tracking over time
- Peer benchmarking (compare to industry)
- Remediation roadmap generation
- Executive summary PDF
- Framework gap analysis
- Custom maturity models
- Advanced visualizations

---

## MVP Success Metrics

### Technical Success

- [ ] Zero backend scan changes (just read existing data)
- [ ] <5 new database fields (just config, not telemetry)
- [ ] Scores calculate in <2 seconds per organization
- [ ] UI loads in <3 seconds
- [ ] 100% of 52 risks have default mappings

### User Success

- [ ] Customers can see overall maturity score
- [ ] Customers understand what blocks advancement
- [ ] Customers can drill into level details
- [ ] Customers can track improvement (future: trending)
- [ ] >80% of users find dashboard intuitive (survey)

### Business Success

- [ ] Differentiate 1Secure from competitors
- [ ] Enable executive conversations (maturity score)
- [ ] Increase customer engagement with risk data
- [ ] Create upsell path (premium analytics in future)

---

## Key Benefits of This MVP Approach

### Why This Works

1. **Minimal Changes to Core Product**
   - No risk engine changes
   - No scan logic changes
   - No new connectors needed
   - Just UI layer addition

2. **Leverage Existing Architecture**
   - Reuse L/M/H thresholds (already configured!)
   - Reuse risk results (already in database!)
   - Reuse category groupings (Data/Identity/Infrastructure)
   - Reuse UI components (risk lists, details)

3. **Low Risk, High Value**
   - If it doesn't work, just hide the UI page
   - No impact on existing features
   - Easy to iterate based on feedback
   - Can add advanced features later

4. **Fast to Market**
   - 5 weeks to MVP
   - Use existing YAML catalog for defaults
   - Most work is UI (no backend complexity)
   - Can beta test quickly

5. **Aligns with Existing Workflow**
   - Admins already configure L/M/H thresholds
   - Just add one more field (maturity mapping)
   - Customers already review risk lists
   - Just add aggregated view

---

## Open Questions for Team Discussion

### Configuration Questions

1. **Default Mappings:** Should we pre-configure all 52 risks or let admins do it?
   - **Recommendation:** Pre-configure with sensible defaults (import from YAML)
   - Allow overrides per customer

2. **Severity Passing State:** How do we handle risks below "Low" threshold?
   - **Recommendation:** Below Low = "Passing" = enables Level 4+

3. **Binary vs Weighted:** Should all risks at a level carry equal weight?
   - **Recommendation:** MVP = binary (all equal), add weighting later

### UI/UX Questions

4. **Navigation:** Where does DRIVE Maturity appear?
   - **Recommendation:** Under Risk Profiles section (shown in screenshot)
   - Alternative: New top-level nav item

5. **Terminology:** Do we say "DRIVE Maturity" or just "Security Maturity"?
   - **Recommendation:** "Security Maturity Score (DRIVE Model)"

6. **Branding:** How much ANSSI/PingCastle visual style to adopt?
   - **Recommendation:** Control graph yes, but keep 1Secure styling

### Technical Questions

7. **Calculation Frequency:** Recalculate on every scan or on-demand?
   - **Recommendation:** On-demand (button click), cache for 1 hour

8. **Database Storage:** Store calculated scores or compute on-the-fly?
   - **Recommendation:** Compute on-the-fly for MVP, optimize later

9. **Multi-Org:** Same scoring logic for all customers?
   - **Recommendation:** Yes for MVP, custom models later

---

## MVP Deliverables Summary

### Code Changes

**Backend (Minimal):**
- New service: `MaturityCalculatorService` (~200 lines)
- New API endpoint: `GET /api/maturity/score/{orgId}` (~50 lines)
- Config schema update: Add `maturity_level_blocked` field (~10 lines)

**Frontend (New Page):**
- New page: Maturity Dashboard (~500 lines React/TypeScript)
- New component: Control Graph (~200 lines)
- New component: Level Detail Modal (~150 lines)
- Config UI update: Add maturity mapping section (~100 lines)

**Total Estimated LOC:** ~1,200 lines (very manageable!)

### Configuration Files

- Default maturity mappings JSON (import from existing YAML catalog)
- Level definitions (already have in `/levels/levels.yaml`)
- UI copy/text for maturity descriptions

### Documentation

- User Guide: "Understanding Your DRIVE Maturity Score"
- Admin Guide: "Configuring Maturity Mappings"
- API Documentation: Maturity score endpoint
- Release Notes: "Introducing DRIVE Maturity Assessment"

---

## Next Steps

### Immediate (This Week)

1. **Team Review:** Present this PRD to product, engineering, and design
2. **Feedback:** Gather input on MVP scope and approach
3. **Prioritization:** Confirm this fits roadmap and timeline
4. **Resource Planning:** Assign eng resources (1 backend, 1 frontend?)

### Short Term (Next 2 Weeks)

5. **Design Mockups:** Create high-fidelity UI designs for dashboard
6. **Technical Spec:** Detailed implementation plan for engineers
7. **Default Mappings:** Finalize the 52 risk → level mappings
8. **Kickoff:** Start Phase 1 (Configuration UI)

### Medium Term (5 Weeks)

9. **MVP Development:** Execute 4-phase plan
10. **Beta Testing:** Test with 2-3 friendly customers
11. **Iteration:** Refine based on feedback
12. **Launch:** General availability release

---

## Appendix: Comparison to Existing UI

### Current UI (From Screenshot)

**Strengths to Keep:**
- ✅ Clean risk list with category grouping
- ✅ Clear severity indicators (green/yellow/red)
- ✅ Configurable thresholds per risk
- ✅ Intuitive measurement types (%, numbers)
- ✅ Simple navigation (sidebar)

**What We Add:**
- 🆕 Aggregated view (overall score)
- 🆕 Progress tracking (level advancement)
- 🆕 Visual control graph
- 🆕 Prioritization (what blocks next level)

**What Stays Unchanged:**
- Risk list view (existing page)
- Risk configuration (just adds one field)
- Risk detail modals (existing)
- Reporting (existing)

---

**Status:** Ready for Team Review
**Estimated Effort:** 5 weeks (1 person-month)
**Risk Level:** Low (no core product changes)
**Value:** High (unique differentiator, executive-friendly)
