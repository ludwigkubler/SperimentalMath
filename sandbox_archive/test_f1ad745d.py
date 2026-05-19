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

def generate_disjointness_matrix(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                M[i][j] = 1
                M[j][i] = 1
    return M

def get_minors(matrix, k):
    if k == 0:
        return []
    minors = []
    for indices in combinations(range(len(matrix)), k):
        submatrix = [[matrix[i][j] for j in indices] for i in indices]
        minors.append(submatrix)
    return minors

def secant_rank(matrix):
    n = len(matrix)
    minors = get_minors(matrix, 1)
    max_det = 0
    for minor in minors:
        det = minor[0][0]
        if abs(det) > max_det:
            max_det = abs(det)
    return max_det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        M_n = generate_disjointness_matrix(n)
        sr_M_n = secant_rank(M_n)
        if sr_M_n < 0.8 * n:
            return {
                "metric_name": "secant_rank",
                "metric_value": sr_M_n,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, sr(M_n)={sr_M_n}"
            }
        results.append(sr_M_n)
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    return {
        "metric_name": "secant_rank",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8 * n_values[-1]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='n={n_values[-1]}, sr(M_n)<0.8n' first_failing_seed={first_failing_seed}")