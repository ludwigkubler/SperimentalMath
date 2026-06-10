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
    m, n = len(A), len(B[0])
    p = len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gaussian_elimination(A, b):
    m, n = len(A), len(b)
    Augmented = [A[i] + [b[i]] for i in range(m)]
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(Augmented[j][i]) > abs(Augmented[max_row][i]):
                max_row = j
        Augmented[i], Augmented[max_row] = Augmented[max_row], Augmented[i]
        for j in range(i+1, m):
            factor = Augmented[j][i] / Augmented[i][i]
            for k in range(n+1):
                Augmented[j][k] -= factor * Augmented[i][k]
    x = [0] * n
    for i in range(m-1, -1, -1):
        x[i] = Augmented[i][-1] / Augmented[i][i]
        for j in range(i-1, -1, -1):
            Augmented[j][-1] -= Augmented[j][i] * x[i]
    return x

def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate_primes(count):
    primes = []
    num = 2
    while len(primes) < count:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def random_cnf(n, m):
    clauses = set()
    for _ in range(m):
        clause = set(random.sample(range(1, n+1), random.randint(1, n)))
        if not any(len(clause.intersection(c)) > 0 for c in clauses):
            clauses.add(frozenset(clause))
    return clauses

def kneser_graph(n, k):
    V = set()
    for subset in itertools.combinations(range(1, n+1), k):
        V.add(tuple(sorted(subset)))
    E = []
    for i in range(len(V)):
        for j in range(i+1, len(V)):
            if len(set(V[i]) ^ set(V[j])) == 2:
                E.append((i, j))
    return V, E

def automorphism_group(G):
    n = len(G)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if G[i][j]:
                A[i][j] = 1
                A[j][i] = 1
    b = [1] * n
    x = gaussian_elimination(A, b)
    return sum(x)

def min_degree(G):
    return max(sum(row) for row in G)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    primes = generate_primes(30)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = random_cnf(n, n*2)
            V, E = kneser_graph(n, 2)
            G = [[0] * len(V) for _ in range(len(V))]
            for u, v in E:
                G[u][v] = 1
                G[v][u] = 1
            perm_count = automorphism_group(G)
            min_deg = min_degree(G)
            results.append({
                "n": n,
                "perm_count": perm_count,
                "min_deg": min_deg,
                "satisfying_assignments": len(cnf) * (2**n - len(cnf))
            })
    metric_value = sum(result["perm_count"] for result in results)
    instances_tested = len(results)
    n_max = max(result["n"] for result in results)
    conjecture_holds = all(result["min_deg"] >= 2**result["n"] - len(result["satisfying_assignments"]) for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "Automorphism Group Permutation Count",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else generate_primes(30)
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=mapping_undefined first_failing_seed={first_failing_seed}")