from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class SystemActivityRecord:
    activity_id: str
    system_id: str
    resource_id: str
    activity_type: str
    user_id: str
    status: str
    timestamp: str
    details: str

@dataclass
class EvidenceFile:
    file_id: str
    system_id: str
    file_path: str
    file_type: str
    created_at: str
    description: str

@dataclass
class DeletionRule:
    category: str
    system_id: str
    required_treatment: str
    allowed_identifiers: str
    retention_period_days: int
