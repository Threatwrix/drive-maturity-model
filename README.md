# DRIVE Risk Catalog

A public, framework-mapped catalog of Microsoft 365 data and identity security checks used to compute the DRIVE maturity score.

## What is this?
- A **normalized catalog** of checks (`/catalog/drive_risk_catalog.csv|json`)
- **Framework mappings** (`/frameworks/*.csv`) to NIST CSF, CIS v8, CIS M365, ISO 27001, and ANSSI/PingCastle topics
- **Maturity model config** (`/levels/levels.yaml`) defining level thresholds and required controls
- **Scoring config** (`/scoring/scoring.yaml`) defining categories, severities, and exposure model

## Contributing
1. Edit `catalog/drive_risk_catalog.csv` (preferred) or `catalog/drive_risk_catalog.json`.
2. For each new/updated check, provide:
   - `check_id`, `title`, `category`, `platform`, `severity`, `description`
   - `logic` (deterministic detection criteria)
   - `data_points` (object counts/fields required)
   - `drive_pillar`, `drive_maturity_min`, `drive_weight`
3. Update relevant rows in `/frameworks/*.csv` with authoritative references.
4. Run validation (coming soon) to ensure schema and referential integrity.

## LICENSE
To be determined. Suggested: Apache-2.0.
