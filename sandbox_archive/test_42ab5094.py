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
        U = [[random.random() for _ in range(d)] for _ in range(d)]
        # Perform QR decomposition to get a unitary matrix
        Q, R = qr_decomposition(U)
        return Q
    
    def qr_decomposition(A):
        d = len(A)
        Q = [[0] * d for _ in range(d)]
        R = A.copy()
        for k in range(d):
            norm = 0
            for i in range(k, d):
                norm += R[i][k] ** 2
            norm = math.sqrt(norm)
            if norm == 0:
                continue
            Q[k][k] = R[k][k] / norm
            for j in range(k + 1, d):
                Q[j][k] = R[j][k] / norm
            for i in range(d):
                R[i][k] /= norm
            for j in range(k + 1, d):
                R[i][j] -= Q[i][k] * R[k][j]
        return Q, R
    
    def von_neumann_entropy(rho):
        eigenvalues = [rho[i][i] for i in range(len(rho))]
        entropy = -sum(eigenvalue * math.log2(eigenvalue) for eigenvalue in eigenvalues if eigenvalue > 0)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d1 = n
        d2 = n
        U = generate_unitary(d1)
        V = generate_unitary(d2)
        rho = [[U[i][k] * V[j][l] for l in range(d2)] for k in range(d1)]
        
        entropy = von_neumann_entropy(rho)
        results.append(entropy)
    
    mean_entropy = sum(results) / len(results)
    min_d = min(n_values)
    lower_bound = 0.5 * math.log2(min_d)
    
    conjecture_holds = all(entropy >= lower_bound for entropy in results)
    counterexample = "" if conjecture_holds else "lower_bound_violation"
    
    return {
        "metric_name": "Von Neumann Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"lower_bound_violation\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")