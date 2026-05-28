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
    
    def generate_read_twice_bp(n):
        width = random.randint(1, 40)
        return [random.choice([0, 1]) for _ in range(width)]
    
    def construct_crossed_product_algebra(bp):
        n = len(bp)
        M = [[0] * (n + 2) for _ in range(n + 2)]
        for i in range(n):
            M[i][i] = 1
            M[n][i] = bp[i]
            M[i][n] = -bp[i]
        return M
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            pivot_row = next(j for j in range(i, m) if matrix[j][i] != 0)
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            rank += 1
            for j in range(m):
                if j == i:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(n + 2):
                    matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def log_base_2(x):
        return math.log(x) / math.log(2)
    
    n = random.randint(1, 40)
    bp = generate_read_twice_bp(n)
    M = construct_crossed_product_algebra(bp)
    rank_M = matrix_rank(M)
    
    if rank_M == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rank_M_is_zero"
        }
    
    width_P = sum(bp)
    if width_P == 0:
        return {
            "metric_name": "minimal_rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "width_P_is_zero"
        }
    
    log_width_P = log_base_2(width_P)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank_M,
        "instances_tested": 1,
        "conjecture_holds": rank_M <= width_P and rank_M >= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    total_rank = sum(r['metric_value'] for r in results if r['instances_tested'] > 0)
    num_trials = len(results)
    mean_rank = total_rank / num_trials
    std_rank = math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results if r['instances_tested'] > 0) / (num_trials - 1))
    
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / num_trials
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['instances_tested'] > 0 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")