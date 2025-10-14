# 1Secure to DRIVE Catalog Mapping Report

## Executive Summary

**1Secure Risks:** 52 total
**1Secure Mapped:** 52 (100.0%)

**DRIVE Checks:** 118 total
**DRIVE Covered by 1Secure:** 3 (2.5%)

## Platform Coverage

- **Active Directory**: 0/63 (0.0%)
- **Exchange Online**: 0/4 (0.0%)
- **File System**: 0/13 (0.0%)
- **OneDrive**: 0/8 (0.0%)
- **SharePoint**: 3/24 (12.5%)
- **Teams**: 0/6 (0.0%)

## Category Coverage

- **Access Control**: 3/32 (9.4%)
- **Compliance & Governance**: 0/7 (0.0%)
- **Configuration**: 0/1 (0.0%)
- **Data Discovery & Classification**: 0/12 (0.0%)
- **Data Protection**: 0/1 (0.0%)
- **Identity**: 0/65 (0.0%)

## Detailed Mappings


### Data


**Third-Party Applications Allowed**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:
  - `SP-ES-006`: Sharepoint external sharing to consumer domains (Level N/A)

**High Risk Permissions on Documents**
- Measure: %
- Thresholds: Low=Below 5, Medium=5 to 15, High=15 and above
- Maps to DRIVE checks:

**Stale Direct User Permissions**
- Measure: %
- Thresholds: Low=Below 5, Medium=5 to 15, High=15 and above
- Maps to DRIVE checks:

**Sites with Broken Permissions Inheritance**
- Measure: %
- Thresholds: Low=Below 60, Medium=60 to 100, High=100 and above
- Maps to DRIVE checks:

**External and Anonymous Sharing of Sensitive Data**
- Measure: %
- Thresholds: Low=Below 5, Medium=5 to 15, High=15 and above
- Maps to DRIVE checks:
  - `SP-ES-001`: Sharepoint open access (anyone links present) (Level N/A)
  - `SP-ES-002`: Sharepoint anyone links with edit (Level N/A)

**Unlabeled Sensitive Files**
- Measure: %
- Thresholds: Low=Below 10, Medium=10 to 30, High=30 and above
- Maps to DRIVE checks:

**Stale User Access to Sensitive Data**
- Measure: %
- Thresholds: Low=Below 5, Medium=5 to 15, High=15 and above
- Maps to DRIVE checks:

**Open Access to Sensitive Data**
- Measure: %
- Thresholds: Low=Below 0, Medium=Below 2, High=2 and above
- Maps to DRIVE checks:

**High-Risk Permissions to Sensitive Data**
- Measure: %
- Thresholds: Low=Below 0, Medium=Below 2, High=2 and above
- Maps to DRIVE checks:

### Identity


**User Accounts with "Password Never Expires"**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 6, High=6 and above
- Maps to DRIVE checks:

**User Accounts with "Password Not Required"**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 3, High=3 and above
- Maps to DRIVE checks:

**Inactive User Accounts**
- Measure: %
- Thresholds: Low=Below 0.01, Medium=0.01 to 1, High=1 and above
- Maps to DRIVE checks:

**User Accounts with Administrative Permissions**
- Measure: %
- Thresholds: Low=Below 2, Medium=2 to 3, High=3 and above
- Maps to DRIVE checks:

**Administrative Groups**
- Measure: %
- Thresholds: Low=Below 2, Medium=2 to 3, High=3 and above
- Maps to DRIVE checks:

**Empty Security Groups**
- Measure: %
- Thresholds: Low=Below 1, Medium=1 to 2, High=2 and above
- Maps to DRIVE checks:

**Dangerous Default Permissions**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Improper Number of Global Administrators**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Conditional Access Policy Disables Admin Token Persistence**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Self-Serve Password Reset is Not Enabled**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**MS Graph Powershell Service Principal Assignment Not Enforced**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Stale Guest Accounts**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 5, High=5 and above
- Maps to DRIVE checks:

**User Accounts with "No MFA Configured"**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 5, High=5 and above
- Maps to DRIVE checks:

**User Accounts Created via Email Verified Self-Service Creation**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 5, High=5 and above
- Maps to DRIVE checks:

**Global Administrators**
- Measure: Num
- Thresholds: Low=Below 4, Medium=4, High=5 and above
- Maps to DRIVE checks:

**Unusual Primary Group on Computer Account**
- Measure: Num
- Thresholds: Low=Below 5, Medium=5 to 10, High=10 and above
- Maps to DRIVE checks:

**Restriction of Dangerous Privileges for Standard Users**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 5, High=5 and above
- Maps to DRIVE checks:

**Review of Delegated Permissions for Standard Users on Organizational Units**
- Measure: Num
- Thresholds: Low=Below 5, Medium=5 to 10, High=10 and above
- Maps to DRIVE checks:

**Same Domain SID History Association**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Well-Known SIDs in SID History**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Administrative Accounts Susceptible to Kerberoasting**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Domain Controller RPC Coercion**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Admin Accounts with Email Access**
- Measure: Num
- Thresholds: Low=Below 5, Medium=5 and above, High=-
- Maps to DRIVE checks:

### Infrastructure


**Disabled Computer Accounts**
- Measure: %
- Thresholds: Low=Below 1, Medium=1 to 3, High=3 and above
- Maps to DRIVE checks:

**Inactive Computer Accounts**
- Measure: %
- Thresholds: Low=Below 0.01, Medium=0.01 to 3, High=3 and above
- Maps to DRIVE checks:

**Unified Audit Log Search is Not Enabled**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Conditional Access Policies and Microsoft Secure Defaults status**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Expired Domain Registrations Found**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**MS Graph Powershell Service Principal Configuration Missing**
- Measure: Binary
- Thresholds: Low=No risk, Medium=-, High=
- Maps to DRIVE checks:

**Legacy authentication protocols enabled**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Domain Controller SMB v1 Vulnerability**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Domain Controller Registration Status**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 3, High=3 and above
- Maps to DRIVE checks:

**Domain Controller Logon Privileges Restriction**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Domain Controller Ownership Verification**
- Measure: Num
- Thresholds: Low=0, Medium=1 to 5, High=5 and above
- Maps to DRIVE checks:

**ESC1: Vulnerable Subject Control in Certificate Templates**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**ESC2: Vulnerable EKU Configurations in Certificate Templates**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**ESC4: Low-Privileged User Access to Published Certificate Templates**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**ESC3: Misconfigured Agent Enrollment Templates**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**Obsolete Windows Server 2012 Member Servers**
- Measure: Num
- Thresholds: Low=Below 6, Medium=6 to 21, High=21 and above
- Maps to DRIVE checks:

**Obsolete Windows 2012 Domain Controllers**
- Measure: Num
- Thresholds: Low=0, Medium=-, High=1 and above
- Maps to DRIVE checks:

**OU Accidental Deletion Protection**
- Measure: Num
- Thresholds: Low=0, Medium=1 and above, High=-
- Maps to DRIVE checks:

**Weak TLS Protocols used by LDAPS**
- Measure: Num
- Thresholds: Low=0, Medium=1 and above, High=-
- Maps to DRIVE checks:

**Outdated Domain Functional Level (2012R2)**
- Measure: Num
- Thresholds: Low=0, Medium=1 and above, High=-
- Maps to DRIVE checks:

## Unmapped DRIVE Checks (Available for Future Integration)


### Active Directory (63 checks)

- `AD-001`: Enabled user accounts stale (no recent lastLogonTimestamp)
- `AD-002`: Disabled accounts still members of groups
- `AD-003`: Contractor accounts (employeeType=Contractor) without 'accountExpires'
- `AD-004`: Users without manager/ownership metadata (no 'manager' attribute) in privileged groups
- `AD-005`: Users with 'Password not required' (PASSWD_NOTREQD)
- `AD-006`: Users with reversible encryption allowed (ENCRYPTED_TEXT_PWD_ALLOWED)
- `AD-007`: Users with 'Do not require Kerberos preauthentication' (DONT_REQUIRE_PREAUTH)
- `AD-008`: krbtgt password age exceeds threshold
- `AD-009`: Domain password policy too weak (length/history/lockout/complexity)
- `AD-010`: Users with 'Password never expires' (DONT_EXPIRE_PASSWORD)
- ... and 53 more

### Exchange Online (4 checks)

- `AC-001-EX`: Inactive user (>90 days) still retains permissions to Exchange resources.
- `ES-001-EX`: External recipient/guest has access to sensitive mailbox items or shared mailboxes.
- `ES-002-EX`: Sensitive data (emails/attachments) shared externally across multiple domains.
- `ES-004-EX`: Inactive external recipient/guest still has access to sensitive mailbox data.

### File System (13 checks)

- `FS-032`: File System Empty Shares
- `FS-033`: File System missing full control ACE
- `FS-AX-005`: File system change permissions/take ownership to non-admins
- `FS-AX-006`: File system unintended inheritance to sensitive paths
- `FS-AX-007`: File system broken inheritance with excessive explicit aces
- `FS-AX-008`: File system orphaned sids in acls
- `FS-AX-009`: File system over-nested groups creating implicit access
- `FS-AX-010`: File system local accounts on in acls
- `FS-AX-011`: File system stale privileged access
- `FS-AX-012`: File system broad access to hidden/admin shares
- ... and 3 more

### OneDrive (8 checks)

- `AC-001-OD`: Inactive user (>90 days) still retains permissions to OneDrive resources.
- `AC-003-OD`: Orphaned users (not resolvable in directory) still appear on ACLs.
- `AC-007-OD`: Site/workload is stale (no activity >180 days).
- `AC-008-OD`: Files are stale (no access >365 days).
- `CC-002-OD`: Non-expiring (permanent) links are allowed.
- `DE-002-OD`: Anonymous sharing links are enabled (scope == anonymous).
- `ES-001-OD`: Guest user has access to sensitive content.
- `ES-002-OD`: Sensitive files shared to multiple external domains.

### SharePoint (21 checks)

- `AC-001-SPO`: Inactive user (>90 days) still retains permissions to SharePoint Online resources.
- `AC-003-SPO`: Orphaned users (not resolvable in directory) still appear on ACLs.
- `AC-006`: Broken permission inheritance
- `AC-007-SPO`: Site/workload is stale (no activity >180 days).
- `AC-008-SPO`: Files are stale (no access >365 days).
- `CC-002-SPO`: Non-expiring (permanent) links are allowed.
- `DE-002-SPO`: Anonymous sharing links are enabled (scope == anonymous).
- `DE-003`: File Shared with Everyone
- `ES-001-SPO`: Guest user has access to sensitive content.
- `ES-002-SPO`: Sensitive files shared to multiple external domains.
- ... and 11 more

### Teams (6 checks)

- `AC-001-Teams`: Inactive user (>90 days) still retains permissions to Microsoft Teams resources.
- `DE-001`: Org-wide Teams sharing  (scope == organization)
- `DE-002-Teams`: Anonymous links to files shared via Teams (backed by SharePoint/OneDrive) are enabled (scope == anonymous).
- `ES-001-Teams`: Guest user has access to sensitive content.
- `ES-002-Teams`: Sensitive files shared to multiple external domains.
- `ES-003`: Shared Channels with sensitive content