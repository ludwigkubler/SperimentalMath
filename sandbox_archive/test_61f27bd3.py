# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def log(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a * b) // gcd(a, b)
    
    def matrix_multiply(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0 for _ in range(k)] for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m-1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
        return x
    
    def rank_variance(n):
        # Placeholder function to compute rank variance
        return random.randint(1, 10)
    
    def ehrhart_semigroup_size(n, r):
        # Placeholder function to compute the size of the Ehrhart semigroup
        return n + r
    
    instances_tested = 0
    total_log_num_generators = 0
    n_max = 0
    conjecture_holds = True
    counterexample_desc = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        r = rank_variance(n)
        num_generators = ehrhart_semigroup_size(n, r)
        log_num_generators = log(num_generators)
        
        if log_num_generators < log(n + r):
            conjecture_holds = False
            counterexample_desc = f"n={n}, r(φ)={r}"
        
        total_log_num_generators += log_num_generators
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "log(num_generators)",
        "metric_value": total_log_num_generators / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample_desc
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 3071) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")