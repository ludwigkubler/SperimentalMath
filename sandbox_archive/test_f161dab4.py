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
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, n):
            A[i][j] /= pivot
        for j in range(n):
            if j != i and A[j][i] != 0:
                factor = A[j][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiplication(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = [[Fraction(0) for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def distillable_entropy(state):
    n = len(state)
    v = [Fraction(1, n)] * n
    Av = matrix_multiplication(state, v)
    max_eigenvalue = 0
    for i in range(n):
        max_eigenvalue = max(max_eigenvalue, abs(Av[i][i]))
    epsilon = math.log2(max_eigenvalue)
    return epsilon

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    state = [[Fraction(random.random()) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        state[i][i] += Fraction(1 - sum(state[i]))
    
    epsilon = distillable_entropy(state)
    if epsilon <= 0:
        return {
            "metric_name": "distillable_entropy",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "epsilon_non_positive"
        }
    
    tau = len([i for i in range(n) if state[i][i] != Fraction(0)])
    metric_value = tau
    instances_tested = 1
    conjecture_holds = tau >= Fraction(1, 2) * math.log2(1 / epsilon)
    counterexample = "" if conjecture_holds else f"tau={tau} < c * log(1/epsilon)"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_d = math.sqrt(sum((r["metric_value"] - mean_d)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "epsilon_non_positive" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] == "epsilon_non_positive")
        print(f"RESULT: FALSIFIED counterexample=\"epsilon_non_positive\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.95")