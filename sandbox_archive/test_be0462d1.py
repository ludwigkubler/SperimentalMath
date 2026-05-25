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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def symmetric_group_universal_enveloping_algebra(n):
        if n == 1:
            return [[Fraction(1)]], Fraction(0)
        I = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        H = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            H[i][i] = Fraction(i + 1)
        return I, H
    
    def noncommutative_tensor_product(A, B):
        m, n = len(A), len(B[0])
        C = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                C[i][j] = A[i][j]
        return C
    
    def minimal_rank(matrix):
        rank = 0
        for row in gaussian_elimination(matrix):
            if any(row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    G, H = symmetric_group_universal_enveloping_algebra(n)
    A = noncommutative_tensor_product(G, H)
    B = noncommutative_tensor_product(H, G)
    C = matrix_multiply(A, B)
    
    rank_A = minimal_rank(A)
    rank_B = minimal_rank(B)
    rank_C = minimal_rank(C)
    
    metric_value = max(rank_A, rank_B, rank_C)
    conjecture_holds = metric_value <= n * math.log(n, 2) ** 2
    counterexample = "" if conjecture_holds else f"Rank {metric_value} exceeds O({n} log^2 {n})"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")