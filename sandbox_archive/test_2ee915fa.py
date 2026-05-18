# auto-injected by SEC sandbox
import itertools
import collections
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import json
from fractions import Fraction

def matrix_mult(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def matrix_add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]

def matrix_flatten(m):
    return [item for row in m for item in row]

def matrix_rank(m):
    if not m:
        return 0
    n = len(m)
    rank = 0
    for col in range(len(m[0])):
        pivot = -1
        for row in range(rank, n):
            if m[row][col] != 0:
                pivot = row
                break
        if pivot == -1:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        pivot_val = m[rank][col]
        for c in range(col, len(m[0])):
            m[rank][c] = Fraction(m[rank][c], pivot_val)
        for r in range(n):
            if r != rank and m[r][col] != 0:
                factor = m[r][col]
                for c in range(col, len(m[0])):
                    m[r][c] -= factor * m[rank][c]
        rank += 1
    return rank

def compute_rho(P, w):
    basis = []
    identity = [[1 if i == j else 0 for j in range(w)] for i in range(w)]
    basis.append(matrix_flatten(identity))
    for T in P:
        new_basis = []
        for b in basis:
            mat_b = [[b[i * w + j] for j in range(w)] for i in range(w)]
            mat_T = [[T[i][j] for j in range(w)] for i in range(w)]
            product = matrix_mult(mat_b, mat_T)
            new_basis.append(matrix_flatten(product))
        for b in new_basis:
            if b not in basis:
                basis.append(b)
    return math.log2(matrix_rank([[b[i] for b in basis] for i in range(len(basis[0]))]) + 1)

def generate_random_bp(n, w, seed):
    random.seed(seed)
    L = 4 * n
    P = []
    for _ in range(L):
        T = [[0 for _ in range(w)] for _ in range(w)]
        for i in range(w):
            j = random.randint(0, w - 1)
            T[i][j] = 1
        P.append(T)
    return P

def generate_adversarial_bp(n):
    w = 2 ** (n + 1)
    P = []
    for _ in range(2 * n):
        T = [[0 for _ in range(w)] for _ in range(w)]
        for i in range(w):
            T[i][i] = 1
        P.append(T)
    for _ in range(2 * n):
        T = [[0 for _ in range(w)] for _ in range(w)]
        for i in range(w):
            T[i][i ^ (1 << (n - 1))] = 1
        P.append(T)
    return P

def generate_friendly_bp(n):
    w = 2
    P = []
    for _ in range(2 * n):
        T = [[0 for _ in range(w)] for _ in range(w)]
        for i in range(w):
            T[i][i] = 1
        P.append(T)
    return P

def run_trial(seed):
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8]
    w_values = [4, 8]
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for w in w_values:
            P = generate_random_bp(n, w, seed)
            rho = compute_rho(P, w)
            metric_values.append(rho)
            if rho > 2 * math.log2(w + 1):
                conjecture_holds = False
                counterexample = f"Random BP with n={n}, w={w}, seed={seed} has ρ={rho} > 2*log2(w+1)"

    for n in [2, 3, 4]:
        P = generate_adversarial_bp(n)
        rho = compute_rho(P, 2 ** (n + 1))
        metric_values.append(rho)
        if rho < n - 2:
            conjecture_holds = False
            counterexample = f"Adversarial BP with n={n} has ρ={rho} < n-2"

    for n in range(2, 9):
        P = generate_friendly_bp(n)
        rho = compute_rho(P, 2)
        metric_values.append(rho)
        if rho > 2:
            conjecture_holds = False
            counterexample = f"Friendly BP with n={n} has ρ={rho} > 2"

    metric_value = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "rho",
        "metric_value": metric_value,
        "instances_tested": len(metric_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps({'seed': seed, **result})}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")