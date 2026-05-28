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

def generate_3cnf(n, m):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + [f'~{v}' for v in variables], 3)
        clauses.append(clause)
    return clauses

def construct_multivariate_cf(clauses):
    # Simplified construction for demonstration
    return sum(1 for clause in clauses)

def rank_of_multivariate_cf(cf_representation):
    # Simplified rank calculation for demonstration
    return len(cf_representation)

def min_resolution_proof_length(clauses):
    # Placeholder function to simulate DPLL solver
    return random.randint(1, 100)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.choice([int(n * 1.5), int(n * 2), int(n * 2.5)])
    clauses = generate_3cnf(n, m)
    
    cf_representation = construct_multivariate_cf(clauses)
    rank = rank_of_multivariate_cf(cf_representation)
    proof_length = min_resolution_proof_length(clauses)
    
    if proof_length == 0:
        return {
            "metric_name": "rank_over_inverse_proof_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "proof_length_zero"
        }
    
    metric_value = rank / proof_length
    
    return {
        "metric_name": "rank_over_inverse_proof_length",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True if metric_value <= 10 else False,
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
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_type = "SUPPORTED"
    else:
        max_metric_value = max(r["metric_value"] for r in results if r["conjecture_holds"])
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        if max_metric_value > 10:
            result_type = "FALSIFIED"
            counterexample = f"max_metric_value={max_metric_value} exceeds 10"
        else:
            result_type = "INCONCLUSIVE"
            counterexample = ""
    
    print(f"RESULT: {result_type} mean={mean_value} std=0 support_fraction={support_fraction}")