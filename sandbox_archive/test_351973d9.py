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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        factor = A[i][i]
        for j in range(n):
            A[i][j] /= factor
        for k in range(i+1, n):
            factor = A[k][i]
            for j in range(n):
                A[k][j] -= factor * A[i][j]

def matrix_multiplication(A, B):
    m, p, q = len(A), len(B), len(B[0])
    C = [[0 for _ in range(q)] for _ in range(m)]
    for i in range(m):
        for j in range(q):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def dpll(phi, assignment):
    if not phi:
        return True
    p = next((p for p in phi if isinstance(p, list)), None)
    if p is None:
        return False
    p_var, p_neg = p[0], ~p[0]
    if p_var in assignment:
        new_phi = [q for q in phi if q != p and not (isinstance(q, list) and q[0] == p_var)]
        return dpll(new_phi, assignment)
    else:
        assignment[p_var] = True
        if dpll(phi, assignment):
            return True
        del assignment[p_var]
        assignment[p_neg] = True
        if dpll(phi, assignment):
            return True
        del assignment[p_neg]
        return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = []
    for _ in range(n * (n - 1)):
        p = random.choice([random.randint(1, n), ~random.randint(1, n)])
        q = random.choice([random.randint(1, n), ~random.randint(1, n)])
        if [p, q] not in phi and [q, p] not in phi:
            phi.append([p, q])
    assignment = {}
    
    w_DPLL = 0
    if dpll(phi, assignment):
        w_DPLL = len(assignment)
    
    min_idx = sum(abs(p) for p in assignment.values())
    
    return {
        "metric_name": "min_idx",
        "metric_value": min_idx,
        "instances_tested": n * (n - 1),
        "n_max": n,
        "conjecture_holds": abs(min_idx - w_DPLL) / max(w_DPLL, 1) <= 0.1 and min_idx >= 0.9 * w_DPLL,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_idx = sum(r["metric_value"] for r in results) / len(results)
    std_idx = math.sqrt(sum((r["metric_value"] - mean_idx) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_idx} std={std_idx} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")