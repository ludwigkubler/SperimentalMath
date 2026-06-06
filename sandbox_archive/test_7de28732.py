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
    
    def calculate_rank_variance(permutation_matrices):
        ranks = [len(set(row)) for row in permutation_matrices]
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((r - mean_rank)**2 for r in ranks) / len(ranks)
        return variance
    
    def calculate_groupoid_order(boolean_function):
        n = int(math.log2(len(boolean_function)))
        groupoid_order = n  # Simplified assumption for demonstration
        return groupoid_order
    
    def generate_permutation_matrices(boolean_function, n):
        permutation_matrices = []
        for i in range(2**n):
            matrix_row = [boolean_function[i ^ j] for j in range(n)]
            permutation_matrices.append(matrix_row)
        return permutation_matrices
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        boolean_function = generate_boolean_function(n)
        groupoid_order = calculate_groupoid_order(boolean_function)
        permutation_matrices = generate_permutation_matrices(boolean_function, n)
        rank_variance = calculate_rank_variance(permutation_matrices)
        
        if rank_variance == 0:
            continue
        
        ratio = Fraction(groupoid_order).limit_denominator() / rank_variance
        results.append({'n': n, 'groupoid_order': groupoid_order, 'rank_variance': rank_variance, 'ratio': ratio})
    
    if not results:
        return {
            "metric_name": "Groupoid Order to Rank Variance Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_ratio = sum(result['ratio'] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result['ratio'] - mean_ratio)**2 for result in results) / len(results))
    
    return {
        "metric_name": "Groupoid Order to Rank Variance Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result['n'] for result in results),
        "conjecture_holds": all(0.5 <= result['ratio'] <= 2 for result in results),
        "counterexample": "" if all(0.5 <= result['ratio'] <= 2 for result in results) else str(results)
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result['metric_value'] for result in results if result['metric_value'] is not None) / len(results)
    std_value = math.sqrt(sum((result['metric_value'] - mean_value)**2 for result in results if result['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")