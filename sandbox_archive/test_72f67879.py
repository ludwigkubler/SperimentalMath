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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        factor = Fraction(A[i][i], A[i][i])
        for k in range(i+1, n):
            factor_k = Fraction(A[k][i], A[i][i])
            for j in range(i, n):
                A[k][j] -= factor_k * A[i][j]
            b[k] -= factor_k * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        sum_j = 0
        for j in range(i+1, n):
            sum_j += A[i][j] * x[j]
        x[i] = Fraction(b[i] - sum_j, A[i][i])
    
    return x

def communication_complexity(f, G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    b = [0] * n
    
    for i in range(n):
        for j in range(n):
            if f((G[i], G[j])) == 1:
                A[i][j] += 1
                b[i] += 1
    
    x = gaussian_elimination(A, b)
    
    return sum(abs(xi) for xi in x)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    G = list(range(n))
    
    def f(g):
        i, j = g
        return (i > j) == (random.random() < 0.5)
    
    metric_value = communication_complexity(f, G)
    instances_tested = n * (n - 1) // 2
    
    if metric_value >= 1 / (log(n)):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Graph with n={n}, A=[{', '.join(map(str, A[0]))}]"
    
    return {
        "metric_name": "communication_complexity",
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
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{result['counterexample']}' first_failing_seed={first_failing_seed}")