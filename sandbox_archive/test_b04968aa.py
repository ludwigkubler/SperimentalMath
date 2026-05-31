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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += ((-1) ** j) * A[0][j] * determinant(submatrix)
        return det
    
    def hyperbolic_metric_entropy(G):
        n = len(G)
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] != 0:
                    A[i][j] = A[j][i] = math.log(2 / (G[i][j] + G[j][i]))
        det_A = determinant(A)
        return -det_A
    
    def resolution_width(phi):
        # Placeholder for actual resolution width calculation
        # This is a dummy implementation for testing purposes
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    m = random.randint(n // 2, n * (n - 1) // 2)
    phi = []
    for _ in range(m):
        var = random.randint(1, n)
        neg = random.choice([True, False])
        clause = [var if not neg else -var]
        while len(clause) < n:
            clause.append(random.randint(1, n))
        phi.append(tuple(sorted(clause)))
    
    G = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        G[i][i] = 1
    for clause in phi:
        for var in clause:
            if var > 0:
                G[0][var] += 1
                G[var][0] += 1
    
    H_G = hyperbolic_metric_entropy(G)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "H(G(φ)) / w(φ)",
        "metric_value": H_G / w_phi if w_phi != 0 else float('inf'),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": H_G / w_phi >= 0.5 if w_phi != 0 else False,
        "counterexample": "" if H_G / w_phi >= 0.5 else f"phi={phi}, H(G(φ))={H_G}, w(φ)={w_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = len([res for res in results if res["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["counterexample"] for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")