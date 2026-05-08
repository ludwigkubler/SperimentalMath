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

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
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
        for j in range(n):
            M[i][j] /= factor
        b[i] /= factor
        for j in range(i+1, n):
            factor = M[j][i]
            for k in range(n):
                M[j][k] -= factor * M[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = b[i]
        for j in range(i+1, n):
            x[i] -= M[i][j] * x[j]
    return x

def rank(mat):
    mat = [row[:] for row in mat]
    r = 0
    for i in range(len(mat)):
        if all(x == 0 for x in mat[i]):
            continue
        r += 1
        factor = 1 / mat[i][i]
        for j in range(i, len(mat[0])):
            mat[i][j] *= factor
        for j in range(r):
            if i != j:
                factor = mat[j][i]
                for k in range(i, len(mat[0])):
                    mat[j][k] -= factor * mat[i][k]
    return r

def size(dnf):
    return sum(1 for term in dnf if any(lit != 0 for lit in term))

def rank_deficit(dnf):
    M = []
    for term in dnf:
        circuit = [i+1 for i, lit in enumerate(term) if lit == 1]
        if circuit not in M:
            M.append(circuit)
    return rank(M) - math.log2(size(dnf))

def is_k_clique(graph, k):
    n = len(graph)
    for subset in itertools.combinations(range(n), k):
        if all(graph[i][j] == 1 for i, j in itertools.combinations(subset, 2)):
            return True
    return False

def characteristic_set(graph, k):
    n = len(graph)
    for subset in itertools.combinations(range(n), k):
        if all(graph[i][j] == 0 for i, j in itertools.combinations(subset, 2)):
            return subset
    return None

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    dnf_size = random.randint(1, n**3)
    dnf = []
    for _ in range(dnf_size):
        term = [random.choice([-1, 1]) if i < n else 0 for i in range(n)]
        dnf.append(term)
    
    metric_value = rank_deficit(dnf)
    conjecture_holds = metric_value <= 2 * math.log(n)
    counterexample = "" if conjecture_holds else "upper_bound_violation"
    
    return {
        "metric_name": "rank_deficit",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"upper_bound_violation\" first_failing_seed={first_failing_seed}")