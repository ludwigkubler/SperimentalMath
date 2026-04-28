# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def matrix_rank(M):
        m, n = len(M), len(M[0])
        rank = 0
        for i in range(m):
            if any(M[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    M[i][j] /= M[i][j]
                for k in range(m):
                    if k != i and any(M[k][j] != 0 for j in range(n)):
                        for j in range(n):
                            M[k][j] -= M[k][i] * M[i][j]
        return rank
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                    max_row = j
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            factor = 1 / augmented[i][i]
            for j in range(n + 1):
                augmented[i][j] *= factor
            for j in range(m):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(n + 1):
                        augmented[j][k] -= factor * augmented[i][k]
        return [row[-1] for row in augmented]
    
    def is_linearly_independent(vectors):
        m, n = len(vectors), len(vectors[0])
        A = [vectors[i] + [1] for i in range(m)]
        return matrix_rank(A) == n
    
    def min_1_certificates(f, k):
        certificates = []
        for alpha in itertools.product([0, 1], repeat=k):
            if f(alpha) == 1:
                certificates.append(alpha)
        return certificates
    
    def sunflower_size(certificates):
        max_size = 0
        for i in range(len(certificates)):
            core = set()
            petals = []
            for j in range(i+1, len(certificates)):
                common_part = set(zip(certificates[i], certificates[j]))
                if not core.intersection(common_part):
                    core.update(common_part)
                    petals.append(set(certificates[j]) - core)
            max_size = max(max_size, len(core) + len(petals))
        return max_size
    
    def f(alpha):
        return alpha[0] ^ alpha[1]
    
    k_values = [2, 3, 4]
    results = []
    
    for k in k_values:
        if k == 4:
            functions = [f for _ in range(2000)] + [lambda x: x[0] == x[1]] + [lambda x: x[0] != x[1]]
        else:
            functions = [lambda alpha, f=f: all(f(alpha[:i] + (b,) + alpha[i+1:]) == 1 for b in [0, 1]) for alpha in itertools.product([0, 1], repeat=k)]
        
        for f in functions:
            certificates = min_1_certificates(f, k)
            r_f = sunflower_size(certificates)
            M = [[f(alpha[:i] + (j,) + alpha[i+1:]) for j in range(2**k)] for i in range(k)]
            rk_M = matrix_rank(M)
            results.append((r_f, rk_M))
    
    metric_name = "log_rk_ratio"
    metric_value = sum(math.log2(r) - math.ceil(math.log2(rk)) for r, rk in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(math.log2(r) <= math.ceil(math.log2(rk)) for r, rk in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"SEED": seed, **result}))
    
    results = [run_trial(seed) for seed in seeds]
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")