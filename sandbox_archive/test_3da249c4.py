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

# Generate a random CNF with n variables and m clauses
def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        clauses.append(clause)
    return clauses

# Convert CNF to matrix A(φ)
def matrix_A(phi):
    n = max(abs(lit) for cl in phi for lit in cl)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for cl in phi:
        for lit in cl:
            i, j = abs(lit), -lit if lit < 0 else lit
            A[i][j] = 1
    return A

# Compute the local induction ring rank LIR(K)
def lir_rank(n):
    # Placeholder for actual LIR computation
    return n  # Simplified example, replace with actual method

# Compute the communication complexity rank of matrix A(φ)
def comm_complexity_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    for i in range(m):
        if any(A[i][j] != 0 for j in range(n)):
            rank += 1
    return rank

# Compute the variance of a list of numbers
def variance(values):
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)

# Run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(instances_tested // (n - 4)):
            phi = generate_cnf(n, random.randint(2 * n, 3 * n))
            A_phi = matrix_A(phi)
            LIR_K = lir_rank(n)
            rank = comm_complexity_rank(A_phi)
            metric_values.append(rank)
    
    if not metric_values:
        return {
            "metric_name": "communication complexity rank",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(variance(metric_values))
    c = std_dev / LIR_K
    
    return {
        "metric_name": "communication complexity rank",
        "metric_value": mean,
        "instances_tested": instances_tested * (n_max - 4),
        "n_max": n_max,
        "conjecture_holds": all(x <= c * LIR_K for x in metric_values),
        "counterexample": "" if all(x <= c * LIR_K for x in metric_values) else "variance exceeds bound"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"variance exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")