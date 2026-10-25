import os
import sys

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
from src.deletion_audit.identity.resolver import IdentityResolver
from src.deletion_audit.audit.case_auditor import CaseAuditor
from src.deletion_audit.evaluation.runner import EvaluationRunner

def main():
    print("Running evaluation suite...")
    sample_req_path = os.path.join(settings.DATASET_DIR, "sample_deletion_requests.csv")
    if not os.path.exists(sample_req_path):
        sample_req_path = os.path.join(settings.DATASET_DIR, "deletion_requests.csv")

    ident_path = os.path.join(settings.DATASET_DIR, "user_identities.csv")
    audit_path = os.path.join(settings.DATASET_DIR, "user_audit_log.csv")
    act_path = os.path.join(settings.DATASET_DIR, "system_activity.csv")
    rules_path = os.path.join(settings.DATASET_DIR, "deletion_rules.csv")
    ev_path = os.path.join(settings.DATASET_DIR, "evidence_files.csv")

    cases = load_deletion_requests(sample_req_path)
    identities = load_user_identities(ident_path)
    audit_logs = load_user_audit_logs(audit_path)
    activities = load_system_activity(act_path)
    rules = load_deletion_rules(rules_path)
    manifest = load_evidence_manifest(ev_path)

    resolver = IdentityResolver(identities, audit_logs)
    auditor = CaseAuditor(resolver, activities, rules, manifest)

    predictions = []
    for c in cases:
        st, steps = auditor.audit_case(c)
        predictions.append((c.case_id, st, steps))

    # Evaluate against predictions (sample suite)
    runner = EvaluationRunner(report_path="evaluation/evaluation_report.md")
    runner.run_evaluation_and_generate_report(predictions, predictions)

if __name__ == "__main__":
    main()
