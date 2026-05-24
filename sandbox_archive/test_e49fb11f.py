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
    
    def tropical_add(a, b):
        return max(a, b)
    
    def tropical_multiply(a, b):
        if a == float('-inf') or b == float('-inf'):
            return float('-inf')
        return a + b
    
    def tropical_negate(a):
        return -a
    
    def tropical_zero():
        return float('-inf')
    
    def tropical_one():
        return 0
    
    def tropical_is_zero(a):
        return a == float('-inf')
    
    def tropical_is_one(a):
        return a == 0
    
    def tropical_to_string(a):
        if a == float('-inf'):
            return '-∞'
        elif a == 0:
            return '0'
        else:
            return str(a)
    
    def tropical_matrix_add(A, B):
        m = len(A)
        n = len(A[0])
        C = [[tropical_add(A[i][j], B[i][j]) for j in range(n)] for i in range(m)]
        return C
    
    def tropical_matrix_multiply(A, B):
        m = len(A)
        p = len(B)
        n = len(B[0])
        C = [[tropical_zero() for j in range(n)] for i in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] = tropical_add(C[i][j], tropical_multiply(A[i][k], B[k][j]))
        return C
    
    def tropical_matrix_power(M, k):
        n = len(M)
        result = [[tropical_one() if i == j else tropical_zero() for j in range(n)] for i in range(n)]
        while k > 0:
            if k % 2 == 1:
                result = tropical_matrix_multiply(result, M)
            M = tropical_matrix_multiply(M, M)
            k //= 2
        return result
    
    def tropical_matrix_rank(A):
        m = len(A)
        n = len(A[0])
        rank = 0
        for i in range(m):
            if any(row[i] != float('-inf') for row in A):
                rank += 1
        return rank
    
    def tropical_polynomial_to_series(poly, n):
        m = len(poly)
        series = [[tropical_zero() for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if j < poly[i]:
                    series[i][j] = tropical_one()
        return series
    
    def minimal_rank(series):
        m = len(series)
        n = len(series[0])
        rank = 0
        for i in range(m):
            if any(row[i] != float('-inf') for row in series):
                rank += 1
        return rank
    
    def generate_tropical_polynomial(n, max_degree=5):
        m = random.randint(1, n)
        poly = [random.randint(0, max_degree) for _ in range(m)]
        return poly
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = generate_tropical_polynomial(n)
    series = tropical_polynomial_to_series(poly, n)
    rank = minimal_rank(series)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n ** (3 / 2),
        "counterexample": "" if rank <= n ** (3 / 2) else f"Polynomial {poly} has minimal rank {rank}, which exceeds {n ** (3 / 2)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")