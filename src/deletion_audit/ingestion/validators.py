from typing import List
from ..models.case import DeletionCase

class DatasetValidationError(Exception):
    pass

def validate_cases(cases: List[DeletionCase]) -> None:
    if not cases:
        raise DatasetValidationError("No cases loaded.")
    seen_ids = set()
    for c in cases:
        if not c.case_id:
            raise DatasetValidationError(f"Missing case_id in case: {c}")
        if c.case_id in seen_ids:
            raise DatasetValidationError(f"Duplicate case_id found: {c.case_id}")
        seen_ids.add(c.case_id)
