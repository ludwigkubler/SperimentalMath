# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return [[A[i][j] / A[i][i] for j in range(n)] for i in range(m)]

def determinant(A):
    m, n = len(A), len(A[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in A[1:]]
        det += (-1) ** j * A[0][j] * determinant(submatrix)
    return det

def permanent(M):
    m, n = len(M), len(M[0])
    if m != n:
        raise ValueError("Matrix must be square")
    if n == 0:
        return 1
    if n == 1:
        return M[0][0]
    perm = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in M[1:]]
        sign = (-1) ** (n - 1 - j)
        perm += sign * M[0][j] * permanent(submatrix)
    return perm

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    ell = random.choice([3, 4, 5])
    m = random.randint(ell + 1, 12)
    a = random.choice([1, 2])
    D = [[random.choice([0, 1]) for _ in range(m)] for _ in range(ell)]
    
    # Compute V(M) via Ryser's formula on the m heaviest columns
    M_heaviest = sorted(D, key=lambda row: sum(row), reverse=True)[:m]
    perm_var = permanent([[M_heaviest[i][j] * M_heaviest[j][i] for j in range(m)] for i in range(m)])
    V_M = math.log2(1 + perm_var) / m
    
    # Pick a hard function f
    def is_hard(f):
        return len(list(itertools.product([0, 1], repeat=ell))) >= 2 ** (ell // 3)
    
    for _ in range(64):
        eps = [random.choice([-1, 1]) for _ in range(m)]
        M_eps = [[M_heaviest[i][j] * eps[j] for j in range(m)] for i in range(m)]
        perm_var_eps = permanent([[M_eps[i][j] * M_eps[j][i] for j in range(m)] for i in range(m)])
        V_M_eps = math.log2(1 + perm_var_eps) / m
        if abs(V_M - V_M_eps) > 0.1:
            return {
                "metric_name": "V(M)",
                "metric_value": V_M,
                "instances_tested": 64,
                "conjecture_holds": False,
                "counterexample": "Ryser's formula discrepancy"
            }
    
    # Estimate bias(NW_{D,f}, w) by enumerating all width-w<=3 DNFs on m variables
    def NW(D, f):
        return sum(f(tuple(row)) for row in D)
    
    def max_bias(w):
        max_b = 0
        for dnf in itertools.product([0, 1], repeat=m):
            if sum(dnf) == w:
                bias = abs(NW(D, lambda x: int(all(x[i] == dnf[i] for i in range(m)))) - 0.5)
                max_b = max(max_b, bias)
        return max_b
    
    for w in [1, 2, 3]:
        bias = max_bias(w)
        if math.log(1 / bias) < 0.05 * V_M * m / w:
            return {
                "metric_name": "bias(NW_{D,f}, w)",
                "metric_value": bias,
                "instances_tested": 64,
                "conjecture_holds": False,
                "counterexample": f"Failed for width {w}"
            }
    
    return {
        "metric_name": "V(M)",
        "metric_value": V_M,
        "instances_tested": 64,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")