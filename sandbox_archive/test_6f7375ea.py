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
    
    def generate_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def algebraic_cycle_representation(circuit):
        n = int(math.log2(len(circuit)))
        cycle_order = 0
        while True:
            cycle_order += 1
            if all(sum(circuit[i:i+n] == circuit[j:j+n] for i, j in combinations(range(2**n), n)) for _ in range(n)):
                break
        return cycle_order
    
    def rank_variance(circuit):
        n = int(math.log2(len(circuit)))
        variance = 0
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] == circuit[j]:
                    variance += 1
        return variance / (n * (n - 1))
    
    def combinations(iterable, r):
        pool = list(iterable)
        n = len(pool)
        indices = list(range(r))
        yield tuple(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield tuple(pool[i] for i in indices)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        circuit = generate_circuit(n)
        alpha_C = algebraic_cycle_representation(circuit)
        rank_var = rank_variance(circuit)
        results.append({"n": n, "alpha_C": alpha_C, "rank_var": rank_var})
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "Not enough instances tested"
        }
    
    alpha_values = [r["alpha_C"] for r in results]
    rank_var_values = [r["rank_var"] for r in results]
    
    mean_alpha = sum(alpha_values) / len(alpha_values)
    mean_rank_var = sum(rank_var_values) / len(rank_var_values)
    
    covariance = sum((alpha_values[i] - mean_alpha) * (rank_var_values[i] - mean_rank_var) for i in range(len(alpha_values))) / len(alpha_values)
    variance_alpha = sum((alpha_values[i] - mean_alpha)**2 for i in range(len(alpha_values))) / len(alpha_values)
    variance_rank_var = sum((rank_var_values[i] - mean_rank_var)**2 for i in range(len(rank_var_values))) / len(rank_var_values)
    
    pearson_corr = covariance / (math.sqrt(variance_alpha) * math.sqrt(variance_rank_var))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": 30,
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")