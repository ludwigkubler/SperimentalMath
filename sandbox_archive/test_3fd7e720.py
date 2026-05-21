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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            if A[i][i] == 0:
                return None  # Singular matrix, no unique solution
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n + 1):
                    A[j][k] -= factor * A[i][k]
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (A[i][-1] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def eigenvalues(M):
        n = len(M)
        if n == 0:
            return []
        if n == 1:
            return [M[0][0]]
        
        # Compute characteristic polynomial using cofactor expansion
        det = 0
        for j in range(n):
            M_minor = [[M[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * M[0][j] * determinant(M_minor)
        
        # Find roots of the characteristic polynomial
        eigenvals = []
        if n == 2:
            a, b, c = M[0][0], M[0][1], M[1][0]
            det = a * M[1][1] - b * c
            trace = a + M[1][1]
            lambda1 = (trace + math.sqrt(trace ** 2 - 4 * det)) / 2
            lambda2 = (trace - math.sqrt(trace ** 2 - 4 * det)) / 2
            eigenvals.extend([lambda1, lambda2])
        else:
            # Use a numerical method to find roots of the polynomial
            # This is a simplified version and may not be accurate for large n
            p = [det]
            for i in range(n):
                p.append(-sum(M[i][j] * p[j - 1] for j in range(1, i + 1)))
            eigenvals = find_roots(p)
        
        return eigenvals
    
    def determinant(A):
        n = len(A)
        if n == 0:
            return 1
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            M_minor = [[A[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * A[0][j] * determinant(M_minor)
        return det
    
    def find_roots(p):
        # Use a simple numerical method to find roots of the polynomial
        # This is a simplified version and may not be accurate for large n
        n = len(p) - 1
        if n == 0:
            return []
        if n == 1:
            return [-p[0] / p[1]]
        
        # Use Newton's method to find roots
        x = [random.uniform(-1, 1) for _ in range(n)]
        tol = 1e-6
        max_iter = 1000
        for _ in range(max_iter):
            f = sum(p[i] * x[i]**(n - i) for i in range(n + 1))
            df = sum((n - i) * p[i] * x[i]**(n - i - 1) for i in range(n + 1))
            if abs(df) < tol:
                break
            x = [x_i - f_i / df_i for x_i, f_i, df_i in zip(x, f, df)]
        return x
    
    def disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] = random.choice([0, 1])
                M[j][i] = M[i][j]
        return M
    
    n = random.randint(5, 40)
    M = disjointness_matrix(n)
    eigenvals = eigenvalues(M)
    
    if eigenvals is None:
        return {
            "metric_name": "free_entropy",
            "metric_value": float('nan'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    free_entropy = sum(math.log(abs(lambda_)) for lambda_ in eigenvals)
    metric_value = free_entropy
    
    return {
        "metric_name": "free_entropy",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value >= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"free_entropy < n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")