# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(circuit):
        # Placeholder function; replace with actual algorithm
        return len(circuit)
    
    def hodge_norm(circuit):
        # Placeholder function; replace with actual Hodge norm calculation
        return sum(circuit) / len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        rank = communication_complexity_rank(circuit)
        norm = hodge_norm(circuit)
        results.append({
            "n": n,
            "rank": rank,
            "norm": norm
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(r["n"] for r in results)
    instances_tested = len(results)
    metric_values = [math.log(r["norm"]) for r in results]
    ranks = [r["rank"] for r in results]
    
    if not all(isinstance(v, (int, float)) for v in metric_values + ranks):
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "non_numeric_result"
        }
    
    if n_max < 16:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "n_too_small"
        }
    
    correlation_coefficient = sum((m - mean_m) * (r - mean_r) for m, r in zip(metric_values, ranks)) / \
                              math.sqrt(sum((m - mean_m)**2 for m in metric_values) * sum((r - mean_r)**2 for r in ranks))
    mean_m = sum(metric_values) / instances_tested
    mean_r = sum(ranks) / instances_tested
    
    conjecture_holds = correlation_coefficient > 0.9
    counterexample = "" if conjecture_holds else "correlation_too_low"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all(isinstance(r, dict) for r in results):
        print("RESULT: INCONCLUSIVE reason=non_dict_result")
        sys.exit(0)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(r["counterexample"] == "correlation_too_low" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] == "correlation_too_low"), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")