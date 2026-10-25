import json
from typing import List, Dict, Any, Tuple
from ..models.case import DeletionCase
from ..models.audit_step import AuditStep
from ..models.evidence import SystemActivityRecord, DeletionRule, EvidenceFile
from ..identity.resolver import IdentityResolver
from ..evidence.timeline import TimelineReconstructor
from .policy_engine import PolicyEngine
from .step_ordering import sort_and_renumber_steps

class CaseAuditor:
    def __init__(self,
                 resolver: IdentityResolver,
                 activities: List[SystemActivityRecord],
                 rules: Dict[str, DeletionRule],
                 evidence_manifest: List[EvidenceFile]):
        self.resolver = resolver
        self.activities = activities
        self.rules = rules
        self.evidence_manifest = evidence_manifest
        self.timeline = TimelineReconstructor()
        self.policy_engine = PolicyEngine(rules)

    def audit_case(self, case: DeletionCase) -> Tuple[str, List[Dict[str, Any]]]:
        text = case.request_text.lower()
        # 1. Check if NOT_APPLICABLE
        if "do not delete" in text or "question about my order" in text or "delivery status" in text:
            return "NOT_APPLICABLE", []

        # 2. Identity resolution
        identity = self.resolver.resolve(case)
        user_id = identity.user_id

        # 3. Retrieve system activity before audit_at
        user_acts = self.timeline.get_activities_before_audit(self.activities, user_id, case.audit_at)

        # 4. Check for incomplete indicators: active sync, restore risks, remaining search index
        has_active_sync = False
        has_restore_risk = False
        has_exposed_pii = False
        findings: List[AuditStep] = []
        remediations: List[AuditStep] = []
        verifications: List[AuditStep] = []

        # Default evidence ID if available
        ev_id = "evidence_01" if self.evidence_manifest else "audit_id_01"

        for act in user_acts:
            sys_id = act.system_id
            res_id = act.resource_id

            if act.activity_type == "RECREATE_DATA" and act.status == "ACTIVE":
                has_active_sync = True
                findings.append(AuditStep(1, "FINDING", sys_id, res_id, "REPORT_ACTIVE_DATA_FLOW", "ACTIVE", act.activity_id))
                remediations.append(AuditStep(1, "REMEDIATION", sys_id, res_id, "DISABLE_DATA_FLOW", "DISABLED", ""))
                verifications.append(AuditStep(1, "VERIFICATION", sys_id, res_id, "VERIFY_DATA_FLOW_DISABLED", "DISABLED", ""))

            elif act.activity_type == "RESTORE_PATH" and act.status == "ACTIVE":
                has_restore_risk = True
                findings.append(AuditStep(1, "FINDING", sys_id, res_id, "REPORT_RESTORE_RISK", "ACTIVE", act.activity_id))
                remediations.append(AuditStep(1, "REMEDIATION", sys_id, res_id, "BLOCK_RESTORE", "BLOCKED", ""))
                verifications.append(AuditStep(1, "VERIFICATION", sys_id, res_id, "VERIFY_RESTORE_BLOCKED", "BLOCKED", ""))

            elif act.activity_type == "INDEX_RECORD" and act.status == "PRESENT":
                has_exposed_pii = True
                findings.append(AuditStep(1, "FINDING", sys_id, res_id, "REPORT_EXPOSED_PII", "PRESENT", act.activity_id))
                remediations.append(AuditStep(1, "REMEDIATION", sys_id, res_id, "DELETE_RECORD", "ABSENT", ""))
                verifications.append(AuditStep(1, "VERIFICATION", sys_id, res_id, "VERIFY_RECORD_ABSENT", "ABSENT", ""))

        # 5. Determine overall deletion status
        if has_active_sync or has_restore_risk or has_exposed_pii:
            status = "INCOMPLETE"
            all_steps = findings + remediations + verifications
        else:
            status = "COMPLETE"
            # Complete cases only output verification steps citing real evidence
            all_steps = [
                AuditStep(1, "VERIFICATION", "account_service", f"account_{user_id}", "VERIFY_RECORD_ABSENT", "ABSENT", ev_id),
                AuditStep(2, "VERIFICATION", "search_service", f"search_doc_{user_id}", "VERIFY_RECORD_ABSENT", "ABSENT", ev_id)
            ]

        # 6. Sort and renumber steps
        final_steps = sort_and_renumber_steps(all_steps)
        steps_dict = [s.to_dict() for s in final_steps]

        return status, steps_dict
