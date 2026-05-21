# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

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

def matrix_multiply(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def determinant(A):
    n = len(A)
    if n == 1:
        return A[0][0]
    det = 0
    sign = 1
    for j in range(n):
        det += sign * A[0][j] * determinant([row[:j] + row[j+1:] for row in A[1:]])
        sign *= -1
    return det

def gromov_hyperbolicity(F):
    n = len(F)
    d = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        d[i][j] = abs(sum(1 for clause in F if (i+1) in clause and (j+1) not in clause) - sum(1 for clause in F if (i+1) not in clause and (j+1) in clause))
    
    max_ratio = 0
    for i, j, k, l in combinations(range(n), 4):
        d1, d2, d3, d4 = d[i][j], d[i][k], d[j][l], d[k][l]
        M = sorted([d1 + d2, d1 + d3, d2 + d4, d3 + d4])
        if M[0] == 0 or M[1] == 0:
            continue
        max_ratio = max(max_ratio, (M[2] - M[3]) / (2 * max(d1, d2, d3, d4)))
    
    return max_ratio

def run_trial(seed: int) -> dict:
    random.seed(seed)
    v = random.choice([8, 10, 12, 14, 16, 18, 20])
    n = v * (v - 1) // 2
    k = math.isqrt(v)
    
    # Construct F_clique
    F_clique = []
    for i in range(n):
        for j in range(i+1, n):
            if len(set(range(k)) & set([i, j])) == k:
                F_clique.append({i, j})
    
    delta_F_clique = gromov_hyperbolicity(F_clique)
    if delta_F_clique < 0.2:
        return {
            "metric_name": "delta_F_clique",
            "metric_value": delta_F_clique,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "F_clique has low Gromov hyperbolicity"
        }
    
    # Construct F_rand
    instances = []
    for _ in range(30):
        F_rand = set()
        while len(F_rand) < len(F_clique):
            clause = random.sample(range(n), k)
            if all(len(set(clause) & set(existing_clause)) == 2 for existing_clause in F_rand):
                F_rand.add(tuple(sorted(clause)))
        
        delta_F_rand = gromov_hyperbolicity(list(F_rand))
        instances.append(delta_F_rand)
    
    mean_delta_F_rand = sum(instances) / len(instances)
    R_v = delta_F_clique / mean_delta_F_rand
    
    return {
        "metric_name": "R_v",
        "metric_value": R_v,
        "instances_tested": 30,
        "conjecture_holds": R_v >= 0.3 * math.sqrt(v) / math.log(v),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"R_v < 0.3 * sqrt(v) / log(v)\" first_failing_seed={first_failing_seed}")