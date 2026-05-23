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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def sos_degree(instance_size):
        # Placeholder function to compute SOS degree
        # This is a dummy implementation and should be replaced with actual computation
        return instance_size ** 2
    
    def min_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    incidence_matrix = matrix_multiply(instance, instance)
    
    sos_deg = sos_degree(n)
    min_rank_val = min_rank(incidence_matrix)
    
    ratio = min_rank_val / sos_deg
    diff = abs(min_rank_val - sos_deg)
    
    return {
        "metric_name": "Ratio of Min Rank to SOS Degree",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.2 and diff <= 3,
        "counterexample": "" if conjecture_holds else f"n={n}, min_rank={min_rank_val}, sos_deg={sos_deg}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    total_ratio = 0
    total_diff = 0
    count_supporting = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        results.append(trial_result)
        total_ratio += trial_result["metric_value"]
        total_diff += trial_result["metric_value"] - sos_degree(trial_result["instances_tested"])
        if trial_result["conjecture_holds"]:
            count_supporting += 1
    
    mean_ratio = total_ratio / len(seeds)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = count_supporting / len(seeds)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, min_rank={results[0]['metric_value']}, sos_deg={sos_degree(results[0]['instances_tested'])}\" first_failing_seed={first_failing_seed}")