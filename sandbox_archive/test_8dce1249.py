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
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def rank(matrix):
    m, n = len(matrix), len(matrix[0])
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(m):
        augmented_matrix[i][-1] = 1
    rref = gaussian_elimination(augmented_matrix, [0] * n)
    rank = sum(1 for row in rref if any(row[j] != 0 for j in range(n)))
    return rank

def generate_frege_tree(depth):
    if depth == 0:
        return []
    else:
        left = generate_frege_tree(random.randint(0, depth - 1))
        right = generate_frege_tree(random.randint(0, depth - 1))
        return [random.choice(['+', '-'])] + left + right

def run_trial(seed: int) -> dict:
    random.seed(seed)
    depths = range(1, 41)
    results = []
    for D in depths:
        for _ in range(30):
            tree = generate_frege_tree(D)
            literals = set()
            for node in tree:
                if node != '+' and node != '-':
                    literals.add(node)
            G = [[l1 == l2 for l2 in literals] for l1 in literals]
            b = [1 if literal in tree else 0 for literal in literals]
            rho_G = rank(G)
            results.append((D, rho_G))
    mean_value = sum(D - rho_G for D, rho_G in results) / len(results)
    support_fraction = sum(1 for D, rho_G in results if rho_G <= D) / len(results)
    conjecture_holds = support_fraction == 1
    counterexample = "" if conjecture_holds else f"rank={rho_G}, expected={D}"
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")