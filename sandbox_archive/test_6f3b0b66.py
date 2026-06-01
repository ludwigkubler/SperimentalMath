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
        Q = [[A[i][j] for j in range(n)] for i in range(m)]
        R = [[0 if i != j else 1 for j in range(n)] for i in range(m)]
        
        for k in range(min(m, n)):
            norm = sum(Q[k][i]**2 for i in range(k, m))**0.5
            Q[k] = [Q[k][i] / norm for i in range(m)]
            
            for j in range(k+1, n):
                R[k][j] = sum(Q[k][i] * Q[i][j] for i in range(k, m))
                Q[j] = [Q[j][i] - R[k][j] * Q[k][i] for i in range(m)]
        
        return Q, R
    
    def von_neumann_entropy(rho):
        eigenvalues = [rho[i][i] for i in range(len(rho))]
        entropy = sum(-eigenvalue * math.log2(eigenvalue) if eigenvalue > 0 else 0 for eigenvalue in eigenvalues)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d1 = random.randint(2, n)
        d2 = random.randint(2, n)
        
        U = generate_unitary(d1)
        V = generate_unitary(d2)
        rho = [[U[i][k] * V[j][l] for l in range(d2)] for k in range(d1)]
        
        entropy = von_neumann_entropy(rho)
        min_dim = min(d1, d2)
        results.append((n, entropy, math.log2(min_dim)))
    
    if not results:
        return {
            "metric_name": "log_min_dimension",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_min_dims = [r[2] for r in results]
    entropies = [r[1] for r in results]
    
    mean_entropy = sum(entropies) / len(entropies)
    std_entropy = (sum((e - mean_entropy)**2 for e in entropies) / len(entropies))**0.5
    support_fraction = sum(e >= 0.5 * d for n, e, d in results) / len(results)
    
    return {
        "metric_name": "log_min_dimension",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")