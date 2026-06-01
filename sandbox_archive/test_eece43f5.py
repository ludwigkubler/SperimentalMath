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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_clause_set_complexity(clauses):
        # Simplified complexity measure
        return len(set(tuple(sorted(c)) for c in clauses))
    
    def compute_minimal_geometric_entropy(clauses):
        # Simplified entropy measure
        return sum(math.log2(len(c)) for c in clauses) / len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n, 2 * n)
            clauses = generate_cnf(n, m)
            c_phi = compute_clause_set_complexity(clauses)
            mge_phi = compute_minimal_geometric_entropy(clauses)
            results.append((n, m, c_phi, mge_phi))
    
    if not results:
        return {
            "metric_name": "minimal_geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _, _, _ in results)
    instances_tested = len(results)
    
    c_values = [c_phi for _, _, c_phi, _ in results]
    mge_values = [mge_phi for _, _, _, mge_phi in results]
    
    mean_c = sum(c_values) / instances_tested
    mean_mge = sum(mge_values) / instances_tested
    
    correlation_coefficient = 0
    if len(set(c_values)) > 1 and len(set(mge_values)) > 1:
        numerator = sum((c - mean_c) * (mge - mean_mge) for c, mge in zip(c_values, mge_values))
        denominator = math.sqrt(sum((c - mean_c) ** 2 for c in c_values)) * math.sqrt(sum((mge - mean_mge) ** 2 for mge in mge_values))
        correlation_coefficient = numerator / denominator
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "minimal_geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")