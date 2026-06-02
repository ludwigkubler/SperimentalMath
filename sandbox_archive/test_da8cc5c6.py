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
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def permutation_action(cnf):
        action = {}
        for literal in set(abs(lit) for lit in sum(cnf, [])):
            action[literal] = {abs(lit): 1 if lit > 0 else -1}
        return action
    
    def min_order(permutation_action):
        orders = [max(action.values()) for action in permutation_action.values()]
        return max(orders) if orders else 1
    
    def communication_complexity_rank(cnf):
        rank = 0
        for clause in cnf:
            rank += len(set(abs(lit) for lit in clause))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        action = permutation_action(cnf)
        min_order_val = min_order(action)
        rank = communication_complexity_rank(cnf)
        results.append((min_order_val, rank))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_order_vals = [r[0] for r in results]
    ranks = [r[1] for r in results]
    
    mean_min_order = sum(min_order_vals) / len(min_order_vals)
    mean_rank = sum(ranks) / len(ranks)
    
    correlation_coefficient = 0
    if len(min_order_vals) > 1:
        numerator = sum((min_order_vals[i] - mean_min_order) * (ranks[i] - mean_rank) for i in range(len(min_order_vals)))
        denominator = math.sqrt(sum((min_order_vals[i] - mean_min_order) ** 2 for i in range(len(min_order_vals))) * sum((ranks[i] - mean_rank) ** 2 for i in range(len(ranks))))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")