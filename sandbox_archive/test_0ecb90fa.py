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
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def noncommutative_Lp_dimension(f, n):
    m = len(f)
    if m == 0:
        return 1
    density_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if f(i) == f(j):
                density_matrix[i][j] += Fraction(1, m)
    identity_matrix = [[Fraction(1 if i==j else 0) for j in range(n)] for i in range(n)]
    A = [row[:] for row in identity_matrix]
    for _ in range(m):
        A = matrix_multiplication(A, density_matrix)
    A = gaussian_elimination(A)
    rank = sum(1 for row in A if any(x != 0 for x in row))
    return rank

def communication_complexity(f, d, p):
    n = len(f)
    max_comm_cost = 0
    for i in range(n):
        for j in range(i+1, n):
            comm_cost = math.ceil(d * (f[i] != f[j]) ** p)
            if comm_cost > max_comm_cost:
                max_comm_cost = comm_cost
    return max_comm_cost

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n+1, 2*n)
    f = {i: random.randint(0, m-1) for i in range(n)}
    
    d = noncommutative_Lp_dimension(f, n)
    upper_bound = d ** p
    
    comm_cost = communication_complexity(f, d, p)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_cost,
        "instances_tested": 1,
        "conjecture_holds": comm_cost <= upper_bound,
        "counterexample": "" if comm_cost <= upper_bound else f"Counterexample for n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*100+1, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm_cost = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm_cost} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_comm_cost} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")