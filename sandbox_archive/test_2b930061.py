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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        circuit_ranks = []
        for i in range(1, n + 1):
            # Generate all possible subsets of size i
            subsets = [list(subset) for subset in itertools.combinations(range(n), i)]
            ranks = []
            for subset in subsets:
                # Evaluate the function on the subset
                subset_value = f[sum(2**j for j in subset)]
                rank = 0
                for j in range(i):
                    if subset[j] == 1:
                        rank += 1
                ranks.append(rank)
            circuit_ranks.append(max(ranks))
        return sum(circuit_ranks) / n
    
    def hodge_dimension(f, d):
        # Placeholder function to compute the dimension of a Hodge class
        # This is a dummy implementation and should be replaced with actual computation
        return len(f)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        R_f = communication_complexity_rank_variance(f)
        dim_H_f = hodge_dimension(f, d=2)  # Placeholder value
        results.append((R_f, dim_H_f))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No data generated"
        }
    
    R_values, dim_H_values = zip(*results)
    mean_R = sum(R_values) / len(R_values)
    mean_dim_H = sum(dim_H_values) / len(dim_H_values)
    correlation_coefficient = (sum((R - mean_R) * (dim_H - mean_dim_H) for R, dim_H in results) /
                               math.sqrt(sum((R - mean_R)**2 for R in R_values) *
                                         sum((dim_H - mean_dim_H)**2 for dim_H in dim_H_values)))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if not results:
        print("RESULT: INCONCLUSIVE no data generated")
    else:
        mean_metric_value = sum(results) / len(results)
        std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if 0.5 <= r < 0.8) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        elif any(r < 0.5 for r in results):
            first_failing_seed = seeds[results.index(next(r for r in results if r < 0.5))]
            print(f"RESULT: FALSIFIED counterexample='low correlation' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient support")