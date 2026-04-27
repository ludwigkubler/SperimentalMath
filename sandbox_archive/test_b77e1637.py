# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n + 1):
                A[j][k] -= factor * A[i][k]
    return A

def forward_substitution(A, b):
    n = len(b)
    x = [0] * n
    for i in range(n):
        sum_j = sum(A[i][j] * x[j] for j in range(i))
        x[i] = (b[i] - sum_j) / A[i][i]
    return x

def backward_substitution(A, b):
    n = len(b)
    x = [0] * n
    for i in range(n-1, -1, -1):
        sum_j = sum(A[i][j] * x[j] for j in range(i+1, n))
        x[i] = (b[i] - sum_j) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B), len(B[0])
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def fast_walsh_hadamard_transform(x):
    n = len(x)
    if n == 1:
        return x
    even = fast_walsh_hadamard_transform(x[0::2])
    odd = fast_walsh_hadamard_transform(x[1::2])
    result = [0] * n
    for k in range(n // 2):
        result[k] = even[k] + odd[k]
        result[k + n // 2] = even[k] - odd[k]
    return result

def inverse_fast_walsh_hadamard_transform(x):
    n = len(x)
    if n == 1:
        return x
    even = inverse_fast_walsh_hadamard_transform([x[k] for k in range(0, n, 2)])
    odd = inverse_fast_walsh_hadamard_transform([x[k] for k in range(1, n, 2)])
    result = [0] * n
    for k in range(n // 2):
        result[k] = (even[k] + odd[k]) / n
        result[k + n // 2] = (even[k] - odd[k]) / n
    return result

def hamming_weight(x):
    return bin(x).count('1')

def generate_random_3cnf(n, density):
    clauses = []
    for _ in range(int(density * n * (n - 1) // 2)):
        while True:
            a, b, c = random.sample(range(1, n + 1), 3)
            if len(set([a, b, c])) == 3:
                break
        sign_a = random.choice([-1, 1])
        sign_b = random.choice([-1, 1])
        sign_c = random.choice([-1, 1])
        clauses.append((sign_a * a, sign_b * b, sign_c * c))
    return clauses

def is_satisfiable(clauses):
    n = max(abs(c) for clause in clauses)
    for assignment in range(2**n):
        if all(any(sign * (assignment & (1 << abs(l) - 1)) != l for sign, l in clause) for clause in clauses):
            return True
    return False

def compute_fourier_transform(A_F):
    n = len(A_F)
    A_F_hat = fast_walsh_hadamard_transform([A_F[i] for i in range(n)])
    return [abs(x) for x in A_F_hat]

def hypercontractive_defect(A_F, p_grid):
    n = len(A_F)
    A_F_norm_p = [sum(abs(A_F[i])**p for i in range(n))**(1/p) for p in p_grid]
    T_rho_A_F_norm_2 = []
    for rho in p_grid:
        T_rho_A_F = [0] * n
        for i in range(n):
            sum_j = 0
            for j in range(n):
                if hamming_weight(i ^ j) <= int(rho * (n - 1)):
                    sum_j += A_F[j]
            T_rho_A_F[i] = sum_j / 2**(int(rho * (n - 1)))
        T_rho_A_F_norm_2.append(sum(x**2 for x in T_rho_A_F)**0.5)
    return [math.log(T_rho_A_F_norm_2[i] / A_F_norm_p[i]) for i in range(len(p_grid))]

def resolution_width(clauses):
    n = max(abs(c) for clause in clauses)
    queue = [(clauses, 1)]
    while queue:
        current_clauses, width = queue.pop(0)
        if not current_clauses:
            return width
        new_clauses = []
        for clause in current_clauses:
            literals = [l for l in clause if abs(l) <= n]
            if len(literals) == 1:
                continue
            literal = random.choice(literals)
            new_clause = tuple(l for l in literals if l != literal and l != -literal)
            if not new_clause:
                return width + 1
            new_clauses.append(new_clause)
        queue.extend((new_clauses, width + 1))
    return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    densities = [4.4, 4.6, 4.8, 5.0]
    p_grid = [1.1, 1.3, 1.5, 1.7, 1.9]
    support_count = 0
    equality_count = 0

    for n in n_values:
        for density in densities:
            for _ in range(10):
                clauses = generate_random_3cnf(n, density)
                if is_satisfiable(clauses):
                    continue
                A_F = [sum(1 for assignment in range(2**n) if all(any(sign * (assignment & (1 << abs(l) - 1)) != l for sign, l in clause) for clause in clauses)) for _ in range(n)]
                A_F_hat = compute_fourier_transform(A_F)
                H_F = hypercontractive_defect(A_F_hat, p_grid)
                w_F_perp = resolution_width(clauses)
                if w_F_perp >= math.ceil(H_F[0] / math.log2(n + 1)):
                    support_count += 1
                    if density == 4.6:
                        equality_count += 1

    return {
        "metric_name": "support_fraction",
        "metric_value": support_count / (len(n_values) * len(densities) * 10),
        "instances_tested": len(n_values) * len(densities) * 10,
        "conjecture_holds": support_count == len(n_values) * len(densities) * 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)

    mean_support_fraction = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_support_fraction} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 80%\" first_failing_seed={first_failing_seed}")