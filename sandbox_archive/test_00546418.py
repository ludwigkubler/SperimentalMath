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
    
    def generate_bp(S, m):
        layers = [random.sample(range(S), S) for _ in range(m)]
        A = [[0] * S for _ in range(m)]
        B = [[0] * S for _ in range(m)]
        
        for i in range(m):
            for j in range(S):
                A[i][j] = random.choice([0, 1])
                B[i][j] = random.choice([0, 1])
        
        return layers, A, B
    
    def matrix_multiply(A, B):
        S = len(A)
        C = [[0] * S for _ in range(S)]
        for i in range(S):
            for j in range(S):
                for k in range(S):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def frobenius_norm(A):
        S = len(A)
        norm = 0
        for i in range(S):
            for j in range(S):
                norm += A[i][j] ** 2
        return math.sqrt(norm)
    
    def compute_rho(C):
        max_norm = max(frobenius_norm(row) for row in C)
        return math.log2(1 + max_norm ** 2)
    
    def is_ip2(n):
        layers = [[i, i+1] for i in range(n)]
        A = [[0 if j != k else 1 for j in range(2**n)] for k in range(2**n)]
        B = [[0 if j != k else 1 for j in range(2**n)] for k in range(2**n)]
        return layers, A, B
    
    sizes = [8, 16, 32, 64]
    var_counts = [8, 12, 16, 20]
    alpha = 4
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for S in sizes:
        for m in var_counts:
            layers, A, B = generate_bp(S, m)
            C = [matrix_multiply(A[i], B[i]) - matrix_multiply(B[i], A[i]) for i in range(m)]
            rho = compute_rho(C)
            
            instances_tested += 1
            if rho > alpha * math.log2(S):
                conjecture_holds = False
                counterexample = f"Random BP of size {S} with m={m} variables, ρ(P) = {rho}"
    
    # IP_2 calibration points
    ip2_sizes = [3, 4, 5, 6]
    for n in ip2_sizes:
        layers, A, B = is_ip2(n)
        C = [matrix_multiply(A[i], B[i]) - matrix_multiply(B[i], A[i]) for i in range(n)]
        rho = compute_rho(C)
        
        instances_tested += 1
        if rho < n / 4:
            conjecture_holds = False
            counterexample = f"IP_2 BP of size {2**n}, ρ(P) = {rho}"
    
    return {
        "metric_name": "ρ(P)",
        "metric_value": compute_rho(C),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")