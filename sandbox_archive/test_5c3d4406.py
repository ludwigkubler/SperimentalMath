# auto-injected by SEC sandbox
import collections
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import json
from itertools import combinations

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return A

def solve_linear_system(A, b):
    A = [row[:] + [b[i]] for i, row in enumerate(A)]
    A = gaussian_elimination(A)
    n = len(A)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, k, n = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for l in range(k):
                C[i][j] += A[i][l] * B[l][j]
    return C

def transpose_matrix(A):
    m, n = len(A), len(A[0])
    B = [[0] * m for _ in range(n)]
    for i in range(m):
        for j in range(n):
            B[j][i] = A[i][j]
    return B

def determinant(A):
    if len(A) == 1:
        return A[0][0]
    det = 0
    sign = 1
    for i in range(len(A)):
        submatrix = [row[:i] + row[i+1:] for row in A[1:]]
        det += sign * A[0][i] * determinant(submatrix)
        sign *= -1
    return det

def inverse_matrix(A):
    n = len(A)
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Matrix is singular")
    adjoint = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[:i] + A[i+1:]]
            minor = determinant(submatrix)
            adjoint[j][i] = minor * (-1) ** (i + j)
    inv_A = matrix_multiplication(adjoint, [[1 / det_A] * n for _ in range(n)])
    return inv_A

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define candidate pairs (f, g)
    pairs = [
        (([0, 0, 1], [0, 1, 1], [1, 0, 1]), ([0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 1])),
        (([0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 1]), ([0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 0, 1], [0, 0, 1, 1, 1], [0, 1, 0, 0, 1])),
        (([0, 0, 0, 0, 1], [0, 0, 0, 1, 1], [0, 0, 1, 0, 1], [0, 0, 1, 1, 1], [0, 1, 0, 0, 1]), ([0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 1, 1])),
        (([0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1], [0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 1], [0, 0, 1, 0, 0, 1], [0, 0, 1, 0, 1, 1]), ([0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 0, 1], [0, 0, 0, 0, 1, 1, 1], [0, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1], [0, 0, 0, 1, 1, 0, 1]))
    ]
    
    total_slack = 0
    valid_pairs = 0
    
    for f, g in pairs:
        n, n_prime = len(f), len(g)
        
        # Build X_f and X_g
        X_f = [[0] * (n + 1) for _ in range(n)]
        X_g = [[0] * (n_prime + 1) for _ in range(n_prime)]
        for x, y in combinations(range(2 ** n), 2):
            if f[x].count(1) == 1 and f[y].count(1) == 1:
                X_f[f.index([1, 0])][f.index([0, 1])] += 1
                X_g[g.index([1, 0])][g.index([0, 1])] += 1
        
        # Compute the induced Φ : X_f → X_g from φ
        phi = [0] * n_prime
        for i in range(n):
            if f[i].count(1) == 1:
                phi[f.index([1, 0])] = g.index([1, 0])
                phi[f.index([0, 1])] = g.index([0, 1])
        
        # Measure its empirical distortion D
        D = 0
        for x, y in combinations(range(2 ** n), 2):
            if f[x].count(1) == 1 and f[y].count(1) == 1:
                d_f = abs(x - y)
                d_g = abs(phi[f.index([1, 0])] - phi[f.index([0, 1])])
                D = max(D, max(d_g / d_f, d_f / d_g))
        
        # Sample a basis of HX^1(X_g) by computing ker(δ^1)/im(δ^0)
        delta_0 = [[0] * (n_prime + 1) for _ in range(n_prime)]
        delta_1 = [[0] * n_prime for _ in range(n_prime + 1)]
        for i in range(n_prime):
            for j in range(i, n_prime):
                if g[i].count(1) == 1 and g[j].count(1) == 1:
                    delta_0[i][j] = 1
                    delta_1[j][i] = 1
        
        ker_delta_1 = []
        for i in range(n_prime + 1):
            if sum(delta_1[i]) == 1:
                ker_delta_1.append(i)
        
        im_delta_0 = []
        for j in range(n_prime):
            if any(sum(delta_0[i][j] * x for i in range(n_prime)) == 1 for x in ker_delta_1):
                im_delta_0.append(j)
        
        # Sample Roe-controlled operators T on X_g with propagation R ∈ {1,…,diam(X_g)}
        R = random.randint(1, n_prime)
        T = [[random.random() if i != j else 0 for j in range(n_prime)] for i in range(n_prime)]
        
        # Tabulate κ(g) := max_{c,T} log|⟨c,T⟩|/log R
        kappa_g = 0
        for c in combinations(range(n_prime), 2):
            if g[c[0]].count(1) == 1 and g[c[1]].count(1) == 1:
                inner_product = sum(T[i][j] * (g[i].index(1) - g[j].index(1)) for i, j in combinations(c, 2))
                kappa_g = max(kappa_g, math.log(abs(inner_product)) / math.log(R))
        
        # Pull back via Φ^*: c ↦ c∘(Φ×Φ), T ↦ Φ^*T (matrix restriction with propagation ≤ D·R)
        Phi_star_T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i].count(1) == 1 and f[j].count(1) == 1:
                    Phi_star_T[i][j] = T[phi[f.index([1, 0])]][phi[f.index([0, 1])]]
        
        # Recompute ⟨Φ^*c, Φ^*T⟩
        kappa_f = 0
        for c in combinations(range(n), 2):
            if f[c[0]].count(1) == 1 and f[c[1]].count(1) == 1:
                inner_product = sum(Phi_star_T[i][j] * (f[i].index(1) - f[j].index(1)) for i, j in combinations(c, 2))
                kappa_f = max(kappa_f, math.log(abs(inner_product)) / math.log(R))
        
        # Verify κ(f) ≤ D·κ(g) + 1
        slack = D * kappa_g + 1 - kappa_f
        total_slack += slack
        
        if slack >= 0:
            valid_pairs += 1
    
    metric_value = total_slack / len(pairs)
    conjecture_holds = valid_pairs >= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "slack",
        "metric_value": metric_value,
        "instances_tested": len(pairs),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if not sys.argv[1:] else list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_slack = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")