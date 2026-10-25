import os
import csv
from typing import List, Dict
from ..models.case import DeletionCase, UserIdentity
from ..models.evidence import SystemActivityRecord, EvidenceFile, DeletionRule

def load_deletion_requests(filepath: str) -> List[DeletionCase]:
    cases = []
    if not os.path.exists(filepath):
        return cases
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(DeletionCase(
                case_id=row["case_id"].strip(),
                email=row["email"].strip(),
                requested_at=row["requested_at"].strip(),
                reported_status=row["reported_status"].strip(),
                reported_at=row["reported_at"].strip(),
                audit_at=row["audit_at"].strip(),
                request_text=row.get("request_text", "").strip()
            ))
    return cases

def load_user_identities(filepath: str) -> Dict[str, UserIdentity]:
    identities: Dict[str, UserIdentity] = {}
    if not os.path.exists(filepath):
        return identities
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row["user_id"].strip()
            identities[uid] = UserIdentity(
                user_id=uid,
                email=row["email"].strip(),
                phone=row.get("phone", "").strip(),
                email_hash=row.get("email_hash", "").strip(),
                name=row.get("name", "").strip(),
                created_at=row.get("created_at", "").strip()
            )
    return identities

def load_user_audit_logs(filepath: str) -> List[Dict[str, str]]:
    audit_logs = []
    if not os.path.exists(filepath):
        return audit_logs
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            audit_logs.append({k: v.strip() for k, v in row.items()})
    return audit_logs

def load_system_activity(filepath: str) -> List[SystemActivityRecord]:
    records = []
    if not os.path.exists(filepath):
        return records
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(SystemActivityRecord(
                activity_id=row["activity_id"].strip(),
                system_id=row["system_id"].strip(),
                resource_id=row["resource_id"].strip(),
                activity_type=row["activity_type"].strip(),
                user_id=row["user_id"].strip(),
                status=row["status"].strip(),
                timestamp=row["timestamp"].strip(),
                details=row.get("details", "").strip()
            ))
    return records

def load_deletion_rules(filepath: str) -> Dict[str, DeletionRule]:
    rules = {}
    if not os.path.exists(filepath):
        return rules
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["category"].strip()
            retention = int(row["retention_period_days"]) if row.get("retention_period_days") else 0
            rules[cat] = DeletionRule(
                category=cat,
                system_id=row["system_id"].strip(),
                required_treatment=row["required_treatment"].strip(),
                allowed_identifiers=row.get("allowed_identifiers", "none").strip(),
                retention_period_days=retention
            )
    return rules

def load_evidence_manifest(filepath: str) -> List[EvidenceFile]:
    evidence = []
    if not os.path.exists(filepath):
        return evidence
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            evidence.append(EvidenceFile(
                file_id=row["file_id"].strip(),
                system_id=row["system_id"].strip(),
                file_path=row["file_path"].strip(),
                file_type=row["file_type"].strip(),
                created_at=row["created_at"].strip(),
                description=row.get("description", "").strip()
            ))
    return evidence
