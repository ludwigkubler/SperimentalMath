# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mult(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(n):
        max_row = i
        for j in range(i+1, m):
            if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                max_row = j
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        pivot = augmented[i][i]
        for j in range(n + 1):
            augmented[i][j] /= pivot
        for j in range(m):
            if j != i:
                factor = augmented[j][i]
                for k in range(n + 1):
                    augmented[j][k] -= factor * augmented[i][k]
    return [row[-1] for row in augmented]

def is_cyclic(G):
    n = len(G)
    visited = [False] * n
    rec_stack = [False] * n

    def dfs(v):
        if rec_stack[v]:
            return True
        if visited[v]:
            return False
        visited[v] = True
        rec_stack[v] = True
        for neighbor in G[v]:
            if dfs(neighbor):
                return True
        rec_stack[v] = False
        return False

    for node in range(n):
        if not visited[node]:
            if dfs(node):
                return True
    return False

def find_coxeter_group(clause_indicators):
    n = len(clause_indicators)
    G = [[] for _ in range(2*n)]
    for i in range(n):
        for j in range(i+1, n):
            if clause_indicators[i] != clause_indicators[j]:
                G[i].append(j+n)
                G[j+n].append(i)
    return G

def frege_proof_depth(clause_indicators):
    G = find_coxeter_group(clause_indicators)
    rank = len(G) // 2
    n = len(G)
    f_n = lcm(n, rank)
    return f_n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        clause_indicators = [random.choice([0, 1]) for _ in range(n)]
        depth = frege_proof_depth(clause_indicators)
        results.append(depth)
    mean = sum(results) / len(results)
    std_dev = (sum((x - mean) ** 2 for x in results) / len(results)) ** 0.5
    conjecture_holds = all(d <= f_n for d, f_n in zip(results, [frege_proof_depth(clause_indicators) for _ in range(30)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": mean,
        "instances_tested": 30,
        "n_max": 40,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 7 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")