# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_2cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(literals)
        return clauses
    
    def ehrhart_quotient(clauses):
        # Placeholder implementation of Ehrhart quotient
        # This is a dummy value for testing purposes
        return len(clauses) / n
    
    def frege_proof_depth(clauses):
        # Placeholder implementation of Frege proof depth
        # This is a dummy value for testing purposes
        return len(clauses)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_2cnf(n)
            q = ehrhart_quotient(clauses)
            d = frege_proof_depth(clauses)
            results.append((q, d))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_values = [q for q, d in results]
    d_values = [d for q, d in results]
    
    mean_n = sum(n_values) / len(n_values)
    mean_d = sum(d_values) / len(d_values)
    
    covariance = sum((n - mean_n) * (d - mean_d) for n, d in results) / len(results)
    variance_n = sum((n - mean_n) ** 2 for n in n_values) / len(n_values)
    variance_d = sum((d - mean_d) ** 2 for d in d_values) / len(d_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_n) * math.sqrt(variance_d))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient > 0.7 and p_value < 0.05,
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")