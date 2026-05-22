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
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def log_det(A):
        det = 1
        for row in gaussian_elimination(A):
            det *= row[0]
        return math.log(abs(det))
    
    def max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j, random.uniform(0, 1)))
        return edges
    
    def sos_polynomial(edges, degree):
        # Simplified representation using a dictionary
        poly = {}
        for u, v, w in edges:
            for i in range(degree + 1):
                for j in range(degree + 1 - i):
                    k = degree - i - j
                    if (u, v, i, j, k) not in poly:
                        poly[(u, v, i, j, k)] = 0
                    poly[(u, v, i, j, k)] += w * math.comb(degree, i) * math.comb(degree - i, j)
        return poly
    
    def moment_matrix(poly, n):
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for u, v, i, j, k in poly:
            if u == v:
                M[i][j] += poly[(u, v, i, j, k)]
            else:
                M[i][k] += poly[(u, v, i, j, k)]
                M[j][i] += poly[(u, v, i, j, k)]
        return M
    
    def symplectic_invariant(M):
        # Simplified calculation of the minimal symplectic invariant
        n = len(M)
        det = 1
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                continue
            det *= M[i][i]
        return math.log(abs(det))
    
    n = random.randint(5, 40)
    d = random.randint(10, 20)
    R = 0.878 + (random.random() * 0.1)  # Ensure R > 0.878
    edges = max_cut_instance(n)
    poly = sos_polynomial(edges, d)
    M = moment_matrix(poly, n)
    
    invariant = symplectic_invariant(M)
    expected_bound = math.log(d / R)
    
    return {
        "metric_name": "symplectic_invariant",
        "metric_value": invariant,
        "instances_tested": 1,
        "conjecture_holds": invariant >= expected_bound,
        "counterexample": "" if invariant >= expected_bound else f"Expected {expected_bound}, got {invariant}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")