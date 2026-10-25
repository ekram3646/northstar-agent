from typing import Dict, List, Tuple
from ..models.evidence import DeletionRule, SystemActivityRecord

class PolicyEngine:
    def __init__(self, rules: Dict[str, DeletionRule]):
        self.rules = rules

    def evaluate_treatment(self, system_id: str, current_state: str) -> Tuple[bool, str]:
        # Find rule matching system_id
        matched_rule = None
        for rule in self.rules.values():
            if rule.system_id == system_id:
                matched_rule = rule
                break

        if not matched_rule:
            return True, "DELETE_RECORD"

        req = matched_rule.required_treatment
        if req == "DELETE_RECORD" and current_state == "ABSENT":
            return True, req
        elif req in ["REDACT_RECORD", "ANONYMIZE_RECORD"] and current_state in ["REDACTED", "ANONYMIZED", "ABSENT"]:
            return True, req
        elif req == "VERIFY_RECORD_PRESENT" and current_state == "PRESENT":
            return True, req

        return False, req
