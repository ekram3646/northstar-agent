import json
import os
from typing import List, Dict, Any

class JsonExtractor:
    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    return data.get("logs", [data])
        except Exception:
            return []
        return []
