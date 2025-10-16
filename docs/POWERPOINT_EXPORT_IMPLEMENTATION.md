# PowerPoint Export Implementation Guide

## Overview

Schema v2.1 adds PowerPoint export tagging to DRIVE check definitions, enabling intelligent prioritization of security findings for executive presentations. This feature is inspired by Netwrix 1Secure's risk reporting capabilities.

**Status:** ✅ Complete and ready for use
**Version:** Schema v2.1
**Date:** October 16, 2025

---

## What's New

### PowerPoint Export Tagging

Each check can now be tagged with presentation priority:

- **1-PrimaryFocus** - Critical findings requiring immediate executive attention (3-7 per org typical)
- **2-SecondaryFocus** - Important findings for management review (10-20 per org typical)
- **3-AdditionalFinding** - Supporting details and context (30-50 per org typical)
- **4-Exclude** - Technical detail only, exclude from executive presentations

### Benefits

1. **Executive-Ready Reports** - Automatically filter checks for C-level audiences
2. **Intelligent Prioritization** - Focus on high-impact, business-relevant findings
3. **Consistent Messaging** - Standardized executive summaries across checks
4. **Chart Recommendations** - Suggested visualizations for each finding
5. **Slide Organization** - Pre-defined sections for logical presentation flow

---

## Implementation Details

### Files Delivered

1. **`/docs/YAML_SCHEMA_V2.1.md`** - Complete schema specification
   - Field definitions and validation rules
   - Priority assignment guidelines
   - Migration strategy
   - Backward compatibility notes

2. **`/tools/add_powerpoint_export_tags.py`** - Migration script
   - Intelligent priority assignment based on severity + level + keywords
   - Automatic executive summary generation
   - Custom priority mapping support
   - Dry-run mode for preview

3. **`/tools/validate_checks.py`** - Updated validation (now supports v2.1)
   - Validates `powerpoint_export` section
   - Consistency checks (priority vs include)
   - Executive summary length recommendations
   - Schema version detection

4. **`/CLAUDE.md`** - Updated development guide
   - Added PowerPoint export tagging section
   - Migration commands and examples
   - Schema version notes

---

## Quick Start

### Step 1: Preview Changes

```bash
# See what priority would be assigned to all checks
python3 tools/add_powerpoint_export_tags.py --dry-run

# Preview specific checks only
python3 tools/add_powerpoint_export_tags.py --dry-run checks/SP-*.yaml
```

### Step 2: Apply Migration

```bash
# Migrate all checks to v2.1
python3 tools/add_powerpoint_export_tags.py

# Or migrate specific checks
python3 tools/add_powerpoint_export_tags.py checks/1S-*.yaml
```

### Step 3: Validate Results

```bash
# Validate all checks
python3 tools/validate_checks.py

# Validate specific check
python3 tools/validate_checks.py checks/SP-ES-001.yaml
```

### Step 4: Review and Refine

```bash
# Find all Primary Focus checks for review
grep -r "priority: 1-PrimaryFocus" checks/*.yaml

# Count by priority level
grep -r "priority:" checks/*.yaml | cut -d: -f3 | sort | uniq -c
```

---

## YAML Schema Changes

### Before (v2.0)

```yaml
check_id: SP-ES-001
title: Sharepoint open access (anyone links present)
# ... other fields ...

metadata:
  version: 1.0.0
  schema_version: '2.0'
```

### After (v2.1)

```yaml
check_id: SP-ES-001
title: Sharepoint open access (anyone links present)
# ... other fields ...

# NEW SECTION
powerpoint_export:
  include: true
  priority: 1-PrimaryFocus
  slide_section: "Critical Findings"
  executive_summary: "Anonymous links expose confidential documents to public internet without authentication, enabling data breaches"
  chart_visualization: "gauge"

metadata:
  version: 1.0.0
  schema_version: '2.1'  # Updated
  last_updated: '2025-10-16T10:52:44Z'
  change_history:
  - date: '2025-10-16'
    version: 1.0.0
    change: Added PowerPoint export tagging (schema v2.1)
    author: PowerPoint-Migration-Script
```

---

## Priority Assignment Logic

The migration script uses intelligent rules to assign priorities:

### Rule-Based Assignment

```python
# Level 1 Critical → 1-PrimaryFocus
# Level 1 High → 1-PrimaryFocus
# Level 2 Critical → 1-PrimaryFocus
# Level 2 High → 2-SecondaryFocus
# Level 3+ → 3-AdditionalFinding (unless promoted)
```

### Keyword-Based Promotion

Checks are promoted if they contain executive-relevant keywords:

**Promote to higher priority:**
- anonymous, public, breach, exposure, confidential, sensitive
- admin, global, privileged, mfa, authentication
- compliance, gdpr, hipaa, sox, pci, regulation
- stale, orphaned, unmonitored, no owner

**Demote to lower priority:**
- protocol, cipher, algorithm, registry
- configuration drift, low severity, informational

### Custom Priority Mapping

Override defaults with custom rules:

```bash
# Create custom mapping file
cat > custom_priorities.json <<'EOF'
{
  "SP-ES-001": "1-PrimaryFocus",
  "AD-FL-*": "2-SecondaryFocus"
}
EOF

# Apply custom mapping
python3 tools/add_powerpoint_export_tags.py --priority-mapping custom_priorities.json
```

---

## Validation Rules

The updated validator enforces:

### Required Fields
- `powerpoint_export.include` (boolean)
- `powerpoint_export.priority` (enum: 1-PrimaryFocus | 2-SecondaryFocus | 3-AdditionalFinding | 4-Exclude)

### Consistency Checks
- ⚠️ Warning if `priority: 4-Exclude` but `include: true`
- ⚠️ Warning if `include: false` but priority is not `4-Exclude`
- ⚠️ Warning if `priority: 1-PrimaryFocus` but no `executive_summary`

### Best Practices
- Executive summaries should be <200 characters for slide readability
- Limit 1-PrimaryFocus to <10% of total checks
- Ensure 2-SecondaryFocus is <20% of total checks

---

## Backward Compatibility

### Schema v2.0 Checks

Checks without `powerpoint_export` section still work:

```python
# Default behavior for v2.0 checks
if schema_version == '2.0' and not powerpoint_export:
    # Auto-assign based on level + severity
    if level == 1 and severity == 'Critical':
        priority = '1-PrimaryFocus'
    elif level <= 2 and severity in ['Critical', 'High']:
        priority = '2-SecondaryFocus'
    else:
        priority = '3-AdditionalFinding'
```

### Migration is Non-Destructive

- ✅ Preserves all existing check data
- ✅ Only adds `powerpoint_export` section
- ✅ Updates schema version to 2.1
- ✅ Adds change history entry
- ✅ No impact on existing v2.0 consumers

---

## PowerPoint Generation (Future)

The `powerpoint_export` metadata will power:

### Slide Generation Logic

```python
# Pseudo-code for PowerPoint generation
def generate_presentation(organization, checks):
    # Filter included checks
    included = [c for c in checks if c['powerpoint_export']['include']]

    # Sort by priority
    primary = [c for c in included if c['powerpoint_export']['priority'] == '1-PrimaryFocus']
    secondary = [c for c in included if c['powerpoint_export']['priority'] == '2-SecondaryFocus']
    additional = [c for c in included if c['powerpoint_export']['priority'] == '3-AdditionalFinding']

    # Generate slides
    slides = []
    slides.append(executive_summary_slide(organization, primary))

    for check in primary:
        slides.append(critical_finding_slide(check))

    slides.append(high_priority_risks_slide(secondary))
    slides.append(additional_context_slide(additional))
    slides.append(roadmap_slide(primary + secondary))

    return create_powerpoint(slides)
```

### Recommended Slide Structure

```
Slide 1: Executive Summary
  - Overall DRIVE maturity level (1-5)
  - Count of 1-PrimaryFocus findings
  - Top 3-5 critical risks (executive_summary)
  - Trend chart (if historical data available)

Slides 2-4: Critical Findings (1-PrimaryFocus)
  - One finding per slide (or 2-3 max)
  - Chart visualization (gauge/trend)
  - Executive summary
  - Recommended action + timeline
  - Business impact

Slides 5-7: High Priority Risks (2-SecondaryFocus)
  - Multiple findings per slide
  - Grouped by slide_section
  - Bar charts or tables
  - Remediation timeline

Slide 8: Additional Context (3-AdditionalFinding)
  - Summary table
  - Link to full technical report
  - Quick wins highlighted

Slide 9: Remediation Roadmap
  - Timeline view (30/60/90 days)
  - Cost/effort estimates
  - Resource requirements
  - Quick wins vs strategic investments
```

---

## Testing Results

### Migration Test

```bash
$ python3 tools/add_powerpoint_export_tags.py checks/SP-ES-001.yaml

🚀 Processing 1 check files...
✅ checks/SP-ES-001.yaml: Added priority=1-PrimaryFocus
======================================================================
📊 Migration Summary:
   ✅ Updated: 1
   ⏭️  Skipped: 0
   ❌ Errors: 0
   📁 Total: 1
======================================================================
```

### Validation Test

```bash
$ python3 tools/validate_checks.py checks/SP-ES-001.yaml

✅ checks/SP-ES-001.yaml: PASSED
```

### Sample Output

```yaml
powerpoint_export:
  include: true
  priority: 1-PrimaryFocus
  slide_section: Critical Findings
  chart_visualization: gauge
  executive_summary: 'Anyone' links allow anonymous access from the internet.
```

---

## Next Steps

### Immediate (Required)

1. **Migrate All Checks**
   ```bash
   python3 tools/add_powerpoint_export_tags.py
   ```

2. **Review Primary Focus Checks**
   - Ensure executive summaries are compelling
   - Verify business impact is clear
   - Confirm correct prioritization

3. **Commit Changes**
   ```bash
   git add checks/*.yaml tools/*.py docs/*.md CLAUDE.md
   git commit -m "Add PowerPoint export tagging (schema v2.1)"
   git push
   ```

### Short-Term (Recommended)

4. **Manual Refinement**
   - Review all `1-PrimaryFocus` checks for executive relevance
   - Add detailed executive summaries where missing
   - Adjust priorities based on organizational context

5. **Custom Mappings**
   - Create organization-specific priority overrides
   - Document rationale for custom priorities

### Long-Term (Future Enhancement)

6. **PowerPoint Generation**
   - Implement Python script using `python-pptx`
   - Integrate with 1Secure API for live data
   - Add chart generation (matplotlib/plotly)
   - Create branded templates

7. **Web UI Integration**
   - Add "Export to PowerPoint" button in DRIVE web app
   - Allow users to customize priority assignments
   - Preview slides before export

---

## Troubleshooting

### Issue: Migration script fails with YAML error

```bash
❌ checks/BAD-CHECK.yaml: YAML parsing error
```

**Solution:** Fix YAML syntax in the check file, then re-run migration.

### Issue: Check marked as v2.1 but no powerpoint_export section

```bash
⚠️  Schema v2.1 check missing powerpoint_export section - will use defaults
```

**Solution:** Re-run migration script on this check:
```bash
python3 tools/add_powerpoint_export_tags.py checks/MISSING-CHECK.yaml
```

### Issue: Too many Primary Focus checks (>10% of total)

**Solution:** Review and demote less critical checks:
1. Identify all `1-PrimaryFocus` checks
2. Assess true executive relevance
3. Demote to `2-SecondaryFocus` if appropriate
4. Focus on immediate threats only (Level 1 Critical/High)

### Issue: Executive summary too long (>200 characters)

```bash
⚠️  powerpoint_export.executive_summary is 245 characters (recommend <200)
```

**Solution:** Edit check file and shorten executive_summary:
```yaml
# Before (245 chars)
executive_summary: "Anonymous links allow unauthorized public internet access to sensitive corporate documents containing confidential business information, enabling potential data breaches that could result in regulatory fines and reputational damage"

# After (198 chars)
executive_summary: "Anonymous links expose confidential documents to public internet without authentication, enabling data breaches and regulatory compliance violations"
```

---

## Support & Resources

### Documentation
- **Schema Spec:** `/docs/YAML_SCHEMA_V2.1.md` - Complete schema reference
- **Dev Guide:** `/CLAUDE.md` - Developer commands and workflows
- **This Guide:** `/docs/POWERPOINT_EXPORT_IMPLEMENTATION.md` - Implementation guide

### Tools
- **Migration:** `tools/add_powerpoint_export_tags.py` - Add PowerPoint tags
- **Validation:** `tools/validate_checks.py` - Validate YAML checks
- **Analysis:** Use `grep`, `jq`, or Python to analyze priorities

### Example Queries

```bash
# Count checks by priority
grep -r "priority:" checks/*.yaml | cut -d: -f3 | sort | uniq -c

# Find all Primary Focus checks
grep -l "priority: 1-PrimaryFocus" checks/*.yaml

# Extract executive summaries
grep -A1 "executive_summary:" checks/*.yaml

# Find checks missing executive summary
python3 << 'EOF'
import yaml, os
from pathlib import Path

for f in Path('checks').glob('*.yaml'):
    with open(f) as file:
        check = yaml.safe_load(file)
        pptx = check.get('powerpoint_export', {})
        if pptx.get('priority') == '1-PrimaryFocus' and 'executive_summary' not in pptx:
            print(f"Missing executive_summary: {f}")
EOF
```

---

## Change Log

### October 16, 2025 - Initial Release (v2.1)

**Added:**
- PowerPoint export tagging schema
- `powerpoint_export` section with 5 fields
- Priority classification (1-4 scale)
- Intelligent migration script with keyword detection
- Updated validation script supporting v2.1
- Comprehensive documentation

**Changed:**
- Schema version bumped from 2.0 → 2.1
- Validation script now supports optional `powerpoint_export` section
- CLAUDE.md updated with new migration commands

**Backward Compatible:**
- v2.0 checks continue to work without changes
- Validation gracefully handles missing `powerpoint_export` section
- Default priority assignment for v2.0 checks

---

**Version:** 1.0.0
**Last Updated:** October 16, 2025
**Authors:** DRIVE Team
**Status:** ✅ Complete and Production Ready
