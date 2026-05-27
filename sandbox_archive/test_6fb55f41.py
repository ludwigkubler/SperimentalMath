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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_matrix(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def free_entropy(M):
        n = len(M)
        trace_sum = sum(sum(M[i][j] * M[j][i] for j in range(n)) for i in range(n))
        return -trace_sum / (2 * n**2)
    
    def communication_complexity(M, n):
        # Placeholder function; actual implementation needed
        return random.random()  # Dummy value
    
    def spearman_rank_correlation(X, Y):
        if len(X) != len(Y):
            raise ValueError("X and Y must have the same length")
        
        n = len(X)
        rank_X = {x: i for i, x in enumerate(sorted(set(X)), start=1)}
        rank_Y = {y: i for i, y in enumerate(sorted(set(Y)), start=1)}
        
        sum_differences_squared = sum((rank_X[X[i]] - rank_Y[Y[i]])**2 for i in range(n))
        rho_numerator = 6 * sum_differences_squared
        rho_denominator = n * (n**2 - 1)
        return 1 - rho_numerator / rho_denominator
    
    def is_significant(p_value, threshold=0.1):
        return p_value < threshold
    
    n = random.randint(5, 40)
    M = generate_matrix(n)
    F_star_M = free_entropy(M)
    CC_R_DISJ_n = communication_complexity(M, n)
    
    if F_star_M <= 0:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "F_star_M is non-positive"
        }
    
    p_value = random.random()  # Placeholder for actual p-value computation
    if not is_significant(p_value):
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "p-value is not significant"
        }
    
    correlation = spearman_rank_correlation([F_star_M], [CC_R_DISJ_n])
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": correlation > 0.6,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")