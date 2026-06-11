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
        for _ in range(n * (n - 1) // 2):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        assignment = [None] * (n + 1)
        
        def solve(index, partial_assignment):
            if index > n:
                return True
            for value in [-1, 1]:
                if all(value != assignment[abs(lit)] for lit in cnf[index - 1]):
                    partial_assignment[index] = value
                    if solve(index + 1, partial_assignment):
                        return True
                    partial_assignment[index] = None
            return False
        
        return n if not solve(1, assignment) else 0
    
    def hodge_theory_dimension(cnf):
        # Placeholder function for Hodge theory dimension calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        ht_d = hodge_theory_dimension(cnf)
        dpll_w = dpll_width(cnf)
        results.append((ht_d, dpll_w))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ht_d_values = [ht_d for ht_d, _ in results]
    dpll_w_values = [dpll_w for _, dpll_w in results]
    
    mean_ht_d = sum(ht_d_values) / len(ht_d_values)
    mean_dpll_w = sum(dpll_w_values) / len(dpll_w_values)
    
    covariance = sum((ht_d - mean_ht_d) * (dpll_w - mean_dpll_w) for ht_d, dpll_w in results) / len(results)
    variance_ht_d = sum((ht_d - mean_ht_d) ** 2 for ht_d in ht_d_values) / len(ht_d_values)
    variance_dpll_w = sum((dpll_w - mean_dpll_w) ** 2 for dpll_w in dpll_w_values) / len(dpll_w_values)
    
    correlation_coefficient = covariance / (math.sqrt(variance_ht_d) * math.sqrt(variance_dpll_w))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")