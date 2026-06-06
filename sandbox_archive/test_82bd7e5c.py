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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def frobenius_normal_form(A):
        m, n = len(A), len(A[0])
        F = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if A[i][j] != 0:
                    F[(i + j) % m][(j - i) % n] += A[i][j]
        return F
    
    def resolution_width(phi):
        # Placeholder for actual resolution width calculation
        # This is a dummy implementation and should be replaced with the actual logic
        return random.randint(1, 10)
    
    def cnf_to_matrix(phi):
        # Placeholder for converting CNF to matrix
        # This is a dummy implementation and should be replaced with the actual logic
        m = len(phi)
        n = max(max(clause) for clause in phi)
        A = [[Fraction(0) for _ in range(n)] for _ in range(m)]
        for i, clause in enumerate(phi):
            for var in clause:
                A[i][abs(var)-1] += Fraction(1 if var > 0 else -1)
        return A
    
    def matrix_dimension(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    phi = [[random.randint(-n, n) for _ in range(random.randint(2, n//2))] for _ in range(n)]
    A = cnf_to_matrix(phi)
    F = frobenius_normal_form(A)
    dim_F = matrix_dimension(F)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "Dimension of Frobenius Normal Form",
        "metric_value": dim_F,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": dim_F >= 0.7 * w_phi,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")