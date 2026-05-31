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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_clause_complexity(cnf):
        return len(cnf)
    
    def construct_noncommutative_polynomial_representation(cnf):
        # Placeholder for actual noncommutative polynomial representation construction
        return random.random()  # Simplified as a random number for demonstration
    
    def compute_rank(R):
        # Placeholder for actual rank computation
        return R
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
        c = compute_clause_complexity(cnf)
        R = construct_noncommutative_polynomial_representation(cnf)
        rank_R = compute_rank(R)
        
        results.append({
            "n": n,
            "c": c,
            "rank_R": rank_R
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max([r["n"] for r in results]),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ranks = [r["rank_R"] for r in results]
    clause_complexities = [r["c"] for r in results]
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n))) * math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        return numerator / denominator if denominator != 0 else 0
    
    correlation_coefficient = pearson_correlation_coefficient(ranks, clause_complexities)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max([r["n"] for r in results]),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": "" if correlation_coefficient >= 0.6 else f"correlation_coefficient={correlation_coefficient}"
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
        mean_C = sum(r["metric_value"] for r in results) / len(results)
        std_C = math.sqrt(sum((r["metric_value"] - mean_C) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_C} std={std_C} support_fraction={support_fraction}")
    elif any(r["counterexample"] and float(r["counterexample"].split('=')[1]) < 0.6 for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if r["counterexample"] and float(r["counterexample"].split('=')[1]) < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")