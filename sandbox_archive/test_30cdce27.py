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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        r = 0
        for i in range(m):
            if all(abs(A[i][j]) < 1e-9 for j in range(n)):
                continue
            r += 1
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return r
    
    def communication_complexity_rank(M):
        n = len(M)
        rank_M = rank(gaussian_elimination(M))
        return rank_M
    
    def minimal_local_indeterminacy(M):
        n = len(M)
        rank_M = rank(gaussian_elimination(M))
        return n - rank_M
    
    instances_tested = 0
    total_alpha = 0
    total_r = 0
    max_n = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        alpha_M = minimal_local_indeterminacy(M)
        r_M = communication_complexity_rank(M)
        
        instances_tested += 1
        total_alpha += alpha_M
        total_r += r_M
        max_n = max(max_n, n)
    
    mean_alpha = total_alpha / instances_tested
    mean_r = total_r / instances_tested
    abs_diff_mean = abs(mean_alpha - mean_r) / instances_tested
    
    correlation_coefficient = 0
    for _ in range(30):
        n = random.randint(5, 40)
        M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        alpha_M = minimal_local_indeterminacy(M)
        r_M = communication_complexity_rank(M)
        
        correlation_coefficient += (alpha_M - mean_alpha) * (r_M - mean_r)
    
    correlation_coefficient /= instances_tested
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs_diff_mean <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")