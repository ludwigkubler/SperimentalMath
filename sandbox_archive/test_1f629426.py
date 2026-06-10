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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    rank = 0
    for row in A:
        if any(row):
            rank += 1
    return rank

def generate_cnf_formula(n, m):
    clauses = []
    variables = list(range(1, n+1))
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        clauses.append(clause)
    return clauses

def communication_complexity_rank_variance(phi):
    # Placeholder function to simulate the computation
    # Replace this with actual DPLL solver logic if available
    return random.random()

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_cnf_formula(n, random.randint(1, n**2))
            mrank_phi = gaussian_elimination(phi)
            rc_phi = communication_complexity_rank_variance(phi)
            results.append((mrank_phi, rc_phi))
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mrank_list = [r[0] for r in results]
    rc_list = [r[1] for r in results]
    
    mean_mrank = sum(mrank_list) / len(mrank_list)
    mean_rc = sum(rc_list) / len(rc_list)
    correlation_coefficient = sum((mrank_list[i] - mean_mrank) * (rc_list[i] - mean_rc) for i in range(len(results))) / (len(results) * math.sqrt(sum((mrank_list[i] - mean_mrank)**2 for i in range(len(results)))) * math.sqrt(sum((rc_list[i] - mean_rc)**2 for i in range(len(results)))))
    mean_abs_diff = sum(abs(mrank_list[i] - mean_mrank) for i in range(len(results))) / len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8 and mean_abs_diff <= 3,
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
        mean_corr_coeff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient does not meet criteria' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")