# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                if factor == 0:
                    continue
                A[j][k] -= factor * A[i][k]
    return A

def tropical_order(matroid):
    n = len(matroid)
    submat = [row[:n] for row in matroid]
    rank = sum(1 for row in gaussian_elimination(submat) if any(row))
    return rank

def random_cnf(n, m):
    variables = set(range(1, n+1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        m = n * 2
        cnf = random_cnf(n, m)
        matroid = [[int(abs(c) == i+1) for c in clause] for clause in cnf]
        mto_phi = tropical_order(matroid)
        c_phi = len(cnf)
        results.append((mto_phi, c_phi))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    mto_values, c_phi_values = zip(*results)
    n_max = max(len(mto_values), len(c_phi_values))
    mean_mto = sum(mto_values) / len(mto_values)
    mean_c_phi = sum(c_phi_values) / len(c_phi_values)
    correlation_coefficient = (sum((mto - mean_mto) * (c - mean_c_phi) for mto, c in zip(mto_values, c_phi_values)) /
                               (len(results) * (sum((mto - mean_mto)**2 for mto in mto_values) / len(mto_values))**0.5 *
                                sum((c - mean_c_phi)**2 for c in c_phi_values) / len(c_phi_values))**0.5)
    mean_abs_diff = sum(abs(mto - c) for mto, c in zip(mto_values, c_phi_values)) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")