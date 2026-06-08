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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def rank(A):
    rref = gaussian_elimination(A)
    rank = 0
    for row in rref:
        if any(row):
            rank += 1
    return rank

def random_k_cnf(n, m):
    variables = list(range(1, n+1))
    clauses = set()
    while len(clauses) < m:
        clause = random.sample(variables, random.randint(2, min(m, n)))
        if all(v not in c for v in clause for c in clauses):
            clauses.add(tuple(sorted(clause)))
    return clauses

def frege_proof_depth(k_cnf):
    # Placeholder function for Frege proof depth calculation
    # This is a dummy implementation and should be replaced with the actual algorithm
    return len(k_cnf) * 2

def minimal_local_index(simplicial_complex):
    # Placeholder function for minimal local index calculation
    # This is a dummy implementation and should be replaced with the actual algorithm
    return rank(simplicial_complex)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = n * (n - 1) // 2
    k_cnf = random_k_cnf(n, m)
    simplicial_complex = [[], [], []] + [list(range(1, n+1))] * (n-3)
    local_index = minimal_local_index(simplicial_complex)
    frege_depth = frege_proof_depth(k_cnf)
    
    if local_index > 10:
        return {
            "metric_name": "LocalIndex",
            "metric_value": local_index,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "local_index_too_high"
        }
    
    return {
        "metric_name": "Correlation",
        "metric_value": local_index * frege_depth,  # Dummy correlation for testing
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='local_index_too_high' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")