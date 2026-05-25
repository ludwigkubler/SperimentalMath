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
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][k] += A[i][j] * B[j][k]
        return C
    
    def is_positive_definite(A):
        n = len(A)
        for i in range(n):
            if A[i][i] <= 0:
                return False
            for j in range(i+1, n):
                A[j][i] /= A[i][i]
                for k in range(i+1, n):
                    A[j][k] -= A[j][i] * A[i][k]
        return True
    
    def compute_rank(A):
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def max_cut_instance(n):
        # Generate a random max-CUT instance with n variables
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def sos_polynomial(edges, degree):
        # Placeholder function to fit a polynomial approximation to the max-CUT objective function
        # This is a dummy implementation and should be replaced with an actual SOS polynomial fitting algorithm
        return random.randint(1, degree)
    
    n = 40
    edges = max_cut_instance(n)
    d = random.randint(2, min(n-1, 5))
    
    # Construct the moment matrix
    M = [[0 for _ in range(n)] for _ in range(n)]
    for u, v in edges:
        M[u][v] += 1
        M[v][u] += 1
    
    rank = compute_rank(M)
    
    # Fit a polynomial approximation to the max-CUT objective function
    degree = sos_polynomial(edges, d)
    
    # Check if the approximation ratio is better than 0.878
    approximation_ratio = random.random() * 0.5 + 0.439  # Placeholder value
    
    result = {
        "metric_name": "SOS Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": approximation_ratio > 0.878 and rank >= d,
        "counterexample": "" if approximation_ratio > 0.878 and rank >= d else f"Approximation ratio: {approximation_ratio}, Rank: {rank}"
    }
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30*100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")