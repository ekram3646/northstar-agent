# Remediation Planning & Verification Prompt

## Objective
For `INCOMPLETE` deletion cases, plan ordered remediation actions and verification steps.
For `COMPLETE` deletion cases, generate required verification steps only.

## Allowed Operations & Ordering Rules
Phase 1: FINDING
  1. REPORT_REMAINING_RECORD (state: PRESENT)
  2. REPORT_EXPOSED_PII (state: PRESENT)
  3. REPORT_ACTIVE_DATA_FLOW (state: ACTIVE)
  4. REPORT_RESTORE_RISK (state: ACTIVE)

Phase 2: REMEDIATION
  1. DISABLE_DATA_FLOW (state: DISABLED)
  2. BLOCK_RESTORE (state: BLOCKED)
  3. DELETE_RECORD (state: ABSENT)
  4. REDACT_RECORD (state: REDACTED)
  5. ANONYMIZE_RECORD (state: ANONYMIZED)

Phase 3: VERIFICATION
  1. VERIFY_RECORD_ABSENT (state: ABSENT)
  2. VERIFY_RECORD_PRESENT (state: PRESENT)
  3. VERIFY_RECORD_REDACTED (state: REDACTED)
  4. VERIFY_RECORD_ANONYMIZED (state: ANONYMIZED)
  5. VERIFY_DATA_FLOW_DISABLED (state: DISABLED)
  6. VERIFY_RESTORE_BLOCKED (state: BLOCKED)

Sorting Key: (Phase Index, Operation Index, system_id, resource_id).
Renumber steps consecutively from 1.
