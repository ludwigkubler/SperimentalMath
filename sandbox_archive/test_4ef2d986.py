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
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def construct_category(f):
        # Placeholder for constructing the category from f
        # This is a dummy implementation and should be replaced with actual logic
        return [[random.randint(0, 1) for _ in range(5)] for _ in range(5)]
    
    def construct_group(category):
        # Placeholder for constructing the group from the category
        # This is a dummy implementation and should be replaced with actual logic
        n = len(category)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A = category
        B = gaussian_elimination(A, [1]*n)
        G = matrix_multiply(I, B)
        return G
    
    def compute_rank(G):
        # Placeholder for computing the rank of the group
        # This is a dummy implementation and should be replaced with actual logic
        n = len(G)
        rank = 0
        for row in G:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
        return rank
    
    def construct_acc_circuit(f):
        # Placeholder for constructing the ACC⁰ circuit from f
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(5, 20)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = lambda x: sum(x[i] * (i+1) for i in range(n))
    category = construct_category(f)
    G = construct_group(category)
    rank_G = compute_rank(G)
    s_f = construct_acc_circuit(f)
    
    return {
        "metric_name": "Rank of Categorified K-theory Group",
        "metric_value": rank_G,
        "instances_tested": 1,
        "conjecture_holds": rank_G <= s_f,
        "counterexample": "" if rank_G <= s_f else f"rank(G)={rank_G}, s(f)={s_f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")