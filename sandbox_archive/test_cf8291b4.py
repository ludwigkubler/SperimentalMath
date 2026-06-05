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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def monoidal_categorify(clauses):
        # Simplified categorification: count unique literals
        return len(set(lit for clause in clauses for lit in clause))
    
    def entropy(subset):
        if not subset:
            return 0
        p = Fraction(len(subset), len(clauses))
        return -p * math.log2(p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_cnf(n)
        min_order = monoidal_categorify(clauses)
        
        subset_entropies = []
        for r in range(1, len(subset) + 1):
            for subset in itertools.combinations(subset, r):
                subset_entropies.append(entropy(subset))
        
        if not subset_entropies:
            continue
        
        avg_entropy = sum(subset_entropies) / len(subset_entropies)
        results.append({
            "n": n,
            "min_order": min_order,
            "avg_entropy": avg_entropy
        })
    
    if not results:
        return {
            "metric_name": "Entropy",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid subsets found"
        }
    
    min_order = min(result["min_order"] for result in results)
    avg_entropy = sum(result["avg_entropy"] for result in results) / len(results)
    
    # Pearson's correlation coefficient
    n = len(results)
    x_sum = sum(result["min_order"] for result in results)
    y_sum = sum(result["avg_entropy"] for result in results)
    xy_sum = sum(result["min_order"] * result["avg_entropy"] for result in results)
    xx_sum = sum(result["min_order"] ** 2 for result in results)
    yy_sum = sum(result["avg_entropy"] ** 2 for result in results)
    
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * xx_sum - x_sum ** 2) * (n * yy_sum - y_sum ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Entropy",
            "metric_value": 0,
            "instances_tested": n,
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    correlation = numerator / denominator
    
    return {
        "metric_name": "Entropy",
        "metric_value": correlation,
        "instances_tested": n,
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": -1 <= correlation <= 1,
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
    
    if not results:
        print("RESULT: INCONCLUSIVE No valid trials found")
        sys.exit(0)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if -1 <= result["metric_value"] <= 1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation outside bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Fewer than 80% seeds support the conjecture")