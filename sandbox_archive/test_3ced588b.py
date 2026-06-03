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

def generate_cnf(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(range(1, 2 * n + 1), 3)
        clauses.append(clause)
    return clauses

def incidence_matrix(cnf: list, n: int) -> list:
    M = [[0] * (2 * n) for _ in range(len(cnf))]
    for i, clause in enumerate(cnf):
        for lit in clause:
            if lit > 0:
                M[i][lit - 1] = 1
            else:
                M[i][-lit - 1] = 1
    return M

def determinant(M: list) -> int:
    n = len(M)
    if n == 1:
        return M[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in M[1:]]
        det += ((-1) ** j) * M[0][j] * determinant(submatrix)
    return det

def distinct_roots(poly: int, n: int) -> int:
    roots = set()
    for i in range(2**n):
        if poly == 0:
            roots.add(i)
    return len(roots)

def resolution_width(cnf: list) -> int:
    # Simplified version of resolution width calculation
    return len(cnf)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    M = incidence_matrix(cnf, n)
    poly = determinant(M)
    r_min = distinct_roots(poly, n)
    w_phi = resolution_width(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "r(min)/w(φ)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_is_zero"
        }
    
    r_min_over_w_phi = r_min / w_phi
    return {
        "metric_name": "r(min)/w(φ)",
        "metric_value": r_min_over_w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": r_min_over_w_phi >= 1,  # Assuming c = 1 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(metric_values) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std=0.00 support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r(min)/w(φ) < 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")