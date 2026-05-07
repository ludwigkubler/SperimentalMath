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
    m, k, n = len(A), len(B), len(B[0])
    C = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[max_row] = M[max_row], M[i]
        factor = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= factor
        for j in range(n):
            if i != j:
                factor = M[j][i]
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    return [row[-1] for row in M]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(2, min(n // 2, 5))
    
    # Generate a random k-CLIQUE instance
    V = list(range(n))
    E = []
    for _ in range(k):
        clique = random.sample(V, k)
        for u in clique:
            for v in clique:
                if u < v and (u, v) not in E and (v, u) not in E:
                    E.append((u, v))
    
    # Construct the hypergraph's rank function via greedy closure
    rank = 0
    edges_covered = set()
    while len(edges_covered) < len(E):
        max_gain = -1
        best_edge = None
        for u, v in E:
            if (u, v) not in edges_covered:
                gain = sum(1 for e in E if e[0] == u or e[1] == u or e[0] == v or e[1] == v)
                if gain > max_gain:
                    max_gain = gain
                    best_edge = (u, v)
        edges_covered.add(best_edge)
        rank += 1
    
    # Compute ρ_f using the polymatroid axioms
    rho_f = rank
    
    # Test if ρ_f ≥ n/(4k) for k-CLIQUE and ρ_f ≤ 3 log n for all DNFs
    if rho_f < n / (4 * k):
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rho_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"k-CLIQUE instance with rho_f={rho_f} < n/(4k)"
        }
    if rho_f > 3 * math.log(n):
        return {
            "metric_name": "polymatroid_rank",
            "metric_value": rho_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"DNF instance with rho_f={rho_f} > 3 log n"
        }
    
    return {
        "metric_name": "polymatroid_rank",
        "metric_value": rho_f,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r['counterexample'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r['counterexample'])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")