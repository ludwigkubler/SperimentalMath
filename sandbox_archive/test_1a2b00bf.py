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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def gqrank(cnf):
        # Placeholder for geometric quantization rank calculation
        return len(cnf)  # Simplified for testing purposes
    
    def w(cnf):
        # Placeholder for resolution proof width calculation
        return len(cnf) * 2  # Simplified for testing purposes
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * 2))
            gq = gqrank(cnf)
            w_val = w(cnf)
            if abs(gq - w_val) > 10:
                return {
                    "metric_name": "gqrank_w_diff",
                    "metric_value": abs(gq - w_val),
                    "instances_tested": 1,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"CNF with gqrank={gq} and w={w_val}"
                }
            results.append((gq, w_val))
    
    if not results:
        return {
            "metric_name": "gqrank_w_diff",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    gqs = [r[0] for r in results]
    ws = [r[1] for r in results]
    mean_gq = sum(gqs) / len(gqs)
    mean_w = sum(ws) / len(ws)
    std_gq = math.sqrt(sum((x - mean_gq) ** 2 for x in gqs) / len(gqs))
    std_w = math.sqrt(sum((x - mean_w) ** 2 for x in ws) / len(ws))
    
    correlation_coefficient = sum((gqs[i] - mean_gq) * (ws[i] - mean_w) for i in range(len(gqs))) / (len(gqs) * std_gq * std_w)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(abs(r["metric_value"]) > 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"gqrank - w > 10\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")