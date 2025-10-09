# DRIVE Maturity Model - Quick Start Guide

## 🎯 What's New

The DRIVE maturity model now uses an **ANSSI/PingCastle-inspired multi-level threshold approach** where individual security checks can define different severity thresholds across multiple maturity levels.

### Before vs After

**OLD MODEL:**
```
Check: Anonymous Links → Level 1 → Binary Pass/Fail
```

**NEW MODEL:**
```
Check: Anonymous Links →
  Level 1: Edit permissions OR Critical data → FAIL (30 points)
  Level 2: >10 Confidential files → FAIL (15 points)
  Level 3: >50 Permanent links → FAIL (8 points)
  Level 4: Stale unused links → FAIL (3 points)
```

## 🚀 Getting Started

### 1. View Example Checks

```bash
# See multi-level threshold examples
cat checks/SP-ES-001.yaml  # SharePoint anonymous links (4 thresholds)
cat checks/AD-FL-001.yaml  # Active Directory functional level (4 thresholds)
```

### 2. Validate Existing Checks

```bash
# Validate YAML syntax and schema
python3 tools/validate_checks.py checks/

# Expected output:
# ✅ SP-ES-001.yaml: PASSED
# ✅ AD-FL-001.yaml: PASSED
```

### 3. Aggregate for Website

```bash
# Generate JSON catalog for GitHub Pages
python3 tools/aggregate_checks.py checks/

# Output:
# docs/catalog/drive_risk_catalog.json
# docs/catalog/stats.json
```

### 4. View Website Locally

```bash
# Open in browser
open docs/index.html

# Or if on Linux
xdg-open docs/index.html
```

### 5. Deploy to GitHub Pages

```bash
# Push to trigger automated deployment
git add .
git commit -m "Deploy DRIVE maturity model"
git push origin main

# Enable GitHub Pages in repo settings:
# Settings → Pages → Source: main branch, /docs folder
```

## 📁 What Was Created

```
✅ /checks/SP-ES-001.yaml              # Example: SharePoint check
✅ /checks/AD-FL-001.yaml              # Example: AD check
✅ /checks/README.md                   # Check format documentation

✅ /docs/index.html                    # Website homepage
✅ /docs/css/style.css                 # ANSSI-inspired styling
✅ /docs/js/main.js                    # Interactive functionality
✅ /docs/NEW_ARCHITECTURE.md           # Architecture design doc
✅ /docs/QUICK_START.md                # This file

✅ /tools/validate_checks.py           # Validation script
✅ /tools/aggregate_checks.py          # Website generation script
✅ /tools/migrate_csv_to_yaml.py       # CSV→YAML migration script

✅ /.github/workflows/deploy-docs.yml  # CI/CD pipeline

✅ /IMPLEMENTATION_SUMMARY.md          # Detailed implementation notes
✅ /CLAUDE.md                          # Updated development guide
```

## 🔧 Common Tasks

### Create New Check

```bash
# 1. Copy template
cp checks/SP-ES-001.yaml checks/YOUR-CHECK-ID.yaml

# 2. Edit check definition
vi checks/YOUR-CHECK-ID.yaml

# 3. Validate
python3 tools/validate_checks.py checks/YOUR-CHECK-ID.yaml

# 4. Aggregate
python3 tools/aggregate_checks.py checks/
```

### Migrate Existing Checks

```bash
# Convert all 117 CSV checks to YAML
python3 tools/migrate_csv_to_yaml.py

# Review generated files
ls -la checks/

# Manually enhance with multi-level thresholds
# (The migration creates single-threshold YAML as starting point)
```

### Update Website

```bash
# After modifying checks
python3 tools/aggregate_checks.py checks/

# Test locally
open docs/index.html

# Deploy
git add .
git commit -m "Update security checks"
git push origin main
```

## 📊 Maturity Levels

| Level | Name | Score | Timeline | Focus |
|-------|------|-------|----------|-------|
| **1** | Critical Exposure Eliminated | 0-20 | Hours-Days | Stop active data leaks |
| **2** | High Risk Mitigated | 21-40 | Weeks-Months | Secure privileged access |
| **3** | Security Baseline Established | 41-60 | Months-Year | Industry best practices |
| **4** | Enhanced Security Posture | 61-80 | Strategic | Proactive automation |
| **5** | State-of-the-Art Security | 81-100 | Future-proof | Predictive capabilities |

## 🎨 Website Features

### Homepage Sections

1. **Overview**
   - 117 Security Checks
   - 5 Maturity Levels
   - 8+ Framework Mappings
   - Multi-Level Thresholds

2. **Maturity Levels**
   - Color-coded level cards
   - Example blocking conditions
   - Threat timelines
   - Score ranges

3. **Security Checks Browser**
   - Filter by Platform, Level, Pillar
   - Search functionality
   - Click for detailed view
   - Framework mappings

4. **Control Graph** (placeholder)
   - Visual distribution
   - Platform coverage
   - Framework alignment

### Filters Available

- **Platform:** SharePoint, OneDrive, Teams, Exchange, AD, File System
- **Level:** 1 (Critical) → 5 (Optimal)
- **Pillar:** D, R, I, V, E
- **Search:** Free text across all fields

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [IMPLEMENTATION_SUMMARY.md](../IMPLEMENTATION_SUMMARY.md) | Complete implementation details |
| [NEW_ARCHITECTURE.md](./NEW_ARCHITECTURE.md) | Architecture design and rationale |
| [CLAUDE.md](../CLAUDE.md) | Development guide for Claude Code |
| [checks/README.md](../checks/README.md) | Check format specification |
| [DRIVE_PRD.md](./DRIVE_PRD.md) | Product requirements document |

## 🧪 Testing

### Validation Tests

```bash
# Run validation
python3 tools/validate_checks.py checks/

# Check for:
# ✅ Required fields present
# ✅ Valid severity values
# ✅ Valid level numbers (1-5)
# ✅ CVSS scores in range (0-10)
# ✅ Framework mappings complete
```

### Website Tests

```bash
# Generate catalog
python3 tools/aggregate_checks.py checks/

# Open in browser
open docs/index.html

# Test:
# ✅ Levels display correctly
# ✅ Filters work
# ✅ Search works
# ✅ Check details modal opens
# ✅ Mobile responsive
```

## 🔄 Migration Path

### Current Status

- ✅ Architecture designed
- ✅ Schema defined
- ✅ 2 example checks created
- ✅ Validation tooling built
- ✅ Website created
- ✅ CI/CD pipeline configured
- ⏳ 115 checks to migrate

### Next Steps

**Week 1-2: Content Migration**
1. Run migration script: `python3 tools/migrate_csv_to_yaml.py`
2. Review generated YAML files
3. Enhance top 25 priority checks with multi-level thresholds

**Week 3: Website Polish**
1. Add control graph visualization (Chart.js/D3.js)
2. Enhance check detail view
3. Add statistics dashboard

**Week 4: Deployment**
1. Enable GitHub Pages
2. Test end-to-end workflow
3. Launch public site

## 🌐 GitHub Pages Setup

1. **Enable Pages:**
   - Go to: `Settings` → `Pages`
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
   - Click `Save`

2. **Wait for deployment:**
   - GitHub Actions will build
   - Site available at: `https://[username].github.io/drive-risk-catalog/`

3. **Custom domain (optional):**
   - Add CNAME file to `/docs/`
   - Configure DNS records
   - Enable HTTPS (automatic)

## 💡 Tips

### Creating Multi-Level Thresholds

**Ask yourself:**
1. Does severity change with **quantity**? (1 vs 100 items)
2. Does severity change with **scope**? (Internal vs Critical data)
3. Does severity change with **permissions**? (Read vs Edit vs Full Control)
4. Does severity change with **time**? (Recent vs Stale resources)

**If YES to any → Use multi-level thresholds**

### Point Deduction Guidelines

| Severity | Typical Points |
|----------|----------------|
| Critical | 25-35 points |
| High | 12-20 points |
| Medium | 5-10 points |
| Low | 2-5 points |

### Framework Mapping Priority

**Required:**
- NIST CSF 2.0 (function + control)
- CIS v8 (control number)

**Recommended:**
- ISO 27001 (for access control checks)
- CIS M365 (for platform-specific checks)
- MITRE ATT&CK (for Critical/High severity)
- GDPR (for data protection checks)

## 🆘 Troubleshooting

### Validation Fails

```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('checks/YOUR-CHECK.yaml'))"

# Check required fields
grep -E "^(check_id|title|level_thresholds):" checks/YOUR-CHECK.yaml
```

### Website Not Loading Checks

```bash
# Verify JSON generated
ls -la docs/catalog/drive_risk_catalog.json

# Check JSON syntax
python -m json.tool docs/catalog/drive_risk_catalog.json

# Check browser console for errors
```

### GitHub Actions Failing

```bash
# Check workflow file
cat .github/workflows/deploy-docs.yml

# View logs on GitHub
# Actions → Latest run → View logs
```

## 📞 Support

- **Documentation:** See files listed above
- **Examples:** Check `SP-ES-001.yaml` and `AD-FL-001.yaml`
- **Issues:** Create GitHub issue
- **Questions:** Review IMPLEMENTATION_SUMMARY.md

---

**Ready to get started?**

```bash
# View examples
cat checks/SP-ES-001.yaml

# Migrate existing checks
python3 tools/migrate_csv_to_yaml.py

# Deploy website
python3 tools/aggregate_checks.py checks/
open docs/index.html
```

**Visit the website:** `https://[your-github-username].github.io/drive-risk-catalog/`
