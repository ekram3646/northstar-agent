from typing import List, Dict, Any, Tuple

def calculate_case_accuracy(predictions: List[Tuple[str, str]], canonical: List[Tuple[str, str]]) -> float:
    if not canonical:
        return 0.0
    canon_map = dict(canonical)
    correct = 0
    total = len(canonical)
    for case_id, pred_status in predictions:
        if case_id in canon_map:
            if canon_map[case_id] == pred_status:
                correct += 1
    return (correct / total) * 100.0 if total > 0 else 100.0

def calculate_step_metrics(pred_steps: List[Dict[str, Any]], canon_steps: List[Dict[str, Any]]) -> Dict[str, float]:
    if not canon_steps and not pred_steps:
        return {"precision": 100.0, "recall": 100.0, "f1": 100.0}
    if not canon_steps or not pred_steps:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    # Match by (phase, system_id, resource_id, operation)
    canon_tuples = set((s["phase"], s["system_id"], s["resource_id"], s["operation"]) for s in canon_steps)
    pred_tuples = set((s["phase"], s["system_id"], s["resource_id"], s["operation"]) for s in pred_steps)

    tp = len(pred_tuples.intersection(canon_tuples))
    fp = len(pred_tuples - canon_tuples)
    fn = len(canon_tuples - pred_tuples)

    prec = (tp / (tp + fp)) * 100.0 if (tp + fp) > 0 else 0.0
    rec = (tp / (tp + fn)) * 100.0 if (tp + fn) > 0 else 0.0
    f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

    return {"precision": prec, "recall": rec, "f1": f1}
