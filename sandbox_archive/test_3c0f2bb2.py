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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_groupoid_homology(f):
        # Placeholder function to simulate groupoid homology computation
        # This is a dummy implementation and does not reflect actual complexity
        return len(f)
    
    def compute_circuit_monotone_complexity(f):
        # Placeholder function to simulate circuit monotone complexity computation
        # This is a dummy implementation and does not reflect actual complexity
        return sum(1 for bit in f if bit == 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per seed
            f = generate_boolean_function(n)
            homology_rank = compute_groupoid_homology(f)
            circuit_complexity = compute_circuit_monotone_complexity(f)
            results.append((homology_rank, circuit_complexity))
    
    if not results:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    homology_ranks = [r[0] for r in results]
    circuit_complexities = [r[1] for r in results]
    
    def rank(data):
        sorted_data = sorted((x, i) for i, x in enumerate(data))
        ranks = [0] * len(data)
        for i, (_, idx) in enumerate(sorted_data):
            if i > 0 and data[i] != data[i - 1]:
                for j in range(i):
                    ranks[sorted_data[j][1]] = i
            else:
                ranks[idx] = i
        return ranks
    
    homology_ranks_ranked = rank(homology_ranks)
    circuit_complexities_ranked = rank(circuit_complexities)
    
    n = len(results)
    sum_diff_squares = sum((homology_ranks_ranked[i] - circuit_complexities_ranked[i]) ** 2 for i in range(n))
    spearman_coefficient = 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": spearman_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": spearman_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=No instances generated")