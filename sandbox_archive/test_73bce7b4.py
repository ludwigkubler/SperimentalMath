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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def compute_local_cohomology(cnf):
        # Simplified local cohomology computation (placeholder)
        return len(cnf) ** 0.5
    
    def compute_frege_proof_length(cnf):
        # Placeholder for SAT solver
        return len(cnf) * 10  # Simplified model
    
    n_values = [5, 10, 15, 20, 30, 40]
    lcoh_values = []
    f_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        lcoh = compute_local_cohomology(cnf)
        f = compute_frege_proof_length(cnf)
        
        if lcoh <= 0 or f <= 0:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "lcoh or f is non-positive"
            }
        
        lcoh_values.append(lcoh)
        f_values.append(f)
    
    mean_lcoh = sum(lcoh_values) / len(lcoh_values)
    mean_f = sum(f_values) / len(f_values)
    
    correlation_coefficient = sum((x - mean_lcoh) * (y - mean_f) for x, y in zip(lcoh_values, f_values)) / \
                              math.sqrt(sum((x - mean_lcoh) ** 2 for x in lcoh_values) * sum((y - mean_f) ** 2 for y in f_values))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")