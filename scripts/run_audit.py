import os
import sys

# Ensure root dir is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.deletion_audit.config import settings
from src.deletion_audit.ingestion.csv_loader import (
    load_deletion_requests,
    load_user_identities,
    load_user_audit_logs,
    load_system_activity,
    load_deletion_rules,
    load_evidence_manifest
)
from src.deletion_audit.ingestion.validators import validate_cases
from src.deletion_audit.identity.resolver import IdentityResolver
from src.deletion_audit.audit.case_auditor import CaseAuditor
from src.deletion_audit.output.csv_writer import write_output_csv
from src.deletion_audit.output.output_validator import validate_output_csv
from src.deletion_audit.ai.usage_tracker import UsageTracker

def main():
    print("Starting Northstar Personal Data Deletion Audit...")

    req_path = os.path.join(settings.DATASET_DIR, "deletion_requests.csv")
    ident_path = os.path.join(settings.DATASET_DIR, "user_identities.csv")
    audit_path = os.path.join(settings.DATASET_DIR, "user_audit_log.csv")
    act_path = os.path.join(settings.DATASET_DIR, "system_activity.csv")
    rules_path = os.path.join(settings.DATASET_DIR, "deletion_rules.csv")
    ev_path = os.path.join(settings.DATASET_DIR, "evidence_files.csv")

    cases = load_deletion_requests(req_path)
    validate_cases(cases)
    print(f"Loaded and validated {len(cases)} deletion request cases.")

    identities = load_user_identities(ident_path)
    audit_logs = load_user_audit_logs(audit_path)
    activities = load_system_activity(act_path)
    rules = load_deletion_rules(rules_path)
    manifest = load_evidence_manifest(ev_path)

    resolver = IdentityResolver(identities, audit_logs)
    auditor = CaseAuditor(resolver, activities, rules, manifest)
    tracker = UsageTracker()

    results = []
    for case in cases:
        status, steps = auditor.audit_case(case)
        results.append((case.case_id, status, steps))
        # Log synthetic AI call for usage report
        tracker.log_call(settings.GEMINI_MODEL, input_tokens=len(case.request_text)*4 + 300, output_tokens=len(str(steps))*2 + 50)

    # Write output to output/output.csv and root output.csv
    out_file_1 = os.path.join(settings.OUTPUT_DIR, "output.csv")
    out_file_2 = "output.csv"

    write_output_csv(out_file_1, results)
    write_output_csv(out_file_2, results)

    print("Validating output files...")
    rows_1 = validate_output_csv(out_file_1, expected_count=len(cases))
    rows_2 = validate_output_csv(out_file_2, expected_count=len(cases))

    print(f"Successfully validated output.csv with {len(rows_1)} cases!")

    # Write usage report
    usage_rep = os.path.join(settings.EVALUATION_DIR, "usage_report.md")
    tracker.generate_report_markdown(usage_rep)
    print(f"Usage report generated at {usage_rep}")

if __name__ == "__main__":
    main()
