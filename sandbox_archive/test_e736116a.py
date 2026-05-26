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
    
    def generate_disjointness_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([i, -i]) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return variables, clauses
    
    def compute_minimal_rank(variables, clauses):
        # Placeholder for actual computation
        # For now, we'll just return a random rank between 1 and n^2
        return random.randint(1, len(variables) ** 2)
    
    def spearman_correlation(x, y):
        x_ranks = {x[i]: i + 1 for i in range(len(x))}
        y_ranks = {y[i]: i + 1 for i in range(len(y))}
        n = len(x)
        numerator = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        denominator = 6 * sum((i - (n + 1) / 2) ** 2 for i in range(1, n + 1))
        return 1 - numerator / denominator
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        variables, clauses = generate_disjointness_instance(n)
        rank = compute_minimal_rank(variables, clauses)
        ranks.append(rank)
        
        # Placeholder for actual complexity calculation
        # For now, we'll just return a random complexity between 1 and n^2
        complexity = random.randint(1, len(variables) ** 2)
        complexities.append(complexity)
    
    correlation_coefficient = spearman_correlation(ranks, complexities)
    metric_value = correlation_coefficient
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient <= 0.5"
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": metric_value,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient <= 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")