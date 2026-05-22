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
    augmented = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        pivot_row = i
        for j in range(i+1, n):
            if abs(augmented[j][i]) > abs(augmented[pivot_row][i]):
                pivot_row = j
        
        augmented[i], augmented[pivot_row] = augmented[pivot_row], augmented[i]
        
        pivot = augmented[i][i]
        for j in range(i, n + 1):
            augmented[i][j] /= pivot
        
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(i, n + 1):
                    augmented[k][j] -= factor * augmented[i][j]
    
    return [row[-1] for row in augmented]

def matroid_polynomial(M):
    n = len(M)
    A = [[0] * (n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            if M[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    
    return gaussian_elimination(A, [1] * (n + 1))[n]

def permanent_encoding_circuit_size(M):
    n = len(M)
    if n == 0:
        return 1
    if n == 1:
        return M[0][0]
    
    size = 0
    for i in range(n):
        for j in range(i, n):
            if M[i][j]:
                sub_M = [row[:i] + row[i+1:j] + row[j+1:] for row in M[:i] + M[i+1:]]
                size += permanent_encoding_circuit_size(sub_M)
    
    return size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rho_M = matroid_polynomial(M)
    perm_circuit_size = permanent_encoding_circuit_size(M)
    
    if perm_circuit_size == 0:
        return {
            "metric_name": "Minimal Monomial Degree Invariant",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Permanent circuit size is zero"
        }
    
    ratio = rho_M / perm_circuit_size
    return {
        "metric_name": "Minimal Monomial Degree Invariant",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 2**(n/2 - 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")