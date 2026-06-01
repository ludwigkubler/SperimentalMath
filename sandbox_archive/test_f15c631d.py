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
        U = [[random.gauss(0, 1) for _ in range(d)] for _ in range(d)]
        Q, R = qr_decomposition(U)
        return Q
    
    def qr_decomposition(A):
        m, n = len(A), len(A[0])
        Q = [[0] * n for _ in range(m)]
        R = copy_matrix(A)
        
        for j in range(n):
            s = 0
            for i in range(j, m):
                s += R[i][j] ** 2
            s = math.sqrt(s)
            
            if s == 0:
                continue
            
            Q[j][j] = R[j][j] / s
            for k in range(j + 1, n):
                Q[k][j] = R[k][j] / s
            
            for i in range(m):
                R[i][j] /= s
            
            for i in range(j + 1, m):
                c = 0
                for k in range(n):
                    c += Q[k][j] * R[i][k]
                
                for k in range(n):
                    R[i][k] -= 2 * c * Q[k][j]
        
        return Q, R
    
    def copy_matrix(A):
        m = len(A)
        n = len(A[0])
        B = [[A[i][j] for j in range(n)] for i in range(m)]
        return B
    
    def trace(A):
        return sum(A[i][i] for i in range(len(A)))
    
    def von_neumann_entropy(rho):
        eigenvalues = [rho[i][i] for i in range(len(rho))]
        entropy = 0
        for lambda_i in eigenvalues:
            if lambda_i > 0:
                entropy -= lambda_i * math.log(lambda_i)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0.0
    min_d = float('inf')
    
    for n in n_values:
        d1 = random.randint(2, n)
        d2 = random.randint(2, n)
        U = generate_unitary(d1)
        V = generate_unitary(d2)
        
        rho = [[U[i][k] * V[j][l] for l in range(d2)] for k in range(d1)]
        entropy = von_neumann_entropy(rho)
        
        instances_tested += 1
        total_entropy += entropy
        min_d = min(min_d, d1, d2)
    
    mean_entropy = total_entropy / instances_tested
    
    conjecture_holds = all(mean_entropy >= 0.5 * math.log(min_d) for _ in range(30))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "von_neumann_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")