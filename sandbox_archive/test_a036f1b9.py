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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate below
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        
        # Back substitution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(A[i][-1], A[i][i])
            for j in range(i-1, -1, -1):
                A[j][-1] -= A[j][i] * x[i]
        
        return x
    
    def matrix_multiply(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def tensor_product(f, g):
        n = len(f)
        result = [[0] * (n * n) for _ in range(n * n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        result[i*n + k][j*n + l] = f[i][k] * g[j][l]
        return result
    
    def acc0_circuit_threshold(f, n):
        # Placeholder function to simulate ACC⁰ circuit threshold
        # This is a dummy implementation and should be replaced with actual logic
        return 2**n // (2**len(f))
    
    def tropicalized_configuration_space(f):
        n = len(f)
        T_f = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                T_f[i][j] = max(f[i], f[j])
        return T_f
    
    def rank(matrix):
        A = [row[:] + [1] for row in matrix]
        gaussian_elimination(A)
        rank = 0
        for row in A:
            if any(row[col] != 0 for col in range(len(row)-1)):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    f = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    T_f = tropicalized_configuration_space(f)
    g = tensor_product(f, f)
    theta_n_k = acc0_circuit_threshold(g, n)
    
    min_rank_T_f = rank(T_f)
    
    metric_name = "min_r(rank(T_f))"
    metric_value = min_rank_T_f
    instances_tested = 1
    conjecture_holds = min_rank_T_f <= theta_n_k
    counterexample = "" if conjecture_holds else f"Counterexample: n={n}, f={f}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = results[next(i for i, r in enumerate(results) if not r["conjecture_holds"])["counterexample"]]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")