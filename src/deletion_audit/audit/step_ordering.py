from typing import List
from ..models.audit_step import AuditStep, PHASE_ORDER, OPERATION_ORDER

def sort_and_renumber_steps(steps: List[AuditStep]) -> List[AuditStep]:
    if not steps:
        return []

    # Sort steps according to strict spec key
    def get_key(s: AuditStep):
        p_idx = PHASE_ORDER.get(s.phase, 99)
        op_map = OPERATION_ORDER.get(s.phase, {})
        o_idx = op_map.get(s.operation, 99)
        return (p_idx, o_idx, s.system_id, s.resource_id)

    sorted_steps = sorted(steps, key=get_key)

    # Renumber consecutively starting from 1
    renumbered = []
    for idx, s in enumerate(sorted_steps, start=1):
        renumbered.append(AuditStep(
            step_no=idx,
            phase=s.phase,
            system_id=s.system_id,
            resource_id=s.resource_id,
            operation=s.operation,
            state=s.state,
            evidence_id=s.evidence_id
        ))

    return renumbered
