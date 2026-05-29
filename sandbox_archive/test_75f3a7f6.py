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
    
    def generate_xor_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def max_plus_matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]
        return C
    
    def max_plus_matrix_multiply(A, B):
        m = len(A)
        p = len(B)
        n = len(B[0])
        C = [[-math.inf] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] = max(C[i][j], A[i][k] + B[k][j])
        return C
    
    def gaussian_elimination(M, b):
        m = len(M)
        n = len(M[0])
        augmented = [M[i] + [b[i]] for i in range(m)]
        
        for j in range(n):
            max_row = j
            for i in range(j+1, m):
                if augmented[i][j] > augmented[max_row][j]:
                    max_row = i
            
            augmented[j], augmented[max_row] = augmented[max_row], augmented[j]
            
            pivot = augmented[j][j]
            for k in range(n + 1):
                augmented[j][k] /= pivot
            
            for i in range(m):
                if i != j:
                    factor = augmented[i][j]
                    for k in range(n + 1):
                        augmented[i][k] -= factor * augmented[j][k]
        
        return [row[-1] for row in augmented]
    
    def min_tropical_cycle_rank(f, n):
        m = len(f)
        M = [[-math.inf] * m for _ in range(m)]
        b = [-math.inf] * m
        
        for i in range(m):
            for j in range(m):
                if f[i] != f[j]:
                    M[i][j] = math.log2(abs(i - j))
        
        return sum(gaussian_elimination(M, b))
    
    def randomized_query_complexity(f, n):
        queries = set()
        while len(queries) < n:
            x = random.randint(0, 2**n - 1)
            if f[x] not in queries:
                queries.add(f[x])
        return len(queries)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_xor_function(n)
        TCR_n = min_tropical_cycle_rank(f, n)
        Q_f = randomized_query_complexity(f, n)
        
        results.append({
            "n": n,
            "TCR_n": TCR_n,
            "Q_f": Q_f
        })
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    TCR_values = [r["TCR_n"] for r in results]
    Q_f_values = [r["Q_f"] for r in results]
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        rank_x = {x[i]: i + 1 for i in range(n)}
        rank_y = {y[i]: i + 1 for i in range(n)}
        
        sum_d_squared = sum((rank_x[x[i]] - rank_y[y[i]]) ** 2 for i in range(n))
        rho_numerator = 6 * sum_d_squared
        rho_denominator = n * (n**2 - 1)
        
        return 1 - rho_numerator / rho_denominator
    
    rho = spearman_rank_correlation(TCR_values, Q_f_values)
    
    mean_Q_f = sum(Q_f_values) / len(Q_f_values)
    std_Q_f = math.sqrt(sum((q - mean_Q_f) ** 2 for q in Q_f_values) / len(Q_f_values))
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": rho >= 0.8 and abs(mean_Q_f - sum(TCR_values) / len(TCR_values)) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials executed")
    else:
        rho_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
        mean_rho = sum(rho_values) / len(rho_values)
        std_rho = math.sqrt(sum((rho - mean_rho) ** 2 for rho in rho_values) / len(rho_values))
        
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            counterexample = "Spearman rank correlation < 0.8"
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")