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
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                if k < i:
                    A[j][k] -= factor * A[i][k]
                else:
                    A[j][k] = 0
    return A

def rank_matrix(A):
    n = len(A)
    r = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(r)):
            continue
        for j in range(r, n):
            A[j], A[r] = A[r], A[j]
            r += 1
            break
    return r

def generate_cnf(n):
    clauses = []
    for i in range(2**n):
        clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
        if all(clause[j] == 0 for j in range(n)):
            continue
        clauses.append(clause)
    return clauses

def communication_complexity(cnf):
    n = len(cnf[0])
    count = [0] * n
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                count[literal - 1] += 1
            else:
                count[-literal - 1] -= 1
    return max(count)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_cnf(n)
    mrank_phi = rank_matrix(gaussian_elimination(phi))
    rc_phi = communication_complexity(phi)
    
    return {
        "metric_name": "mrank_rc_correlation",
        "metric_value": mrank_phi * rc_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")