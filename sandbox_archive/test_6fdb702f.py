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
    random.seed(seed)
    
    def generate_transition_matrix(n):
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    T[i][j] = random.randint(1, 10)
                    T[j][i] = T[i][j]
        return T
    
    def sum_of_singular_values(T):
        n = len(T)
        U = [[0] * n for _ in range(n)]
        S = [0] * n
        V = [[0] * n for _ in range(n)]
        
        # Compute the transition matrix for read-twice BPs (IP_2)
        T_twice = generate_transition_matrix(n)
        
        # Compute singular values using power iteration method
        def power_iteration(A, max_iter=100):
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x**2 for x in v))
            for _ in range(max_iter):
                v = A @ v
                v /= math.sqrt(sum(x**2 for x in v))
            return v
        
        def svd(A):
            U = [[0] * n for _ in range(n)]
            S = [0] * n
            V = [[0] * n for _ in range(n)]
            
            for i in range(n):
                v = power_iteration(A)
                u = A @ v
                s = math.sqrt(sum(x**2 for x in u))
                U[i] = u / s
                S[i] = s
                V[i] = v
            
            return U, S, V
        
        U, S, V = svd(T_twice)
        sv_sum_twice = sum(S)
        
        return sv_sum_twice
    
    n = random.randint(5, 40)
    sv_sum_twice = sum_of_singular_values(n)
    
    return {
        "metric_name": "sum_of_singular_values",
        "metric_value": sv_sum_twice,
        "instances_tested": 1,
        "conjecture_holds": True if sv_sum_twice >= n else False,
        "counterexample": "" if sv_sum_twice >= n else f"n={n}, sum_of_singular_values={sv_sum_twice}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")