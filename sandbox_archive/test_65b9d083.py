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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
        A[i], A[max_row] = A[max_row], A[i]
        if A[i][i] == 0:
            continue
        for j in range(n):
            A[i][j] /= A[i][i]
        for k in range(m):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]

def matrix_rank(A):
    m, n = len(A), len(A[0])
    rank = 0
    B = [row[:] for row in A]
    gaussian_elimination(B)
    for i in range(m):
        if any(B[i]):
            rank += 1
    return rank

def field_rank(matrix):
    m, n = len(matrix), len(matrix[0])
    rank = 0
    B = [[Fraction(matrix[i][j]) for j in range(n)] for i in range(m)]
    gaussian_elimination(B)
    for i in range(m):
        if any(b != Fraction(0) for b in B[i]):
            rank += 1
    return rank

def communication_matrix(f, n):
    C = [[0] * (2**n) for _ in range(2**n)]
    for x in range(2**n):
        for y in range(2**n):
            if f(x ^ y) == f(x) ^ f(y):
                C[x][y] = 1
            else:
                C[x][y] = -1
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = lambda x: random.choice([0, 1])
        C = communication_matrix(f, n)
        rank = matrix_rank(C)
        variance = sum((C[i][j] - rank)**2 for i in range(2**n) for j in range(2**n)) / (2**(2*n))
        results.append({
            "n": n,
            "rank": rank,
            "variance": variance
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    mean_variance = sum(result["variance"] for result in results) / len(results)
    std_variance = math.sqrt(sum((result["variance"] - mean_variance)**2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["rank"] - (mean_variance**2)) <= 3 * std_rank) / len(results)
    
    return {
        "metric_name": "Brauer group rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"support_fraction={support_fraction:.2f} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")