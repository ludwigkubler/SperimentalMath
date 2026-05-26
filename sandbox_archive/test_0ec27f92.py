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
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = -A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] += factor * A[i][k]

def rank(A):
    n = len(A)
    r = 0
    for i in range(n):
        if all(abs(A[i][j]) < 1e-9 for j in range(r)):
            continue
        for j in range(r, n):
            A[i], A[j] = A[j], A[i]
            break
        r += 1
    return r

def characteristic_polynomial(f):
    n = len(f)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            A[i][j] = f[(i+j) % n]
    det = 0
    for p in itertools.permutations(range(n)):
        sign = (-1)**sum(i < j for i, j in zip(p, sorted(p)))
        prod = 1
        for i in range(n):
            prod *= A[i][p[i]]
        det += sign * prod
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    
    det = characteristic_polynomial(f)
    if det == 0:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    H = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            H[i][j] = Fraction(1, (i + j + 2) * (i + j + 3))
    
    rank_H = rank(H)
    
    return {
        "metric_name": "rank",
        "metric_value": rank_H,
        "instances_tested": 1,
        "conjecture_holds": rank_H <= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(r['conjecture_holds'] for r in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")