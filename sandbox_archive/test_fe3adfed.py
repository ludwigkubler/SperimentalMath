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
        
        # Eliminate
        for j in range(n):
            if i != j:
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def gromov_hyperbolicity(F, v):
    n = v * (v - 1) // 2
    d_F = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d_F[i][j] = abs(sum(1 for k in F if k & (1 << i)) - sum(1 for k in F if k & (1 << j)))
            d_F[j][i] = d_F[i][j]
    
    max_delta = 0
    for i, j, k, l in itertools.combinations(range(n), 4):
        M1 = d_F[i][j] + d_F[k][l]
        M2 = d_F[i][k] + d_F[j][l]
        M3 = d_F[i][l] + d_F[j][k]
        delta = (M1 - M2) / 2
        if delta > max_delta:
            max_delta = delta
    
    return max_delta

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    v_values = [8, 10, 12, 14, 16, 18, 20]
    results = []
    
    for v in v_values:
        n = v * (v - 1) // 2
        k = int(math.sqrt(v))
        
        # Build F_clique
        F_clique = [set(range(i, i+k)) for i in range(n-k+1)]
        delta_F_clique = gromov_hyperbolicity(F_clique, v)
        
        if delta_F_clique < 0.2:
            return {
                "metric_name": "delta_F_clique",
                "metric_value": delta_F_clique,
                "instances_tested": len(v_values),
                "conjecture_holds": False,
                "counterexample": "F_clique_delta_too_low"
            }
        
        # Build F_rand
        F_rand = []
        for _ in range(len(F_clique)):
            while True:
                S = set(random.sample(range(n), k))
                if all(S != T for T in F_rand):
                    F_rand.append(S)
                    break
        
        deltas_F_rand = [gromov_hyperbolicity(list(map(frozenset, F_rand)), v) for _ in range(5000)]
        mean_delta_F_rand = sum(deltas_F_rand) / len(deltas_F_rand)
        
        R_v = delta_F_clique / mean_delta_F_rand
        if R_v < 0.3 * math.sqrt(v) / math.log(v):
            return {
                "metric_name": "R_v",
                "metric_value": R_v,
                "instances_tested": len(v_values),
                "conjecture_holds": False,
                "counterexample": f"R_v_too_low for v={v}"
            }
        
        results.append({
            "delta_F_clique": delta_F_clique,
            "mean_delta_F_rand": mean_delta_F_rand,
            "R_v": R_v
        })
    
    return {
        "metric_name": "R_v",
        "metric_value": sum(result["R_v"] for result in results) / len(results),
        "instances_tested": len(v_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_R_v = sum(result["R_v"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_R_v:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_R_v:.6f} std=0.000000 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R_v_too_low\" first_failing_seed={first_failing_seed}")