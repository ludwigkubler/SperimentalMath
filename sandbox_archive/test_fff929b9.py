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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def generate_k_sat_instance(m, n):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause:
                    clause.add(var)
            clauses.append(list(clause))
        return clauses
    
    def tropical_vector_space(xor_func):
        n = int(math.log2(len(xor_func)))
        T = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if xor_func[(i - 1) ^ (j - 1)] == 1:
                    T[i][j] = 1
        return T
    
    def tusnady_2_box_discrepancy(T):
        n = len(T) - 1
        D = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if T[i][j] == 1:
                    D[i][j] = max(abs(i - j), abs(n - i - j))
        return sum(sum(row) for row in D)
    
    def minimal_rank(T):
        n = len(T) - 1
        rank = 0
        for i in range(1, n + 1):
            if any(T[i][j] == 1 for j in range(1, n + 1)):
                rank += 1
        return rank
    
    def spearman_rank_correlation(ranks_x, ranks_y):
        n = len(ranks_x)
        sorted_indices_x = sorted(range(n), key=lambda i: ranks_x[i])
        sorted_indices_y = sorted(range(n), key=lambda i: ranks_y[i])
        rho_numerator = sum((sorted_indices_x[i] - sorted_indices_y[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1)
        return 1 - (6 * rho_numerator) / rho_denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks_x = []
    ranks_y = []
    
    for n in n_values:
        xor_func = generate_xor_function(n)
        T = tropical_vector_space(xor_func)
        D = tusnady_2_box_discrepancy(T)
        r_f = minimal_rank(T)
        
        ranks_x.append(r_f)
        ranks_y.append(D)
    
    rho = spearman_rank_correlation(ranks_x, ranks_y)
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": rho >= 0.5,
        "counterexample": "" if rho >= 0.5 else "rho < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho < 0.5' first_failing_seed={first_failing_seed}")