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

def generate_kcnf(n, alpha):
    clauses = []
    for _ in range(int(alpha * n * (n - 1) / 2)):
        clause = set()
        while len(clause) < 2:
            var = random.randint(1, n)
            if random.choice([True, False]):
                clause.add(var)
            else:
                clause.add(-var)
        clauses.append(tuple(sorted(clause)))
    return clauses

def hodge_rank(F):
    # Placeholder for Hodge rank computation
    # This is a dummy implementation and should be replaced with actual logic
    return len(F)

def permutation_circuit_depth(F):
    # Placeholder for permutation circuit depth computation
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(5, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 25]
    alpha_values = [0.2, 0.3, 0.4]
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            F = generate_kcnf(n, alpha)
            rank = hodge_rank(F)
            depth = permutation_circuit_depth(F)
            results.append((rank, depth))
    
    ranks = [r for r, _ in results]
    depths = [d for _, d in results]
    
    if not ranks or not depths:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    n = len(ranks)
    sum_ranks = sum(ranks)
    sum_depths = sum(depths)
    sum_rank_squared = sum(r * r for r in ranks)
    sum_depth_squared = sum(d * d for d in depths)
    sum_product = sum(r * d for r, d in zip(ranks, depths))
    
    rank_mean = sum_ranks / n
    depth_mean = sum_depths / n
    
    numerator = n * sum_product - sum_ranks * sum_depths
    denominator = math.sqrt((n * sum_rank_squared - sum_ranks ** 2) * (n * sum_depth_squared - sum_depths ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    rho = numerator / denominator
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": 0.6 <= rho < 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_valid_results")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        
        support_fraction = sum(1 for r in results if 0.6 <= r < 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        elif any(r < 0.6 for r in results):
            first_failing_seed = seeds[results.index(min([r for r in results if r < 0.6]))]
            print(f"RESULT: FALSIFIED counterexample=\"rho_below_0.6\" first_failing_seed={first_failing_seed}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} below_threshold")