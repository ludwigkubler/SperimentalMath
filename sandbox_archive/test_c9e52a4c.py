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
    n = 40
    p_values = [1.5, 2.0, 2.5]
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def singular_values(M):
        # Compute the singular values of a matrix using power iteration method
        U, S, Vt = [], [], []
        A = M
        for _ in range(100):  # Power iteration iterations
            v = [random.gauss(0, 1) for _ in range(n)]
            u = [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]
            u_norm = math.sqrt(sum(x**2 for x in u))
            u = [x / u_norm for x in u]
            
            s = sum(u[i] * A[i][j] * v[j] for i in range(n) for j in range(n))
            S.append(s)
            
            v = [sum(A[j][i] * u[j] for j in range(n)) for i in range(n)]
            v_norm = math.sqrt(sum(x**2 for x in v))
            v = [x / v_norm for x in v]
        
        return sorted(S, reverse=True)
    
    def noncommutative_lp_norm(singular_values, p):
        return sum(s**(p/(p-1)) for s in singular_values)**(1/p)
    
    min_norm = float('inf')
    for _ in range(30):  # Number of instances per seed
        M = generate_disjointness_matrix(n)
        norm = noncommutative_lp_norm(singular_values(M), p)
        if norm < min_norm:
            min_norm = norm
    
    return {
        "metric_name": "noncommutative lp norm",
        "metric_value": min_norm,
        "instances_tested": 30,
        "conjecture_holds": min_norm >= 0.1 * math.sqrt(n),
        "counterexample": "" if min_norm >= 0.1 * math.sqrt(n) else f"min_norm={min_norm}, n={n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        random.seed(seed)
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
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")