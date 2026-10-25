import os
import sqlite3
from typing import List, Dict, Any

class SqliteExtractor:
    def extract_records(self, db_path: str, user_id: str) -> List[Dict[str, Any]]:
        results = []
        if not os.path.exists(db_path):
            return results
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            
            # Query user_records table
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_records'")
            if cur.fetchone():
                cur.execute("SELECT * FROM user_records WHERE user_id=?", (user_id,))
                rows = cur.fetchall()
                for r in rows:
                    results.append(dict(r))
            conn.close()
        except Exception:
            pass
        return results
