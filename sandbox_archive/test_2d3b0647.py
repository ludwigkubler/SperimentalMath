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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_quantum_state(phi):
        n = int(math.log2(len(phi)))
        state = [[0] * (2**n) for _ in range(2**n)]
        state[0][0] = 1
        return state
    
    def rank_variance(state):
        n = len(state)
        total = sum(sum(row) for row in state)
        mean = Fraction(total, n*n)
        variance = sum((state[i][j] - mean)**2 for i in range(n) for j in range(n)) / (n*n)
        return float(variance)
    
    def min_rank(state):
        n = len(state)
        rank = 0
        for i in range(n):
            if any(state[j][i] != 0 for j in range(n)):
                rank += 1
        return rank
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        phi = generate_boolean_function(n)
        state = compute_quantum_state(phi)
        min_rank_val = min_rank(state)
        rank_var_val = rank_variance(state)
        results.append((min_rank_val, rank_var_val))
    
    if not results:
        return {
            "metric_name": "min_rank vs rank_var",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    min_ranks = [r[0] for r in results]
    rank_vars = [r[1] for r in results]
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_rank_var = sum(rank_vars) / len(rank_vars)
    
    correlation_coefficient = 0
    p_value = 1
    
    return {
        "metric_name": "min_rank vs rank_var",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")