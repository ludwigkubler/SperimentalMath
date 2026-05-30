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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_random_matrix(N):
    return [[random.choice([0, 1]) for _ in range(N)] for _ in range(N)]

def hyperbolic_metric_diameter(M):
    N = len(M)
    max_dist = 0
    for i in range(N):
        for j in range(i + 1, N):
            dist = sum(abs(M[i][k] - M[j][k]) for k in range(N))
            if dist > max_dist:
                max_dist = dist
    return max_dist

def randomized_two_party_communication_complexity(M):
    N = len(M)
    # Simplified model: each bit requires 1 unit of communication
    return sum(sum(row) for row in M)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        N = n
        M = generate_random_matrix(N)
        d_H = hyperbolic_metric_diameter(M)
        CC_R = randomized_two_party_communication_complexity(M)
        results.append((d_H, CC_R))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    # Calculate Spearman rank correlation coefficient
    ranks_d_H = {d_H: i for i, (d_H, _) in enumerate(sorted(set(d_H for d_H, _ in results)), start=1)}
    ranks_CC_R = {CC_R: i for i, (_, CC_R) in enumerate(sorted(set(CC_R for _, CC_R in results)), start=1)}
    
    n = len(results)
    rho_numerator = sum((ranks_d_H[d_H] - ranks_CC_R[CC_R]) ** 2 for d_H, CC_R in results)
    rho_denominator = (n * (n**2 - 1)) / 12
    rho = 1 - (6 * rho_numerator) / rho_denominator
    
    return {
        "metric_name": "Spearman rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": n,
        "n_max": max(n for _, n in results),
        "conjecture_holds": rho >= 0.8 and rho <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_rho = sum(result["metric_value"] for result in results) / len(results)
        std_rho = math.sqrt(sum((result["metric_value"] - mean_rho) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction=1.0")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation coefficient does not meet the threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no trials supported")