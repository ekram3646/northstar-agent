import os
import json
import urllib.request
from typing import Dict, Any, Tuple
from .usage_tracker import UsageTracker

class AIProvider:
    def __init__(self, tracker: UsageTracker, api_key: str = "", model_name: str = "gemini-3.8-flash"):
        self.tracker = tracker
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name

    def audit_with_ai(self, prompt: str, case_id: str) -> Tuple[str, Dict[str, Any]]:
        # Estimate prompt tokens
        input_tokens = len(prompt) // 4
        
        if not self.api_key:
            # Deterministic offline fallback
            output_tokens = 150
            self.tracker.log_call(self.model_name, input_tokens, output_tokens)
            return "DETERMINISTIC_FALLBACK", {"status": "OK"}

        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"}
            }
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                out_tokens = len(text) // 4
                self.tracker.log_call(self.model_name, input_tokens, out_tokens)
                return "SUCCESS", json.loads(text)
        except Exception as e:
            self.tracker.log_call(self.model_name, input_tokens, 100)
            return f"ERROR: {str(e)}", {"status": "FALLBACK"}
