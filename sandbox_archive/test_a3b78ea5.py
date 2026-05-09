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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def determinant(A):
    n = len(A)
    det = 1.0
    U = [row[:] for row in A]
    gaussian_elimination(U)
    for i in range(n):
        det *= U[i][i]
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_name = "free_entropy"
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        M_n = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        
        # Map entries to non-commutative variables
        X = [[(M_n[i][j] + 1) / 2 for j in range(n)] for i in range(n)]
        
        # Compute eigenvalues using power iteration method
        def power_iteration(A, v0, tol=1e-6):
            v = v0
            while True:
                v_next = [sum(a * b for a, b in zip(row, v)) for row in A]
                norm_v_next = sum(x**2 for x in v_next)**0.5
                v_next = [x / norm_v_next for x in v_next]
                if abs(sum(v[i] * v_next[i] for i in range(n))) > 1 - tol:
                    break
                v = v_next
            return v
        
        def eigenvalues(A, num_eigs=10):
            v0 = [random.random() for _ in range(n)]
            eigvals = []
            for _ in range(num_eigs):
                v = power_iteration(A, v0)
                lambda_i = sum(a * b for a, b in zip(v, A @ v)) / sum(x**2 for x in v)
                eigvals.append(lambda_i)
                v0 = [x - lambda_i * y for x, y in zip(v, A)]
            return eigvals
        
        eigenvals = eigenvalues(X)
        
        # Compute empirical free entropy
        rho = [math.exp(-lambda_i) / sum(math.exp(-lambda_j) for lambda_j in eigenvals) for lambda_i in eigenvals]
        phi = -sum(rho[i] * math.log(rho[i]) for i in range(n))
        
        total_metric_value += phi
        instances_tested += n
    
    mean_metric_value = total_metric_value / instances_tested
    support_fraction = sum(1 for n in n_values if mean_metric_value >= 1 / (n * math.log(n))) / len(n_values)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"mean<{mean_metric_value} std<NA> support_fraction<{support_fraction}>"
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}**}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")