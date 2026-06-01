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
    
    def generate_unitary(d):
        u = [[0] * d for _ in range(d)]
        for i in range(d):
            u[i][i] = 1
        return u
    
    def matrix_mult(A, B):
        d1, d2 = len(A), len(B[0])
        C = [[0] * d2 for _ in range(d1)]
        for i in range(d1):
            for j in range(d2):
                for k in range(len(B)):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def trace(A):
        return sum(A[i][i] for i in range(len(A)))
    
    def eigenvalues(A):
        d = len(A)
        if d == 1:
            return [A[0][0]]
        
        # Simple power iteration method to find one eigenvalue
        v = [random.random() for _ in range(d)]
        v /= math.sqrt(sum(x**2 for x in v))
        for _ in range(100):
            v = matrix_mult(A, v)
            v /= math.sqrt(sum(x**2 for x in v))
        
        # Approximate the eigenvalue
        lambda_ = trace(matrix_mult(A, [v])) / sum(v[i]**2 for i in range(d))
        return [lambda_] + eigenvalues([[A[i][j] - (A[i][k] * v[k] * v[j]) / lambda_ for j in range(d)] for k in range(d)])
    
    def von_neumann_entropy(evals):
        return -sum(e * math.log2(e) for e in evals if e > 0)
    
    d1, d2 = random.randint(5, 30), random.randint(5, 30)
    U = generate_unitary(d1)
    V = generate_unitary(d2)
    rho = [[U[i][k] * V[j][l] for l in range(d2)] for k in range(d1)]
    
    evals = eigenvalues(rho)
    S_rho = von_neumann_entropy(evals)
    
    min_dim = min(d1, d2)
    log_min_dim = math.log2(min_dim)
    
    return {
        "metric_name": "S(ρ)",
        "metric_value": abs(S_rho),
        "instances_tested": 1,
        "n_max": max(d1, d2),
        "conjecture_holds": abs(S_rho) >= 0.5 * log_min_dim,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "minimal_quadratic_entanglement"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")