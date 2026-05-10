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
# end SEC prelude

import random
import math
from typing import List, Dict

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    
    def generate_max_cut_instance(n: int) -> List[List[int]]:
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def matrix_multiply(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        n = len(A)
        C = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def spectral_norm(M: List[List[float]]) -> float:
        n = len(M)
        v = [1.0 / math.sqrt(n)] * n
        for _ in range(100):  # Power iteration method
            v_next = matrix_multiply(M, v)
            norm_v_next = sum(x**2 for x in v_next) ** 0.5
            v = [x / norm_v_next for x in v_next]
        return abs(v[0])
    
    def moment_matrix(instance: List[List[int]], d: int) -> List[List[float]]:
        n = len(instance)
        M = [[0.0] * (n + 1) for _ in range(n + 1)]
        M[0][0] = 1.0
        for i in range(n):
            for j in range(i, n):
                M[i+1][j+1] = instance[i][j]
                M[j+1][i+1] = instance[i][j]
        for k in range(2, d + 1):
            new_M = [[0.0] * (n + 1) for _ in range(n + 1)]
            for i in range(n):
                for j in range(i, n):
                    for l in range(j, n):
                        new_M[i+1][j+1] += instance[i][l] * M[j+1][k-1+l]
                        new_M[j+1][i+1] += instance[i][l] * M[j+1][k-1+l]
            M = new_M
        return M
    
    n = random.randint(5, 40)
    instance = generate_max_cut_instance(n)
    d = 5
    M_d = moment_matrix(instance, d)
    spectral_norm_M_d = spectral_norm(M_d)
    
    if spectral_norm_M_d < 0.9 * math.sqrt(n):
        return {
            "metric_name": "spectral_norm",
            "metric_value": spectral_norm_M_d,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "spectral norm too small"
        }
    else:
        return {
            "metric_name": "spectral_norm",
            "metric_value": spectral_norm_M_d,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='spectral norm too small' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")