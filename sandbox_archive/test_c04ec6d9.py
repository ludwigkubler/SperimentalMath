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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_multiply(A, B):
    m, k = len(A), len(B)
    n = len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented_matrix = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        pivot = augmented_matrix[i][i]
        for j in range(n+1):
            augmented_matrix[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented_matrix[j][i]
                for k in range(n+1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    return [row[-1] for row in augmented_matrix]

def compute_gram_matrix(clauses):
    n = len(clauses)
    G = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            count = 0
            for clause in clauses:
                if (i+1) in clause and (j+1) in clause:
                    count += 2
                elif (i+1) in clause or (j+1) in clause:
                    count += 1
            G[i][j] = G[j][i] = count
    return G

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    A = [row[:] for row in matrix]
    r = 0
    for i in range(n):
        if r < m:
            pivot_row = r
            while pivot_row < m and A[pivot_row][i] == 0:
                pivot_row += 1
            if pivot_row < m:
                A[r], A[pivot_row] = A[pivot_row], A[r]
                for j in range(n):
                    A[r][j] /= A[r][i]
                for j in range(m):
                    if j != r:
                        factor = A[j][i]
                        for k in range(n):
                            A[j][k] -= factor * A[r][k]
                r += 1
    return r

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(2*n, 3*n)
    clauses = []
    for _ in range(m):
        clause = set(random.sample(range(1, n+1), random.randint(1, n)))
        clauses.append(clause)
    
    G = compute_gram_matrix(clauses)
    min_rank = rank(G)
    
    metric_value = min_rank
    instances_tested = 1
    conjecture_holds = min_rank <= 3*n**2/m and min_rank <= 10*n**2/m
    counterexample = "" if conjecture_holds else "min_rank > 10n^2/m"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"min_rank > 10n^2/m\" first_failing_seed={first_failing_seed}")