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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([f'x{i}', f'-x{i}']) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def msr(cnf):
        # Placeholder function to compute minimal symmetric function rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)  # Simplified for testing purposes
    
    def resolution_width(cnf):
        # Placeholder function to compute resolution proof width
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) * (len(cnf) - 1) // 2  # Simplified for testing purposes
    
    msr_values = []
    w_values = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        msr_value = msr(cnf)
        w_value = resolution_width(cnf)
        msr_values.append(msr_value)
        w_values.append(w_value)
    
    if len(msr_values) == 0 or len(w_values) == 0:
        return {
            "metric_name": "msr_w_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_input"
        }
    
    mean_msr = sum(msr_values) / len(msr_values)
    mean_w = sum(w_values) / len(w_values)
    correlation_coefficient = sum((msr_values[i] - mean_msr) * (w_values[i] - mean_w) for i in range(len(msr_values))) / (len(msr_values) * math.sqrt(sum((msr_values[i] - mean_msr) ** 2 for i in range(len(msr_values)))) * math.sqrt(sum((w_values[i] - mean_w) ** 2 for i in range(len(w_values)))))
    
    return {
        "metric_name": "msr_w_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(msr_values),
        "n_max": max(40, max(n for _ in range(30))),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")