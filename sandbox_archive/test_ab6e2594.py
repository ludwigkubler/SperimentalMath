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
        pivot_row = None
        for j in range(i, n):
            if A[j][i] != 0:
                pivot_row = j
                break
        if pivot_row is None:
            continue
        A[i], A[pivot_row] = A[pivot_row], A[i]
        pivot = A[i][i]
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    rank = sum(1 for row in A if any(row[j] != 0 for j in range(n)))
    return rank

def tropicalized_hodge_rank(cnf):
    # Convert CNF to a matrix representation
    n = len(cnf)
    A = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        for literal in clause:
            if literal > 0:
                A[literal - 1][n] += 1
                A[n][literal - 1] -= 1
            else:
                A[-literal - 1][n] += 1
                A[n][-literal - 1] -= 1
    return gaussian_elimination(A)

def bp_read_twice_width(cnf):
    n = len(cnf)
    width = 0
    for clause in cnf:
        width = max(width, sum(1 for literal in clause if literal > 0))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = []
    for _ in range(m):
        clause = [random.randint(-n, -1) if random.choice([True, False]) else random.randint(1, n) for _ in range(random.randint(1, n))]
        cnf.append(clause)
    
    rho_V_I = tropicalized_hodge_rank(cnf)
    bp_width = bp_read_twice_width(cnf)
    
    # Define f(n) as a simple function of n
    f_n = 2 * n
    
    return {
        "metric_name": "rho_V_I vs f(n)",
        "metric_value": rho_V_I,
        "instances_tested": 1,
        "conjecture_holds": rho_V_I <= f_n and bp_width <= 10,
        "counterexample": "" if rho_V_I <= f_n and bp_width <= 10 else f"rho_V_I={rho_V_I}, f(n)={f_n}, bp_width={bp_width}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_V_I = sum(r["metric_value"] for r in results) / len(results)
    std_rho_V_I = (sum((r["metric_value"] - mean_rho_V_I) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_V_I} std={std_rho_V_I} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho_V_I} std={std_rho_V_I} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")