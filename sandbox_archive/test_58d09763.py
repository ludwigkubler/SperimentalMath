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
    
    def compute_quantum_state(phi):
        n = len(phi)
        state = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if phi[i ^ j] == 1:
                    state[i][j] = 1 / math.sqrt(2**n)
        return state
    
    def min_rank(state):
        n = len(state)
        rank = 0
        for i in range(n):
            row = [state[j][i] for j in range(n)]
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity(phi):
        n = len(phi)
        complexity = 0
        for i in range(2**n):
            for j in range(2**n):
                if phi[i ^ j] == 1:
                    complexity += 1
        return complexity
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    complexities = []
    
    for n in n_values:
        phi = generate_boolean_function(n)
        state = compute_quantum_state(phi)
        min_rank_val = min_rank(state)
        complexity_val = communication_complexity(phi)
        min_ranks.append(min_rank_val)
        complexities.append(complexity_val)
    
    if len(min_ranks) < 30:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": len(min_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation_coefficient = sum((min_ranks[i] - mean(min_ranks)) * (complexities[i] - mean(complexities)) for i in range(len(min_ranks))) / (len(min_ranks) * std_dev(min_ranks) * std_dev(complexities))
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(min_ranks) - 2)))
    
    return {
        "metric_name": "min_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8 and p_value < 0.01,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")