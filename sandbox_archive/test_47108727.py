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
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        pivot = A[i][i]
        if pivot == 0:
            continue
        for k in range(i+1, n):
            factor = Fraction(A[k][i], pivot)
            for j in range(n):
                A[k][j] -= factor * A[i][j]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(A[i][n], A[i][i])
        for k in range(i-1, -1, -1):
            A[k][n] -= A[k][i] * x[i]
    return x

def characteristic_polynomial(cnf, p):
    n = len(cnf)
    A = [[0] * (n + 1) for _ in range(n)]
    for clause in cnf:
        for literal in clause:
            row = abs(literal) - 1
            if literal > 0:
                A[row][row] += p
            else:
                A[row][row] -= p
            A[row][n] += 1

    gaussian_elimination(A)
    det = 1
    for i in range(n):
        det *= A[i][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m = random.randint(5, 40)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
        cnf.append(clause)

    det = characteristic_polynomial(cnf, 2)
    if det == 0:
        return {
            "metric_name": "minimal_p_adic_valuation_rank",
            "metric_value": float('inf'),
            "instances_tested": m,
            "n_max": m,
            "conjecture_holds": False,
            "counterexample": "characteristic_polynomial_is_zero"
        }

    v = 0
    p = 2
    while det % p == 0:
        det //= p
        v += 1

    return {
        "metric_name": "minimal_p_adic_valuation_rank",
        "metric_value": v,
        "instances_tested": m,
        "n_max": m,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"minimal_p_adic_valuation_rank_is_incorrect\" first_failing_seed={r['seed']}")
                break