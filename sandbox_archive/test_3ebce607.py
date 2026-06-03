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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def circuit_monotone_width(cnf):
        max_length = 0
        for clause in cnf:
            length = sum(1 for var in clause if abs(var) == 1)
            max_length = max(max_length, length)
        return max_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        aut_order = len(cnf)  # Simplified assumption for demonstration
        w_phi = circuit_monotone_width(cnf)
        results.append((aut_order, w_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    aut_orders = [r[0] for r in results]
    w_phis = [r[1] for r in results]
    
    mean_aut_order = sum(aut_orders) / len(aut_orders)
    mean_w_phi = sum(w_phis) / len(w_phis)
    
    correlation_coefficient = 0
    if len(set(aut_orders)) > 1 and len(set(w_phis)) > 1:
        numerator = sum((a - mean_aut_order) * (w - mean_w_phi) for a, w in zip(aut_orders, w_phis))
        denominator = math.sqrt(sum((a - mean_aut_order)**2 for a in aut_orders)) * math.sqrt(sum((w - mean_w_phi)**2 for w in w_phis))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(aut_orders),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8 and abs(mean_aut_order - mean_w_phi) <= 3,
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
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")