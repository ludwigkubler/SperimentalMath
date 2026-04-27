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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            A[j][i:] = [A[j][k] - factor * A[i][k] for k in range(i, n)]
    return A

def solve_linear_system(A, b):
    n = len(A)
    A_b = list(zip(A, b))
    gaussian_elimination(A_b)
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_b[i][1] - sum(A_b[i][0][j] * x[j] for j in range(i+1, n))) / A_b[i][0][i]
    return x

def matrix_multiplication(A, B):
    m, k = len(A), len(B[0])
    result = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            result[i][j] = sum(A[i][l] * B[l][j] for l in range(len(B)))
    return result

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    for j in range(n):
        det += ((-1) ** j) * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
    return det

def inverse(A):
    n = len(A)
    det = determinant(A)
    if det == 0:
        raise ValueError("Matrix is not invertible")
    adjugate = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            cofactor = ((-1) ** (i+j)) * determinant(minor)
            adjugate[j][i] = cofactor
    return matrix_multiplication(adjugate, [[1/det] * n for _ in range(n)])

def svd(A):
    m, n = len(A), len(A[0])
    A_t = list(zip(*A))
    U = gaussian_elimination(A)
    V = gaussian_elimination(A_t)
    S = [max(row) for row in U]
    return U, S, V

def continued_fraction(x, k):
    a = []
    while len(a) < k:
        x_inv = 1 / x
        a.append(int(x_inv))
        x = x_inv - int(x_inv)
    return a

def log_sum(a):
    s = 0
    for ai in a:
        s += math.log(1 + ai)
    return s

def comb_discrepancy(M, num_samples=400):
    n = len(M)
    max_disc = 0
    for _ in range(num_samples):
        A = random.sample(range(n), random.randint(1, n))
        B = random.sample(range(n), random.randint(1, n))
        disc = abs(sum(M[i][j] for i in A for j in B)) / (n ** 2)
        if disc > max_disc:
            max_disc = disc
    return max_disc

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6, 7, 8, 9]
    results = []
    for n in n_values:
        N = 2 ** n
        M_types = [
            (lambda _: [[random.choice([-1, 1]) for _ in range(N)] for _ in range(N)], "uniform"),
            (lambda _: [[-1 if i == j else 0 for i in range(N)] for j in range(N)], "Sylvester-Hadamard"),
            (lambda _: [[-1 if i & j == 0 else 1 for i in range(N)] for j in range(N)], "AND-of-XORs"),
            (lambda _: [[-1 if i & j != 0 else 1 for i in range(N)] for j in range(N)], "Disjointness")
        ]
        for M_type, name in M_types:
            M = M_type()
            U, S, V = svd(M)
            sigma_1, sigma_2 = S[0], S[1]
            rho = Fraction(sigma_2, sigma_1).limit_denominator(4 * N)
            a = continued_fraction(rho, math.ceil(math.log2(N)))
            S_M = log_sum(a)
            disc = comb_discrepancy(M)
            results.append({
                "metric_name": "disc_N",
                "metric_value": disc * N,
                "instances_tested": 1,
                "conjecture_holds": disc * N >= 0.05 * sigma_1 / (1 + S_M),
                "counterexample": "" if disc * N >= 0.05 * sigma_1 / (1 + S_M) else f"{name} matrix of size {N}x{N}"
            })
    return {
        "seed": seed,
        "trials": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["trials"])
    
    disc_values = [r["metric_value"] for r in all_results if "disc_N" in r["metric_name"]]
    support_fraction = sum(r["conjecture_holds"] for r in all_results) / len(all_results)
    hadamard_counterexample = any("Hadamard" in r["counterexample"] for r in all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={sum(disc_values)/len(disc_values):.4f} std={math.sqrt(sum((x - sum(disc_values)/len(disc_values))**2 for x in disc_values) / len(disc_values)):.4f} support_fraction={support_fraction:.2f}")
    elif hadamard_counterexample:
        first_failing_seed = next(r["seed"] for r in all_results if "Hadamard" in r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"Hadamard matrix\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f} hadamard_counterexample=False")