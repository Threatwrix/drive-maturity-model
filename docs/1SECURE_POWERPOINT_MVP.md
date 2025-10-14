# 1Secure PowerPoint Report Enhancement - MVP
## Adding DRIVE Maturity to Risk Assessment Report

**Version:** 1.0 MVP
**Date:** October 14, 2025
**Goal:** Add DRIVE maturity slides to existing PowerPoint export with minimal changes

---

## Current PowerPoint Structure (Analyzed)

**Existing Report:** "Risk Assessment Report for Gobias Industries 2025-10-14.pptx"

### Current Slide Structure (25 slides)

```
Slide 1:  Title slide
          - "Cybersecurity Risk Assessment Report"
          - Organization name, date, reported by

Slides 2-17: Individual Risk Details (one risk per slide)
          - Risk name
          - Current score (e.g., "34 / 39 users (87.18%)")
          - Severity level (Low/Medium/High or Not detected)
          - Threshold values
          - Related regulations
          - Trend indicator
          - Reporting period

Slides 18-21: Summary Tables
          - "Monitored Risk Metrics" by category
          - Previous vs Current score comparison
          - Risk severity column
          - Trend arrows
          - Grouped by: Infrastructure, Identity, Data
```

### Observations

✅ **Strengths:**
- Clean, professional design
- One risk per slide (detailed view)
- Includes regulatory mappings
- Trend indicators (change over time)
- Summary tables by category

⚠️ **Gaps:**
- No executive summary
- No overall risk score/rating
- No prioritization guidance
- No maturity progression view
- Very detailed (25 slides = too long for executives)

---

## MVP Enhancement: Add DRIVE Maturity Slides

### Strategy: INSERT 4 new slides at the beginning

**Keep all existing slides (2-25), just add executive summary up front.**

---

## NEW Slide 2: Executive Summary - DRIVE Maturity Score

**Position:** After title slide, before individual risk details

**Layout:** Large score display with visual indicator

```
┌────────────────────────────────────────────────────────────┐
│  Security Maturity Assessment - DRIVE Model                │
├────────────────────────────────────────────────────────────┤
│                                                             │
│         Overall Maturity: Level 1 / 5                      │
│         ████████░░░░░░░░░░░░░░░░░░░░  20%                 │
│                                                             │
│    ┌──────────────────┐    ┌──────────────────┐          │
│    │ Data Security    │    │ Identity Security│          │
│    │   Level 2 / 5    │    │   Level 1 / 5    │          │
│    │   ████████████   │    │   ████████       │          │
│    │      40%         │    │      20%  ⚠️     │          │
│    └──────────────────┘    └──────────────────┘          │
│                                                             │
│  Key Findings:                                             │
│  • 7 High severity risks blocking Level 2 advancement     │
│  • Identity security is the primary concern (20%)          │
│  • Data security performing better (40%)                   │
│                                                             │
│  Reporting Period: September 15 - October 15, 2025        │
└────────────────────────────────────────────────────────────┘
```

**Data Elements:**
- Overall maturity level (1-5)
- Overall percentage (based on level)
- Data Security level + percentage
- Identity Security level + percentage
- Bullet points with key findings
- Visual: Progress bars or gauge chart
- Color coding: Red (L0-1), Yellow (L2-3), Green (L4-5)

---

## NEW Slide 3: Maturity Level Progression

**Position:** After executive summary

**Layout:** PingCastle-style control graph with level descriptions

```
┌────────────────────────────────────────────────────────────┐
│  DRIVE Maturity Level Progress                             │
├────────────────────────────────────────────────────────────┤
│                                                             │
│    Level 1  →  Level 2  →  Level 3  →  Level 4  →  Level 5│
│      ✅         ❌          ⏭️          ⏭️          ⏭️       │
│   Critical    High Risk  Baseline   Enhanced   State-of-  │
│   Exposure    Mitigated  Security   Security   the-Art    │
│   ACHIEVED    BLOCKED    NOT YET    NOT YET    NOT YET     │
│                                                             │
│  Level Definitions:                                        │
│                                                             │
│  ✅ Level 1: Critical Exposure Mitigated                   │
│     All immediate threats addressed (15 checks passed)     │
│                                                             │
│  ❌ Level 2: High Risk Mitigated [CURRENT GOAL]           │
│     Short-term protection controls (37 checks required)    │
│     → BLOCKED by 7 High severity risks                     │
│                                                             │
│  Level 3: Standard Security Baseline                       │
│     Industry-standard controls (26 checks required)        │
│                                                             │
│  Level 4: Enhanced Security Posture                        │
│     Proactive security management (3 checks required)      │
│                                                             │
│  Level 5: State-of-the-Art Security                       │
│     Continuous excellence (9 checks required)              │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Data Elements:**
- Visual control graph (5 levels)
- Current level indicator (checkmark)
- Blocked level indicator (X)
- Level descriptions
- Check counts per level
- Blocking risk count

---

## NEW Slide 4: Priority Risks Blocking Advancement

**Position:** After maturity progression

**Layout:** Table of High severity risks preventing next level

```
┌────────────────────────────────────────────────────────────┐
│  Top Priority Risks - Blocking Level 2 Advancement         │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  You must address these 7 High severity risks to advance   │
│  from Level 1 to Level 2:                                  │
│                                                             │
│  Risk Name                          Current     Target     │
│  ────────────────────────────────────────────────────────  │
│  1. User Accounts with No MFA       34/39       0 accounts │
│     Configured                      (87.18%)    (High)     │
│                                                             │
│  2. Dangerous Default Permissions   Detected    Not        │
│                                                 detected   │
│                                                             │
│  3. Global Administrators           11/39       ≤4 admins  │
│                                     (28.21%)    (High)     │
│                                                             │
│  4. Third-Party Applications        Detected    Not        │
│     Allowed                                     detected   │
│                                                             │
│  5. MS Graph PowerShell Service     Detected    Not        │
│     Principal Not Enforced                      detected   │
│                                                             │
│  6. [Additional High risk]          ...         ...        │
│                                                             │
│  7. [Additional High risk]          ...         ...        │
│                                                             │
│  💡 Recommended Action: Address MFA gaps first (87% risk)  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Data Elements:**
- List of risks blocking current level
- Current values (from scan results)
- Target values (from threshold config)
- Severity indicator
- Prioritization recommendation
- Focus on HIGH severity risks only

---

## NEW Slide 5: Maturity Improvement Roadmap

**Position:** After priority risks

**Layout:** Timeline/phases for achieving next 2-3 levels

```
┌────────────────────────────────────────────────────────────┐
│  Maturity Improvement Roadmap                               │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Current State: Level 1 (Critical Exposure Mitigated)      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Phase 1: Achieve Level 2 (Estimated: 30-60 days)   │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │ • Fix 7 High severity risks                         │  │
│  │ • Priority: Enable MFA for 34 accounts              │  │
│  │ • Remove dangerous default permissions               │  │
│  │ • Reduce Global Admins to ≤4                        │  │
│  │ • Remove unauthorized third-party apps               │  │
│  │                                                      │  │
│  │ Estimated Effort: 40-80 hours                       │  │
│  │ Business Impact: High - Addresses immediate threats  │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Phase 2: Achieve Level 3 (Estimated: 60-90 days)   │  │
│  ├─────────────────────────────────────────────────────┤  │
│  │ • Fix 15 Medium severity risks                       │  │
│  │ • Address stale permissions and inactive accounts    │  │
│  │ • Implement baseline security hygiene                │  │
│  │                                                      │  │
│  │ Estimated Effort: 60-100 hours                      │  │
│  │ Business Impact: Medium - Establishes baseline      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  ⏭️ Phase 3: Achieve Level 4-5 (Future optimization)      │
│     • Requires achieving Levels 1-3 first                  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

**Data Elements:**
- Phased roadmap (2-3 phases)
- Risk counts per phase
- Estimated timeline
- Estimated effort (hours)
- Business impact rating
- Key action items per phase

---

## Slide Numbering Update

**NEW Structure (29 slides total):**

```
Slide 1:    Title slide (UNCHANGED)
Slide 2:    🆕 Executive Summary - DRIVE Maturity Score
Slide 3:    🆕 Maturity Level Progression
Slide 4:    🆕 Priority Risks Blocking Advancement
Slide 5:    🆕 Maturity Improvement Roadmap
Slides 6-21:  Individual Risk Details (RENUMBERED, content unchanged)
Slides 22-29: Summary Tables (RENUMBERED, content unchanged)
```

**Old slides 2-25 become new slides 6-29 (just renumbered, no content changes)**

---

## Implementation Approach

### Option 1: Template-Based (Recommended for MVP)

**Use PowerPoint template with placeholders:**

```python
from pptx import Presentation

# Load existing report template
prs = Presentation('risk_report_template.pptx')

# NEW: Insert maturity slides at position 1 (after title)
maturity_data = get_maturity_score(org_id)

# Slide 2: Executive Summary
slide = prs.slides.add_slide(prs.slide_layouts[MATURITY_SUMMARY_LAYOUT])
slide.shapes['OverallLevel'].text = f"Level {maturity_data['overall_level']} / 5"
slide.shapes['DataLevel'].text = f"Level {maturity_data['data_level']} / 5"
slide.shapes['IdentityLevel'].text = f"Level {maturity_data['identity_level']} / 5"
slide.shapes['KeyFindings'].text = maturity_data['key_findings']

# Slide 3: Maturity Progression
slide = prs.slides.add_slide(prs.slide_layouts[MATURITY_GRAPH_LAYOUT])
# ... populate control graph

# Slide 4: Priority Risks
slide = prs.slides.add_slide(prs.slide_layouts[PRIORITY_RISKS_LAYOUT])
# ... populate blocking risks table

# Slide 5: Roadmap
slide = prs.slides.add_slide(prs.slide_layouts[ROADMAP_LAYOUT])
# ... populate roadmap phases

# EXISTING: Continue with individual risk slides (unchanged logic)
for risk in risks:
    slide = prs.slides.add_slide(prs.slide_layouts[RISK_DETAIL_LAYOUT])
    # ... existing risk population code

prs.save(f'risk_report_{org_name}_{date}.pptx')
```

### Option 2: Dynamic Generation (Future Enhancement)

- Generate charts/graphs dynamically (using matplotlib or plotly)
- Export as images, insert into slides
- More flexible but requires more code

---

## Data Requirements

### Data Already Available (from existing report)

✅ Risk scan results (current values, previous values)
✅ Severity levels (Low/Medium/High)
✅ Thresholds (configured per risk)
✅ Trend indicators
✅ Reporting period
✅ Organization name

### NEW Data Needed (from maturity calculator)

🆕 Overall maturity level (1-5)
🆕 Data Security level (1-5)
🆕 Identity Security level (1-5)
🆕 Blocking risks list (filtered by severity)
🆕 Check counts per level
🆕 Roadmap phases with estimates

**Source:** Maturity Calculator Service (from MVP PRD)

### API Call Example

```javascript
// Get maturity data for PowerPoint generation
GET /api/maturity/score/{orgId}

Response:
{
  "overall_level": 1,
  "data_level": 2,
  "identity_level": 1,
  "blocking_risks": [
    {
      "risk_id": "1S-IDENTITY-013",
      "name": "User Accounts with No MFA Configured",
      "current_value": "34 / 39 users (87.18%)",
      "target_value": "0 accounts",
      "severity": "High",
      "blocks_level": 2
    },
    // ... 6 more
  ],
  "level_breakdown": {
    "1": {"total": 15, "passed": 15, "failed": 0},
    "2": {"total": 37, "passed": 30, "failed": 7},
    "3": {"total": 26, "passed": 0, "failed": 0}
  },
  "roadmap": {
    "phase1": {
      "target_level": 2,
      "risk_count": 7,
      "estimated_days": "30-60",
      "estimated_hours": "40-80",
      "priority_actions": ["Enable MFA", "Remove dangerous permissions"]
    },
    "phase2": {
      "target_level": 3,
      "risk_count": 15,
      "estimated_days": "60-90",
      "estimated_hours": "60-100"
    }
  },
  "key_findings": [
    "7 High severity risks blocking Level 2 advancement",
    "Identity security is the primary concern (20%)",
    "Data security performing better (40%)"
  ]
}
```

---

## Design Specifications

### Branding & Colors

**Use existing 1Secure/Netwrix branding:**
- Primary color: (from existing slides)
- Maturity level colors:
  - Level 0-1: 🔴 Red (Critical - #D32F2F)
  - Level 2-3: 🟡 Yellow/Orange (Medium - #FFA726)
  - Level 4-5: 🟢 Green (Good - #43A047)

### Fonts & Typography

**Match existing report style:**
- Headings: (existing font from title slides)
- Body text: (existing font from risk slides)
- Data/numbers: (existing font from metrics)

### Chart Style

**Control Graph (Slide 3):**
- Horizontal timeline with 5 nodes
- Checkmark icon for achieved levels
- X icon for blocked level
- Lock icon for future levels
- Progress line connecting nodes

**Progress Bars (Slide 2):**
- Horizontal bars (not circular gauges for MVP)
- Percentage labels
- Color-coded by level achieved

---

## Implementation Tasks

### Phase 1: Template Design (Week 1)
- [ ] Design 4 new slide layouts in PowerPoint
- [ ] Add placeholder shapes with names
- [ ] Match existing branding/colors
- [ ] Get design approval from team

### Phase 2: Code Integration (Week 2)
- [ ] Extend PowerPoint generation script
- [ ] Add maturity data API call
- [ ] Insert new slides at position 1
- [ ] Populate placeholders with maturity data
- [ ] Test with sample organization

### Phase 3: Data Mapping (Week 2)
- [ ] Map blocking risks to slide 4 table
- [ ] Calculate roadmap estimates (effort/timeline)
- [ ] Generate key findings bullets
- [ ] Format percentage displays

### Phase 4: Testing & Refinement (Week 3)
- [ ] Test with multiple organizations
- [ ] Verify slide numbering/order
- [ ] Check data accuracy
- [ ] User acceptance testing
- [ ] Documentation

---

## MVP Scope Decisions

### IN SCOPE (MVP)

✅ 4 new slides (executive summary focus)
✅ Static template layouts (placeholders)
✅ Text and simple charts (progress bars)
✅ Blocking risks table (High severity only)
✅ 2-phase roadmap (Levels 2-3)

### OUT OF SCOPE (Post-MVP)

❌ Dynamic chart generation (images)
❌ Trend over time (historical maturity)
❌ Framework-specific views (NIST, CIS, ISO)
❌ Detailed remediation steps per risk
❌ Custom branding per customer
❌ Interactive/clickable elements
❌ Comparison to peers/benchmarks

---

## User Experience Changes

### Before MVP (Current State)

**User workflow:**
1. Run risk scan in 1Secure
2. Generate PowerPoint report
3. Review 25 slides of individual risks
4. Manually identify priorities
5. Manually summarize for executives

**Pain points:**
- Too detailed for executives (25 slides)
- No overall risk score/rating
- No prioritization guidance
- Hard to track improvement over time

### After MVP (With Maturity Slides)

**User workflow:**
1. Run risk scan in 1Secure
2. Generate PowerPoint report (now 29 slides)
3. **NEW:** Review executive summary (slides 2-5)
   - See overall maturity level at a glance
   - Understand what blocks advancement
   - Get prioritized action list
   - View improvement roadmap
4. Review detailed risks (slides 6-29) - same as before

**Benefits:**
- Executive-friendly summary (4 slides)
- Clear prioritization (blocking risks)
- Maturity progression tracking
- Roadmap for improvement
- **Still have all the detail** for security teams (slides 6-29)

---

## Success Metrics

### Technical Success

- [ ] New slides generate in <5 seconds
- [ ] Data accuracy 100% (matches UI dashboard)
- [ ] PowerPoint opens without errors in PowerPoint/Keynote/Google Slides
- [ ] All placeholders populated correctly

### User Success

- [ ] Executives can understand maturity in <2 minutes (slides 2-5)
- [ ] Security teams can identify priorities (slide 4)
- [ ] Report is shareable with board/leadership
- [ ] Users prefer new report over old (survey)

### Business Success

- [ ] Increased report downloads (track metrics)
- [ ] Higher customer satisfaction with reporting
- [ ] Differentiation from competitors (unique feature)
- [ ] Enables executive-level conversations

---

## Example: Before & After Comparison

### BEFORE (Current Report)

```
25 slides:
- Slide 1: Title
- Slides 2-17: Individual risks (one per slide, very detailed)
- Slides 18-25: Summary tables

Executive reaction: "Too detailed, what's my overall risk?"
Security team: "Which risks should I fix first?"
```

### AFTER (MVP Enhanced Report)

```
29 slides:
- Slide 1: Title
- 🆕 Slide 2: Overall Maturity = Level 1/5 (20%) ← EXECUTIVE SUMMARY
- 🆕 Slide 3: Progress graph showing Level 2 blocked ← VISUAL
- 🆕 Slide 4: 7 High risks to fix (prioritized list) ← ACTIONABLE
- 🆕 Slide 5: 2-phase roadmap with timelines ← ROADMAP
- Slides 6-21: Individual risks (unchanged)
- Slides 22-29: Summary tables (unchanged)

Executive reaction: "We're at Level 1/5, need to get to Level 2. Clear priorities."
Security team: "Fix these 7 High risks first, here's the timeline."
```

---

## Open Questions

### Design Questions

1. **Slide position:** Insert at beginning (after title) or end (before summary)?
   - **Recommendation:** Beginning (executive summary first)

2. **Chart style:** Simple progress bars or more advanced visualizations?
   - **Recommendation:** Simple bars for MVP, enhance later

3. **Level descriptions:** Show all 5 or just current +1?
   - **Recommendation:** Show all 5 for context

### Content Questions

4. **Roadmap phases:** How many to show (2, 3, or all 5)?
   - **Recommendation:** 2 phases (next 2 levels only)

5. **Blocking risks:** Show all or limit to top 10?
   - **Recommendation:** Show all High severity, limit Medium to top 10

6. **Key findings:** Auto-generate or template-based?
   - **Recommendation:** Auto-generate 3-5 bullet points

### Technical Questions

7. **Chart generation:** Static template or dynamic image generation?
   - **Recommendation:** Static template for MVP

8. **Data refresh:** Recalculate maturity on report generation or use cached?
   - **Recommendation:** Recalculate (always fresh)

9. **Backwards compatibility:** Support old report format too?
   - **Recommendation:** Yes, add toggle in UI

---

## Appendix: PowerPoint Template Structure

### Slide Layouts Needed

```
Template: risk_report_template_v2.pptx

Layouts:
1. Title Slide (existing)
2. Maturity Summary (NEW)
   - Placeholders: OverallLevel, DataLevel, IdentityLevel, KeyFindings
3. Maturity Graph (NEW)
   - Placeholders: ControlGraph, LevelDescriptions
4. Priority Risks (NEW)
   - Placeholders: RisksTable (dynamic rows)
5. Roadmap (NEW)
   - Placeholders: Phase1, Phase2, Phase3 (optional)
6. Risk Detail (existing)
   - Placeholders: RiskName, CurrentScore, Severity, etc.
7. Summary Table (existing)
   - Placeholders: Table, Category, etc.
```

### Template File Location

```
/1secure/templates/powerpoint/
├── risk_report_template_v1.pptx  (current, for backwards compat)
├── risk_report_template_v2.pptx  (NEW with maturity slides)
└── master_slides/
    ├── maturity_summary.xml
    ├── maturity_graph.xml
    ├── priority_risks.xml
    └── roadmap.xml
```

---

## Next Steps

### Immediate (This Week)

1. **Review with team:** Present this enhancement to product/design/engineering
2. **Design mockups:** Create high-fidelity PowerPoint layouts
3. **Confirm scope:** Ensure 4 slides fit MVP timeline

### Short Term (2-3 Weeks)

4. **Create templates:** Design 4 new slide layouts
5. **Code integration:** Extend PowerPoint generator
6. **Testing:** Validate with sample organizations

### Launch (Week 4)

7. **Beta release:** Test with friendly customers
8. **Iterate:** Refine based on feedback
9. **GA release:** Make available to all customers

---

**Status:** Ready for Team Review
**Estimated Effort:** 3-4 weeks (design + dev + test)
**Dependencies:** Maturity Calculator Service (from MVP PRD)
**Risk Level:** Low (additive only, doesn't change existing slides)
**Value:** High (executive-friendly, actionable, differentiator)
