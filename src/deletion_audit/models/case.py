from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DeletionCase:
    case_id: str
    email: str
    requested_at: str
    reported_status: str
    reported_at: str
    audit_at: str
    request_text: str

@dataclass
class UserIdentity:
    user_id: str
    email: str
    phone: str
    email_hash: str
    name: str
    created_at: str
    historical_emails: List[str] = field(default_factory=list)
    historical_phones: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
