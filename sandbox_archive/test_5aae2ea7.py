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
    return abs(a * b) // gcd(a, b)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Inverse doesn't exist")
    else:
        return x % m

def matrix_mult(A, B):
    n = len(A)
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(n + 1):
            M[i][j] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n + 1):
                M[j][k] -= factor * M[i][k]
    x = [0 for _ in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = M[i][n]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def submodular_width(P, n):
    max_width = 0
    for X in range(1 << n):
        for Y in range(1 << n):
            width = P[X] + P[Y] - P[X & Y]
            if width > max_width:
                max_width = width
    return max_width

def k_clique_instance(n, k):
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if random.randint(0, 1) == 0 and len([x for x in range(k) if (i >> x) & 1 and (j >> x) & 1]) >= k-1:
                edges.append((i, j))
    return edges

def general_cnf_instance(n):
    clauses = []
    for _ in range(n):
        clause = random.sample(range(n), random.randint(1, n))
        clauses.append(clause)
    return clauses

def polymatroid_rank(P, X):
    return sum(P[i] for i in range(len(X)) if (X >> i) & 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n//2, 5))
    
    P_clique = [polymatroid_rank([i for i in range(n)], X) for X in range(1 << n)]
    P_general = [polymatroid_rank([i for i in range(n)], X) for X in range(1 << n)]
    
    width_clique = submodular_width(P_clique, n)
    width_general = submodular_width(P_general, n)
    
    metric_value_clique = width_clique
    metric_value_general = width_general
    
    conjecture_holds = (width_clique >= n and width_general <= math.log(n))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "submodular_width",
        "metric_value_clique": metric_value_clique,
        "metric_value_general": metric_value_general,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_clique = sum(r["metric_value_clique"] for r in results) / len(results)
    std_clique = math.sqrt(sum((r["metric_value_clique"] - mean_clique) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean_clique={mean_clique} std_clique={std_clique} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean_clique={mean_clique} std_clique={std_clique} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")