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
    
    def tropical_identity(x):
        return x
    
    def tropical_inverse(x):
        if x == float('-inf'):
            return float('inf')
        return -x
    
    def tropical_matrix_multiply(A, B):
        n = len(A)
        C = [[tropical_zero() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] = tropical_add(C[i][j], tropical_multiply(A[i][k], B[k][j]))
        return C
    
    def tropical_matrix_rank(matrix):
        n = len(matrix)
        A = [row[:] for row in matrix]
        rank = 0
        for i in range(n):
            if all(A[j][i] == tropical_zero() for j in range(rank)):
                continue
            pivot_row = rank
            for j in range(rank + 1, n):
                if A[j][i] != tropical_zero():
                    A[pivot_row], A[j] = A[j], A[pivot_row]
                    break
            for j in range(n):
                if j == i:
                    continue
                factor = tropical_negate(A[j][i])
                for k in range(n):
                    A[j][k] = tropical_add(A[j][k], tropical_multiply(factor, A[pivot_row][k]))
            rank += 1
        return rank
    
    def construct_quasi_symmetric_function(P):
        n = len(P)
        f = [[tropical_zero() for _ in range(2**n)] for _ in range(n)]
        for i in range(n):
            for j in range(2**i):
                if P[i][j] != 0:
                    f[i][j] = tropical_add(f[i][j], P[i][j])
        return f
    
    def bp_readtwice_complexity(P):
        n = len(P)
        dp = [[tropical_zero() for _ in range(2**n)] for _ in range(n)]
        dp[0][0] = tropical_one()
        for i in range(n):
            for j in range(2**i):
                if P[i][j] != 0:
                    for k in range(2**(i+1)):
                        dp[i+1][k] = tropical_add(dp[i+1][k], tropical_multiply(P[i][j], dp[i][k]))
        return max(max(row) for row in dp)
    
    n = random.randint(5, 40)
    P = [[random.choice([tropical_zero(), tropical_one()]) for _ in range(2**i)] for i in range(n)]
    f = construct_quasi_symmetric_function(P)
    rank = tropical_matrix_rank(f)
    bp_complexity = bp_readtwice_complexity(P)
    
    conjecture_holds = abs(bp_complexity - math.log(rank)) <= 1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "BP_ReadTwice complexity",
        "metric_value": bp_complexity,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")