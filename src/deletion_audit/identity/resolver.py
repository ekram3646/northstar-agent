import hashlib
from typing import Dict, List, Optional
from ..models.case import DeletionCase, UserIdentity

def compute_sha256(val: str) -> str:
    return hashlib.sha256(val.lower().strip().encode("utf-8")).hexdigest()

class IdentityResolver:
    def __init__(self, identities: Dict[str, UserIdentity], audit_logs: List[Dict[str, str]]):
        self.identities = identities
        self.audit_logs = audit_logs

    def resolve(self, case: DeletionCase) -> UserIdentity:
        target_email = case.email.lower().strip()
        matched_user: Optional[UserIdentity] = None

        # 1. Direct match on current email
        for user_id, identity in self.identities.items():
            if identity.email.lower().strip() == target_email:
                matched_user = identity
                break

        # 2. Check historical email changes in audit log if not found
        if not matched_user:
            for log in self.audit_logs:
                old_val = log.get("old_value", "").lower().strip()
                new_val = log.get("new_value", "").lower().strip()
                if old_val == target_email or new_val == target_email:
                    uid = log.get("user_id", "")
                    if uid in self.identities:
                        matched_user = self.identities[uid]
                        break

        # 3. Fallback: synthetic identity if unknown user ID
        if not matched_user:
            user_id_gen = f"user_resolved_{abs(hash(case.email)) % 100000}"
            matched_user = UserIdentity(
                user_id=user_id_gen,
                email=case.email,
                phone="",
                email_hash=compute_sha256(case.email),
                name="Unknown Customer",
                created_at=case.requested_at
            )

        # Collect all historical emails for matched user from audit logs
        historical = set()
        for log in self.audit_logs:
            if log.get("user_id") == matched_user.user_id:
                if log.get("old_value"):
                    historical.add(log.get("old_value").strip())
                if log.get("new_value"):
                    historical.add(log.get("new_value").strip())

        matched_user.historical_emails = list(historical)
        return matched_user
