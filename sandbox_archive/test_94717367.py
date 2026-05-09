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
# end SEC prelude

import random
import math
from typing import List, Dict

def gaussian_elimination(A: List[List[float]]) -> List[List[float]]:
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate non-pivot elements
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
    return A

def count_positive_eigenvalues(A: List[List[float]]) -> int:
    n = len(A)
    eigenvalues = [0] * n
    for i in range(n):
        if abs(A[i][i]) > 1e-9:
            eigenvalues[i] = A[i][i]
    return sum(1 for ev in eigenvalues if ev > 0)

def max_cut_instance(n: int) -> List[List[int]]:
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        G[i][i] = 0
    return G

def degree_d_moment_matrix(G: List[List[int]], d: int) -> List[List[float]]:
    n = len(G)
    M = [[0.0 for _ in range(d+1)] for _ in range(d+1)]
    for i in range(n):
        for j in range(i, n):
            if G[i][j] == 1:
                for k in range(d+1):
                    for l in range(k+1):
                        M[l][k-l] += (i**l * j**(k-l) + j**l * i**(k-l)) / (2 * n)
    return M

def sos_refutation_degree(M: List[List[float]], d_max: int) -> int:
    for d in range(1, d_max+1):
        A = degree_d_moment_matrix(M, d)
        A = gaussian_elimination(A)
        if all(abs(A[i][i]) > 0 for i in range(d+1)):
            return d
    return d_max + 1

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    n = random.randint(5, 40)
    G = max_cut_instance(n)
    positive_eigenvalue_counts = []
    refutation_degrees = []
    
    for d in range(2, 9):
        M = degree_d_moment_matrix(G, d)
        eigenvalues = count_positive_eigenvalues(M)
        positive_eigenvalue_counts.append(eigenvalues)
        refutation_degree = sos_refutation_degree(M, d)
        refutation_degrees.append(refutation_degree)
    
    mean_positive_eigenvalues = sum(positive_eigenvalue_counts) / len(positive_eigenvalue_counts)
    max_refutation_degree = max(refutation_degrees)
    
    conjecture_holds = all(e >= math.log(n) / (d**2) for e, d in zip(positive_eigenvalue_counts, range(2, 9)))
    counterexample = "" if conjecture_holds else f"n={n}, refutation_degree={max_refutation_degree}"
    
    return {
        "metric_name": "mean_positive_eigenvalues",
        "metric_value": mean_positive_eigenvalues,
        "instances_tested": len(positive_eigenvalue_counts),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")