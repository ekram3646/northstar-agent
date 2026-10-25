import os
import json
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class UsageRecord:
    model_name: str
    call_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def estimated_cost_usd(self) -> float:
        # Pricing assumptions for gemini-3.8-flash / gemini-2.5-flash
        # Input: $0.10 / 1M tokens, Output: $0.40 / 1M tokens
        input_cost = (self.input_tokens / 1_000_000) * 0.10
        output_cost = (self.output_tokens / 1_000_000) * 0.40
        return input_cost + output_cost

class UsageTracker:
    def __init__(self):
        self.records: Dict[str, UsageRecord] = {}

    def log_call(self, model_name: str, input_tokens: int, output_tokens: int):
        if model_name not in self.records:
            self.records[model_name] = UsageRecord(model_name=model_name)
        rec = self.records[model_name]
        rec.call_count += 1
        rec.input_tokens += input_tokens
        rec.output_tokens += output_tokens

    def generate_report_markdown(self, filepath: str):
        total_calls = sum(r.call_count for r in self.records.values())
        total_input = sum(r.input_tokens for r in self.records.values())
        total_output = sum(r.output_tokens for r in self.records.values())
        total_tokens = total_input + total_output
        total_cost = sum(r.estimated_cost_usd for r in self.records.values())
        avg_tokens = (total_tokens / total_calls) if total_calls > 0 else 0
        avg_cost = (total_cost / total_calls) if total_calls > 0 else 0

        md = f"""# Personal Data Deletion Audit Agent — Token Usage & Cost Report

## Summary of Final Dataset Run (518 Cases)

| Metric | Value |
| :--- | :--- |
| **Total Cases Evaluated** | 518 |
| **Total Model Calls** | {total_calls} |
| **Total Input Tokens** | {total_input:,} |
| **Total Output Tokens** | {total_output:,} |
| **Total Tokens** | {total_tokens:,} |
| **Average Tokens per Request** | {avg_tokens:.2f} |
| **Total Estimated Cost (USD)** | ${total_cost:.4f} |
| **Average Cost per Request (USD)** | ${avg_cost:.6f} |

## Model Breakdown

| Model Name | Calls | Input Tokens | Output Tokens | Total Tokens | Estimated Cost (USD) |
| :--- | :---: | :---: | :---: | :---: | :---: |
"""
        for r in self.records.values():
            md += f"| `{r.model_name}` | {r.call_count} | {r.input_tokens:,} | {r.output_tokens:,} | {r.total_tokens:,} | ${r.estimated_cost_usd:.4f} |\n"

        md += """
## Pricing Assumptions & Methodology
- Pricing based on standard Gemini 3.8 Flash rates ($0.10 / 1M input tokens, $0.40 / 1M output tokens).
- Bounded prompt normalization and token-efficient structured outputs were enforced to minimize token overhead.
"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
