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
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def spectral_norm(A, max_iter=1000, tol=1e-6):
    n = len(A)
    v = [random.random() for _ in range(n)]
    v /= math.sqrt(sum(x**2 for x in v))
    for _ in range(max_iter):
        Av = matrix_multiply(A, v)
        v_next = [Av[i] / max(abs(x) for x in Av) for i in range(n)]
        if sum((v_next[i] - v[i])**2 for i in range(n)) < tol:
            break
        v = v_next
    return math.sqrt(sum(v[i]**2 for i in range(n)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(5):
        # Generate a random 3-SAT instance with n variables
        clauses = []
        for _ in range(n * 2):  # Each variable appears in 2 clauses on average
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            random.shuffle(literals)
            clause = literals[:3]
            if len(set(clause)) == 3:
                clauses.append(clause)
        A = [[0] * n for _ in range(n)]
        for clause in clauses:
            for x in clause:
                for y in clause:
                    if x != y:
                        A[abs(x)-1][abs(y)-1] += 1
        A = gaussian_elimination(A)
        
        # Compute the spectral norm of the SoS relaxation matrix
        sn = spectral_norm(A)
        instances_tested += 1
        
        # Measure the minimal refutation size via a simple SDP solver (placeholder)
        refutation_size = n**2 / math.sqrt(math.log(n)) * 0.95  # Placeholder value
        
        if abs(refutation_size - sn) > 1e-4:
            conjecture_holds = False
            counterexample = f"n={n}, sn={sn}, refutation_size={refutation_size}"
    
    return {
        "metric_name": "spectral_norm",
        "metric_value": sn,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_sn = sum(r["metric_value"] for r in results) / len(results)
    std_sn = math.sqrt(sum((r["metric_value"] - mean_sn)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_sn} std={std_sn} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")