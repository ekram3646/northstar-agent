from typing import List
from ..models.evidence import SystemActivityRecord

class TimelineReconstructor:
    def get_activities_before_audit(self, records: List[SystemActivityRecord], user_id: str, audit_at: str) -> List[SystemActivityRecord]:
        user_records = [r for r in records if r.user_id == user_id]
        # Filter records up to audit_at
        valid_records = []
        for r in user_records:
            if r.timestamp <= audit_at:
                valid_records.append(r)
        # Sort by timestamp ascending
        valid_records.sort(key=lambda x: x.timestamp)
        return valid_records
