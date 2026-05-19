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
    
    def generate_random_graph(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiplication(A, B):
        n = len(A)
        C = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def gaussian_elimination(A, b):
        n = len(A)
        M = [A[i] + [b[i]] for i in range(n)]
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = M[i][i]
            for j in range(n + 1):
                M[i][j] /= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        return [row[-1] for row in M]
    
    def compute_eigenvalues(M):
        n = len(M)
        identity = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        eigenvalues = []
        for _ in range(10):  # Power iteration method
            v = [random.random() for _ in range(n)]
            v = [x / sum(v) for x in v]
            Mv = matrix_multiplication(M, v)
            lambda_ = sum(x * y for x, y in zip(Mv, v))
            eigenvalues.append(lambda_)
        return eigenvalues
    
    def sos_moment_matrix(G):
        n = len(G)
        M = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    M[i][i] += 1
                    M[j][j] += 1
                    M[i][j] -= 1
                    M[j][i] -= 1
        return M
    
    def check_eigenvalue_bound(eigenvalues):
        for lambda_ in eigenvalues:
            if lambda_ < -1 or lambda_ > 1:
                return False
        return True
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    G = generate_random_graph(n)
    M = sos_moment_matrix(G)
    eigenvalues = compute_eigenvalues(M)
    
    metric_value = sum(eigenvalues) / len(eigenvalues)
    conjecture_holds = check_eigenvalue_bound(eigenvalues)
    counterexample = "" if conjecture_holds else "eigenvalue_outside_interval"
    
    return {
        "metric_name": "mean_eigenvalue",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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