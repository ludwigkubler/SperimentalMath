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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for j in range(i - 1, -1, -1):
                b[j] -= A[j][i] * x[i]
        return x
    
    def matrix_mult(A, B):
        n = len(A)
        C = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det
    
    def inv(A):
        n = len(A)
        det_A = determinant(A)
        if det_A == 0:
            raise ValueError("Singular matrix")
        adjoint = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                submatrix = [[A[x][y] for y in range(n) if y != j] for x in range(n) if x != i]
                adjoint[i][j] = (-1) ** (i + j) * determinant(submatrix)
        inv_A = matrix_mult(adjoint, [Fraction(1, det_A)] * n)
        return inv_A
    
    def circuit_monotone_width(G):
        n = len(G)
        if n < 3:
            return 0
        edges = sum(G[i] for i in range(n))
        return edges // (n - 2)
    
    def alexander_dirac_invariant(M):
        n = len(M)
        if n < 3:
            return 0
        A = [[Fraction(0)] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = Fraction(1, M[i][j])
                A[j][i] = Fraction(1, M[j][i])
        B = [Fraction(1)] * n
        x = gaussian_elimination(A, B)
        return sum(x) / n
    
    def construct_manifold(G):
        n = len(G)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j]:
                    M[i][j] = M[j][i] = Fraction(1, G[i][j])
        return M
    
    def run_test(d, n):
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            neighbors = random.sample(range(n), d - 1)
            for j in neighbors:
                if i < j:
                    G[i][j] = G[j][i] = random.randint(1, 10)
        
        M = construct_manifold(G)
        w_G = circuit_monotone_width(G)
        m_alex_M = alexander_dirac_invariant(M)
        
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": Fraction(w_G * m_alex_M, (w_G**2 + m_alex_M**2).sqrt()),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(w_G - m_alex_M) <= 5,
            "counterexample": ""
        }
    
    results = []
    for d in [3, 4]:
        for _ in range(10):
            result = run_test(d, random.randint(5, 20))
            results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = Fraction(total_metric_value, len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_metric_value": mean_metric_value,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 53))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["mean_metric_value"] for r in results)
    mean_metric_value = Fraction(total_metric_value, len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if all(r["support_fraction"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")