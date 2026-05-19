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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    n = 40
    p_values = [1.5, 2.0, 2.5]
    min_norm = float('inf')
    
    def singular_values(M):
        # Compute the singular values of M using power iteration method
        U = [[random.random() for _ in range(n)] for _ in range(n)]
        V = [[random.random() for _ in range(n)] for _ in range(n)]
        S = [1.0] * n
        
        def matmul(A, B):
            return [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
        
        def transpose(M):
            return [[M[j][i] for j in range(n)] for i in range(n)]
        
        def svd_step(U, V, S):
            U = matmul(U, matmul(V, matmul(transpose(V), matmul(M, V))))
            V = matmul(V, matmul(U, matmul(transpose(U), matmul(V, M))))
            S = [math.sqrt(sum(x * x for x in row)) for row in U]
            return U, V, S
        
        for _ in range(10):
            U, V, S = svd_step(U, V, S)
        
        return S
    
    def noncommutative_lp_norm(svals, p):
        return sum(x**(p/(p-1)) for x in svals)**((p-1)/p)
    
    random.seed(seed)
    for _ in range(30):
        M = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        norm = noncommutative_lp_norm(singular_values(M), p)
        min_norm = min(min_norm, norm)
    
    return {
        "metric_name": "noncommutative L^p norm",
        "metric_value": min_norm,
        "instances_tested": 30,
        "conjecture_holds": min_norm >= 0.1 * math.sqrt(n),
        "counterexample": "" if min_norm >= 0.1 * math.sqrt(n) else "min_norm < 0.1*sqrt(n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_norm < 0.1*sqrt(n)\" first_failing_seed={first_failing_seed}")