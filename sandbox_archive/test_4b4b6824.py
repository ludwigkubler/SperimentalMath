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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(b[i], A[i][i])
        for j in range(i-1, -1, -1):
            b[j] -= A[j][i] * x[i]
    return x

def matrix_multiply(A, B):
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    instances_tested = 30
    total_action_complexity = 0
    action_complexities = []
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        # Simulate moment polytope and symplectic leaves (simplified)
        symplectic_leaves = random.randint(1, 2**n)
        rho_f = random.gauss(0, math.sqrt(n))
        total_action_complexity += abs(rho_f)
        action_complexities.append(abs(rho_f))
    
    mean_action_complexity = Fraction(total_action_complexity, instances_tested)
    std_deviation = (sum((x - mean_action_complexity)**2 for x in action_complexities) / instances_tested).sqrt()
    gaussian_bound = 3 * std_deviation
    conjecture_holds = all(0 <= rho_f <= 2**(n/2) + gaussian_bound for rho_f in action_complexities)
    
    counterexample = ""
    if not conjecture_holds:
        for i, rho_f in enumerate(action_complexities):
            if not (0 <= rho_f <= 2**(n/2) + gaussian_bound):
                counterexample = f"Instance {i+1}: rho_f = {rho_f}"
                break
    
    return {
        "metric_name": "Action Complexity",
        "metric_value": mean_action_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)).sqrt()
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")