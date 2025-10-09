#!/usr/bin/env python3
"""
DRIVE Check Validation Tool
Validates YAML check definitions against schema requirements
"""
import yaml
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Schema requirements
REQUIRED_ROOT_FIELDS = [
    'check_id', 'title', 'short_description', 'detailed_description',
    'category', 'platform', 'drive_pillars', 'automatable', 'owner',
    'status', 'detection', 'level_thresholds', 'framework_mappings',
    'remediation', 'validation', 'references', 'metadata'
]

REQUIRED_THRESHOLD_FIELDS = [
    'level', 'threshold_id', 'threshold_condition', 'threshold_description',
    'severity', 'business_impact', 'threat_timeline', 'attacker_profile',
    'cvss_score', 'points_deduction', 'remediation_priority'
]

VALID_SEVERITIES = ['Critical', 'High', 'Medium', 'Low']
VALID_PLATFORMS = [
    'Active Directory', 'SharePoint', 'OneDrive', 'Teams',
    'Exchange Online', 'File System', 'Azure AD', 'Entra ID'
]
VALID_PILLARS = ['D', 'R', 'I', 'V', 'E']
VALID_LEVELS = [1, 2, 3, 4, 5]
VALID_STATUSES = ['active', 'draft', 'deprecated', 'archived']

class CheckValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []

    def validate_check_file(self, file_path: str) -> bool:
        """Validate a single YAML check file"""
        self.errors = []
        self.warnings = []
        self.info = []

        try:
            with open(file_path, 'r') as f:
                check = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parsing error: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False

        # Validate structure
        self._validate_required_fields(check)
        self._validate_check_id(check)
        self._validate_drive_pillars(check)
        self._validate_level_thresholds(check)
        self._validate_framework_mappings(check)
        self._validate_remediation(check)
        self._validate_metadata(check)

        return len(self.errors) == 0

    def _validate_required_fields(self, check: Dict):
        """Validate all required root fields are present"""
        for field in REQUIRED_ROOT_FIELDS:
            if field not in check:
                self.errors.append(f"Missing required field: {field}")

    def _validate_check_id(self, check: Dict):
        """Validate check_id format and uniqueness"""
        if 'check_id' not in check:
            return

        check_id = check['check_id']

        # Format: PLATFORM-CATEGORY-###
        if not check_id or len(check_id) < 5:
            self.errors.append(f"Invalid check_id format: {check_id}")

        # Check platform
        platform = check.get('platform', '')
        if platform not in VALID_PLATFORMS:
            self.warnings.append(f"Unusual platform: {platform}")

        # Check status
        status = check.get('status', '')
        if status not in VALID_STATUSES:
            self.errors.append(f"Invalid status: {status}. Must be one of {VALID_STATUSES}")

    def _validate_drive_pillars(self, check: Dict):
        """Validate DRIVE pillars"""
        if 'drive_pillars' not in check:
            return

        pillars = check['drive_pillars']
        if not isinstance(pillars, list):
            self.errors.append("drive_pillars must be a list")
            return

        if len(pillars) == 0:
            self.errors.append("At least one DRIVE pillar must be specified")

        for pillar in pillars:
            if pillar not in VALID_PILLARS:
                self.errors.append(f"Invalid DRIVE pillar: {pillar}. Must be one of {VALID_PILLARS}")

    def _validate_level_thresholds(self, check: Dict):
        """Validate level thresholds structure and content"""
        if 'level_thresholds' not in check:
            return

        thresholds = check['level_thresholds']
        if not isinstance(thresholds, list):
            self.errors.append("level_thresholds must be a list")
            return

        if len(thresholds) == 0:
            self.errors.append("At least one level threshold must be defined")
            return

        # Track levels to ensure proper coverage
        levels_covered = set()
        threshold_ids = set()

        for idx, threshold in enumerate(thresholds):
            # Check required fields
            for field in REQUIRED_THRESHOLD_FIELDS:
                if field not in threshold:
                    self.errors.append(f"Threshold {idx}: Missing required field '{field}'")

            # Validate level
            level = threshold.get('level')
            if level not in VALID_LEVELS:
                self.errors.append(f"Threshold {idx}: Invalid level {level}. Must be 1-5")
            else:
                levels_covered.add(level)

            # Validate threshold_id uniqueness
            threshold_id = threshold.get('threshold_id', '')
            if threshold_id in threshold_ids:
                self.errors.append(f"Duplicate threshold_id: {threshold_id}")
            threshold_ids.add(threshold_id)

            # Validate severity
            severity = threshold.get('severity')
            if severity not in VALID_SEVERITIES:
                self.errors.append(f"Threshold {idx}: Invalid severity '{severity}'. Must be one of {VALID_SEVERITIES}")

            # Validate CVSS score
            cvss = threshold.get('cvss_score')
            if cvss is not None and (not isinstance(cvss, (int, float)) or cvss < 0 or cvss > 10):
                self.errors.append(f"Threshold {idx}: Invalid CVSS score {cvss}. Must be 0-10")

            # Validate points deduction
            points = threshold.get('points_deduction')
            if points is not None and (not isinstance(points, (int, float)) or points < 0):
                self.errors.append(f"Threshold {idx}: Invalid points_deduction {points}. Must be >= 0")

            # Validate remediation priority
            priority = threshold.get('remediation_priority')
            if priority is not None and (not isinstance(priority, int) or priority < 1):
                self.errors.append(f"Threshold {idx}: Invalid remediation_priority {priority}. Must be >= 1")

        # Check level coverage
        if 1 not in levels_covered:
            self.warnings.append("No Level 1 threshold defined - check may not block critical exposures")

        # Level ordering validation
        sorted_levels = sorted(levels_covered)
        if len(sorted_levels) > 1:
            expected_points = []
            for level in sorted_levels:
                level_thresholds = [t for t in thresholds if t.get('level') == level]
                max_points = max([t.get('points_deduction', 0) for t in level_thresholds])
                expected_points.append((level, max_points))

            # Lower levels should generally have higher point deductions
            for i in range(len(expected_points) - 1):
                if expected_points[i][1] < expected_points[i+1][1]:
                    self.warnings.append(
                        f"Level {expected_points[i+1][0]} has higher points_deduction than Level {expected_points[i][0]} - verify this is intentional"
                    )

    def _validate_framework_mappings(self, check: Dict):
        """Validate framework mappings"""
        if 'framework_mappings' not in check:
            return

        mappings = check['framework_mappings']

        # Check for minimum framework coverage
        if 'nist_csf' not in mappings:
            self.warnings.append("Missing NIST CSF mapping - recommended for all checks")

        if 'cis_v8' not in mappings:
            self.warnings.append("Missing CIS v8 mapping - recommended for all checks")

        # Validate NIST CSF structure
        if 'nist_csf' in mappings:
            nist = mappings['nist_csf']
            if 'function' not in nist:
                self.warnings.append("NIST CSF mapping missing 'function' field")
            valid_functions = ['IDENTIFY', 'PROTECT', 'DETECT', 'RESPOND', 'RECOVER', 'GOVERN']
            if nist.get('function') not in valid_functions:
                self.warnings.append(f"NIST CSF function should be one of {valid_functions}")

    def _validate_remediation(self, check: Dict):
        """Validate remediation section"""
        if 'remediation' not in check:
            return

        remediation = check['remediation']

        # Check required remediation fields
        required_remediation_fields = [
            'automated_fix_available', '1secure_remediable', 'fix_complexity',
            'estimated_time_minutes', 'prerequisites', 'steps'
        ]

        for field in required_remediation_fields:
            if field not in remediation:
                self.warnings.append(f"Remediation missing recommended field: {field}")

        # Validate steps structure
        if 'steps' in remediation:
            steps = remediation['steps']
            if not isinstance(steps, list):
                self.errors.append("Remediation steps must be a list")
            else:
                for idx, step in enumerate(steps):
                    if 'step' not in step:
                        self.errors.append(f"Remediation step {idx}: Missing 'step' number")
                    if 'action' not in step:
                        self.errors.append(f"Remediation step {idx}: Missing 'action' description")

    def _validate_metadata(self, check: Dict):
        """Validate metadata section"""
        if 'metadata' not in check:
            return

        metadata = check['metadata']

        # Check version format
        version = metadata.get('version', '')
        if not version or not version.count('.') >= 2:
            self.warnings.append(f"Invalid version format: {version}. Expected X.Y.Z")

        # Check dates
        last_reviewed = metadata.get('last_reviewed', '')
        if last_reviewed:
            try:
                datetime.fromisoformat(last_reviewed)
            except ValueError:
                self.warnings.append(f"Invalid date format for last_reviewed: {last_reviewed}")

        next_review = metadata.get('next_review_due', '')
        if next_review:
            try:
                datetime.fromisoformat(next_review)
            except ValueError:
                self.warnings.append(f"Invalid date format for next_review_due: {next_review}")

    def print_results(self, file_path: str):
        """Print validation results"""
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print(f"✅ {file_path}: PASSED")
            return True
        else:
            if len(self.errors) > 0:
                print(f"❌ {file_path}: FAILED")
                for error in self.errors:
                    print(f"   ERROR: {error}")
            else:
                print(f"⚠️  {file_path}: PASSED with warnings")

            if len(self.warnings) > 0:
                for warning in self.warnings:
                    print(f"   WARNING: {warning}")

            return len(self.errors) == 0


def validate_all_checks(checks_dir: str) -> tuple[int, int, int]:
    """Validate all YAML files in checks directory"""
    checks_path = Path(checks_dir)

    if not checks_path.exists():
        print(f"❌ Checks directory not found: {checks_dir}")
        return 0, 0, 0

    yaml_files = list(checks_path.glob("*.yaml")) + list(checks_path.glob("*.yml"))

    if len(yaml_files) == 0:
        print(f"⚠️  No YAML files found in {checks_dir}")
        return 0, 0, 0

    print(f"\n🔍 Validating {len(yaml_files)} check files...\n")

    validator = CheckValidator()
    passed = 0
    failed = 0
    warnings_count = 0

    for yaml_file in sorted(yaml_files):
        result = validator.validate_check_file(str(yaml_file))
        validator.print_results(str(yaml_file))

        if result:
            if len(validator.warnings) > 0:
                warnings_count += 1
            else:
                passed += 1
        else:
            failed += 1

        print()  # Blank line between checks

    # Summary
    print("=" * 70)
    print(f"📊 Validation Summary:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ⚠️  Passed with warnings: {warnings_count}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Total: {len(yaml_files)}")
    print("=" * 70)

    return passed, warnings_count, failed


def main():
    if len(sys.argv) > 1:
        # Validate specific file or directory
        target = sys.argv[1]
        if os.path.isfile(target):
            validator = CheckValidator()
            result = validator.validate_check_file(target)
            validator.print_results(target)
            sys.exit(0 if result else 1)
        elif os.path.isdir(target):
            passed, warnings, failed = validate_all_checks(target)
            sys.exit(0 if failed == 0 else 1)
        else:
            print(f"❌ Invalid path: {target}")
            sys.exit(1)
    else:
        # Default: validate checks directory
        checks_dir = os.path.join(os.path.dirname(__file__), '..', 'checks')
        passed, warnings, failed = validate_all_checks(checks_dir)
        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
