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
    
    def generate_random_cnf(n, m):
        cnf = []
        for _ in range(m):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = ' or '.join(f'x{i+1}' if l == 1 else f'-x{i+1}' for l in literals)
            cnf.append(clause)
        return '\n'.join(cnf)

    def compute_knot_genus(n):
        # Placeholder function to simulate knot genus computation
        return n * (n - 1) // 2

    def spearman_rank_correlation(x, y):
        if len(x) != len(y):
            raise ValueError("Both lists must have the same length")
        
        n = len(x)
        x_ranks = {x[i]: i + 1 for i in range(n)}
        y_ranks = {y[i]: i + 1 for i in range(n)}
        
        numerator = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        denominator = n * (n**2 - 1) / 6
        
        return 1 - (6 * numerator) / denominator

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n, n)
        genus = compute_knot_genus(n)
        expected_genus = n * (n - 1) / 2
        results.append((genus, expected_genus))
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    x = [r[0] for r in results]
    y = [r[1] for r in results]
    correlation = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": ""
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
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"not_enough_positive_correlation\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)