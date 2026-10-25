#!/usr/bin/env python3
"""
Generate Northstar Personal Data Deletion Audit Dataset.
Produces 518 cases in dataset/deletion_requests.csv along with supporting CSVs and evidence files.
"""

import os
import csv
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta, timezone

DATASET_DIR = "dataset"
EVIDENCE_DIR = os.path.join(DATASET_DIR, "evidence")

def hash_email(email: str) -> str:
    return hashlib.sha256(email.lower().strip().encode('utf-8')).hexdigest()

def ensure_dirs():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("evaluation", exist_ok=True)

def generate_deletion_rules():
    rules_path = os.path.join(DATASET_DIR, "deletion_rules.csv")
    rules = [
        ["category", "system_id", "required_treatment", "allowed_identifiers", "retention_period_days"],
        ["primary_account", "account_service", "DELETE_RECORD", "none", "0"],
        ["tombstone_record", "account_service", "REDACT_RECORD", "user_id", "3650"],
        ["order_history", "order_service", "ANONYMIZE_RECORD", "user_id,order_id", "2555"],
        ["support_tickets", "support_desk", "REDACT_RECORD", "ticket_id,user_id", "1095"],
        ["search_index", "search_service", "DELETE_RECORD", "none", "0"],
        ["analytics_export", "analytics_dw", "ANONYMIZE_RECORD", "user_id,event_name", "730"],
        ["sync_pipeline", "crm_sync_engine", "DISABLE_DATA_FLOW", "none", "0"],
        ["backup_archive", "backup_vault", "BLOCK_RESTORE", "none", "365"],
        ["audit_trail", "security_audit_log", "REDACT_RECORD", "user_id,event_type", "3650"],
        ["financial_ledger", "finance_service", "VERIFY_RECORD_PRESENT", "user_id,transaction_id", "3650"],
    ]
    with open(rules_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rules)

def generate_dataset():
    ensure_dirs()
    generate_deletion_rules()

    # Generate 518 cases
    requests = []
    identities = []
    audit_logs = []
    activities = []
    evidence_manifest = []

    # Prepare SQLite snapshot DB for evidence
    sqlite_db_path = os.path.join(EVIDENCE_DIR, "system_snapshots.sqlite")
    conn = sqlite3.connect(sqlite_db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_records (user_id TEXT, email TEXT, status TEXT, last_updated TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS support_attachments (attachment_id TEXT, user_id TEXT, file_name TEXT, content TEXT, created_at TEXT)")

    base_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

    for i in range(518):
        case_id = f"case_{i:03d}"
        user_id = f"user_{1000 + i}"
        email = f"customer_{i}@northstar-example.com"
        old_email = f"old_customer_{i}@olddomain.com" if i % 4 == 1 else ""
        requested_at = (base_time + timedelta(days=i % 30, hours=i % 24)).isoformat()
        reported_at = (base_time + timedelta(days=i % 30, hours=(i % 24) + 2)).isoformat()
        audit_at = (base_time + timedelta(days=i % 30 + 5, hours=i % 24)).isoformat()

        # Decide case archetype
        if i % 10 == 0:
            # NOT_APPLICABLE: user asked question or withdrew request
            reported_status = "NOT_STARTED"
            request_text = "Hi Northstar support, I have a question about my order delivery status. Please do not delete my account."
            status_type = "NOT_APPLICABLE"
        elif i % 3 == 0:
            # COMPLETE: deletion finished properly before audit_at
            reported_status = "COMPLETE"
            request_text = f"Please delete all my personal data and account records for user {user_id}."
            status_type = "COMPLETE"
        else:
            # INCOMPLETE: remaining records, active sync, or restore risk
            reported_status = "COMPLETE" if i % 2 == 0 else "PARTIALLY_COMPLETE"
            request_text = f"I request complete deletion of all personal data under GDPR/CCPA for email {email}."
            status_type = "INCOMPLETE"

        requests.append([case_id, email, requested_at, reported_status, reported_at, audit_at, request_text])

        # Identity
        email_h = hash_email(email)
        identities.append([user_id, email, f"+1-555-{i:04d}", email_h, f"Customer {i}", requested_at])

        if old_email:
            audit_id = f"audit_id_{i}"
            audit_logs.append([audit_id, user_id, "EMAIL_CHANGE", old_email, email, requested_at, "user_settings"])

        # System Activity & Evidence
        activity_id_1 = f"act_{i}_1"
        activity_id_2 = f"act_{i}_2"

        if status_type == "COMPLETE":
            activities.append([activity_id_1, "account_service", f"account_{i:03d}", "DELETE_RECORD", user_id, "SUCCESS", reported_at, "Account record deleted"])
            activities.append([activity_id_2, "search_service", f"search_doc_{i:03d}", "DELETE_RECORD", user_id, "SUCCESS", reported_at, "Search index cleared"])
        elif status_type == "INCOMPLETE":
            activities.append([activity_id_1, "account_service", f"account_{i:03d}", "DELETE_RECORD", user_id, "SUCCESS", reported_at, "Primary account tombstoned"])
            if i % 5 == 1:
                # Active sync flow risk
                activities.append([activity_id_2, "crm_sync_engine", f"sync_job_{i:03d}", "RECREATE_DATA", user_id, "ACTIVE", audit_at, "CRM sync job active and auto-recreating user data"])
            elif i % 5 == 2:
                # Restore risk
                activities.append([activity_id_2, "backup_vault", f"backup_snapshot_{i:03d}", "RESTORE_PATH", user_id, "ACTIVE", audit_at, "Unblocked backup snapshot contains unredacted user data"])
            else:
                # Secondary record / search index remaining
                activities.append([activity_id_2, "search_service", f"search_doc_{i:03d}", "INDEX_RECORD", user_id, "PRESENT", audit_at, "Exposed email in search index"])

            # Add sqlite snapshot entry
            cur.execute("INSERT INTO user_records VALUES (?, ?, ?, ?)", (user_id, email, "PRESENT" if status_type == "INCOMPLETE" else "DELETED", audit_at))
            cur.execute("INSERT INTO support_attachments VALUES (?, ?, ?, ?, ?)", (f"att_{i}", user_id, f"passport_scan_{i}.pdf", f"Contains PII for {email}", audit_at))

    conn.commit()
    conn.close()

    # Write deletion_requests.csv
    with open(os.path.join(DATASET_DIR, "deletion_requests.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"])
        writer.writerows(requests)

    # Write sample_deletion_requests.csv (First 10 cases)
    with open(os.path.join(DATASET_DIR, "sample_deletion_requests.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"])
        writer.writerows(requests[:10])

    # Write user_identities.csv
    with open(os.path.join(DATASET_DIR, "user_identities.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "email", "phone", "email_hash", "name", "created_at"])
        writer.writerows(identities)

    # Write user_audit_log.csv
    with open(os.path.join(DATASET_DIR, "user_audit_log.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["audit_id", "user_id", "event_type", "old_value", "new_value", "timestamp", "source"])
        writer.writerows(audit_logs)

    # Write system_activity.csv
    with open(os.path.join(DATASET_DIR, "system_activity.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["activity_id", "system_id", "resource_id", "activity_type", "user_id", "status", "timestamp", "details"])
        writer.writerows(activities)

    # Write evidence_files.csv manifest
    evidence_manifest.append(["evidence_01", "system_snapshots", "dataset/evidence/system_snapshots.sqlite", "sqlite", base_time.isoformat(), "System snapshot database"])
    evidence_manifest.append(["evidence_02", "support_logs", "dataset/evidence/support_audit.json", "json", base_time.isoformat(), "Support desk audit json"])

    with open(os.path.join(DATASET_DIR, "evidence_files.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file_id", "system_id", "file_path", "file_type", "created_at", "description"])
        writer.writerows(evidence_manifest)

    # Create json evidence
    support_audit_data = {"audit_file": "support_audit.json", "logs": []}
    for i in range(10):
        support_audit_data["logs"].append({
            "ticket_id": f"ticket_{i:03d}",
            "user_id": f"user_{1000 + i}",
            "customer_email": f"customer_{i}@northstar-example.com",
            "notes": f"Customer ticket log for case_{i:03d}"
        })
    with open(os.path.join(EVIDENCE_DIR, "support_audit.json"), "w", encoding="utf-8") as f:
        json.dump(support_audit_data, f, indent=2)

    # Write blank template output.csv in root and dataset/
    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        f.write("case_id,deletion_status,steps_json\n")
    with open(os.path.join(DATASET_DIR, "output.csv"), "w", newline="", encoding="utf-8") as f:
        f.write("case_id,deletion_status,steps_json\n")

    print("Dataset generated successfully with 518 cases!")

if __name__ == "__main__":
    generate_dataset()
