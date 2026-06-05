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
    
    def generate_sat_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def compute_min_order(clauses):
        n = len(clauses[0])
        min_order = 0
        for i in range(n):
            if all(any(j != k and abs(clause[i]) == abs(clause[k]) for clause in clauses) for j in range(i + 1, n)):
                min_order += 1
        return min_order
    
    def compute_entropy(subset):
        counts = [0] * (n + 1)
        for clause in subset:
            for literal in clause:
                counts[abs(literal)] += 1
        total_literals = sum(counts)
        entropy = 0.0
        for count in counts:
            if count > 0:
                p = Fraction(count, total_literals)
                entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(n, 2*n)  # Ensure at least one clause per variable
        clauses = generate_sat_instance(n, m)
        subset_size = min(m, 10)  # Ensure non-empty subset
        subset = random.sample(clauses, subset_size)
        
        min_order = compute_min_order(clauses)
        entropy = compute_entropy(subset)
        
        results.append({
            "n": n,
            "min_order": min_order,
            "entropy": entropy
        })
    
    if len(results) < 30:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        ranks_x = [sorted(x).index(xi) + 1 for xi in x]
        ranks_y = [sorted(y).index(yi) + 1 for yi in y]
        sum_diff_squares = sum((ranks_x[i] - ranks_y[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    x = [result["min_order"] for result in results]
    y = [result["entropy"] for result in results]
    correlation_coefficient = spearman_rank_correlation(x, y)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")