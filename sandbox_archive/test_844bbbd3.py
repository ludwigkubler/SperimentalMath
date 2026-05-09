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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def gaussian_elimination(A, b):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i + 1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(m - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def random_d_regular_graph(n, d):
    if (n - 1) % d != 0:
        raise ValueError("d must be a divisor of n-1")
    G = [[] for _ in range(n)]
    degree = [0] * n
    edges_added = set()
    for i in range(d):
        for j in range(i + 1, n):
            if (i, j) not in edges_added and (j, i) not in edges_added:
                G[i].append(j)
                G[j].append(i)
                degree[i] += 1
                degree[j] += 1
                edges_added.add((i, j))
    for i in range(d):
        remaining = d - degree[i]
        candidates = [j for j in range(n) if j != i and j not in G[i]]
        random.shuffle(candidates)
        for j in candidates[:remaining]:
            G[i].append(j)
            G[j].append(i)
            degree[i] += 1
            degree[j] += 1
    return G

def adjacency_matrix(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in G[i]:
            A[i][j] = 1
    return A

def dehn_function(G):
    n = len(G)
    A = adjacency_matrix(G)
    I = [[int(i == j) for j in range(n)] for i in range(n)]
    B = [0] * n
    x = gaussian_elimination(A, B)
    return sum(abs(x[i]) for i in range(n))

def resolution_length(Phi):
    stack = []
    clauses = set()
    for clause in Phi:
        if len(clause) == 1:
            return 1
        literals = list(clause)
        while literals:
            literal = literals.pop()
            if literal not in clauses:
                clauses.add(literal)
                stack.append((literal, literals))
                break
        else:
            return float('inf')
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    d = 3
    G = random_d_regular_graph(n, d)
    delta_G = dehn_function(G)
    Phi = []
    for i in range(n):
        for j in G[i]:
            if i < j:
                Phi.append({i + 1, -j - 1})
    resolution_len = resolution_length(Phi)
    c = 0.5
    conjecture_holds = resolution_len >= 2 ** (c * delta_G)
    counterexample = "" if conjecture_holds else f"delta(G)={delta_G}, resolution length={resolution_len}"
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": len(Phi),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")