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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_matrix(n, r):
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        U, _, Vt = qr_decomposition(A)
        H = (U @ Vt).T
        return H
    
    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[0] * n for _ in range(m)]
        R = A.copy()
        
        for j in range(n):
            s = 0
            for i in range(j, m):
                s += R[i][j] ** 2
            if s == 0:
                continue
            u = [R[i][j] / math.sqrt(s) if i == j else R[i][j] for i in range(m)]
            Q[j] = u
            
            for i in range(j + 1, m):
                q_j = Q[j]
                s = sum(q_j[k] * R[i][k] for k in range(n))
                for k in range(n):
                    R[i][k] -= s * q_j[k]
        
        return Q, R, Q
    
    def spectral_gap(H):
        n = len(H)
        eigenvalues = [0] * n
        v = [1] * n
        
        for _ in range(100):  # Power iteration method
            v = [sum(H[i][j] * v[j] for j in range(n)) for i in range(n)]
            norm = math.sqrt(sum(x ** 2 for x in v))
            v = [x / norm for x in v]
        
        lambda_max = max(v)
        lambda_min = min(-v)
        return abs(lambda_max - lambda_min)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            r = random.randint(1, min(n - 1, 10))  # Matrix rank
            H = generate_matrix(n, r)
            gap = spectral_gap(H)
            total_metric_value += gap
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_metric_value = total_metric_value / instances_tested
    conjecture_holds = all(gap >= Fraction(r, math.log(n)) for r in range(1, min(n - 1, 10)) for n in n_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Spectral Gap",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")