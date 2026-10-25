from typing import List, Dict, Any
from .extractors.json_extractor import JsonExtractor
from .extractors.sqlite_extractor import SqliteExtractor

class EvidenceRegistry:
    def __init__(self):
        self.json_extractor = JsonExtractor()
        self.sqlite_extractor = SqliteExtractor()

    def query_evidence(self, manifest: List[Any], user_id: str) -> List[Dict[str, Any]]:
        extracted = []
        for file in manifest:
            path = file.file_path
            if file.file_type == "json":
                records = self.json_extractor.extract(path)
                for r in records:
                    if r.get("user_id") == user_id:
                        r["source_file_id"] = file.file_id
                        extracted.append(r)
            elif file.file_type == "sqlite":
                records = self.sqlite_extractor.extract_records(path, user_id)
                for r in records:
                    r["source_file_id"] = file.file_id
                    extracted.append(r)
        return extracted
