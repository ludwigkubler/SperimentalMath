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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank_var = 0
        for i in range(n + 1):
            count = sum(1 for x in f if bin(x).count('1') == i)
            rank_var += (i - n / 2) ** 2 * count / (2**n)
        return rank_var
    
    def hodge_structure_rank(f):
        # Simplified Hodge structure rank calculation
        # This is a placeholder and should be replaced with actual computation
        return len(set(f))
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_boolean_function(n)
        min_rank_H = hodge_structure_rank(f)
        rank_var = communication_complexity_rank_variance(f)
        results.append((min_rank_H, rank_var))
    
    if len(results) < 100:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    hodge_ranks = [r[0] for r in results]
    rank_vars = [r[1] for r in results]
    
    mean_hodge_rank = sum(hodge_ranks) / len(hodge_ranks)
    mean_rank_var = sum(rank_vars) / len(rank_vars)
    
    covariance = sum((h - mean_hodge_rank) * (v - mean_rank_var) for h, v in zip(hodge_ranks, rank_vars)) / len(results)
    variance_hodge = sum((h - mean_hodge_rank) ** 2 for h in hodge_ranks) / len(results)
    variance_rank_var = sum((v - mean_rank_var) ** 2 for v in rank_vars) / len(results)
    
    pearson_corr_coeff = covariance / math.sqrt(variance_hodge * variance_rank_var)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr_coeff,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(pearson_corr_coeff) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")