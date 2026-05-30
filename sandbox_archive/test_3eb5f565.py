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
    
    def generate_k_cnf(n, k):
        clauses = set()
        for _ in range(k):
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            while len(set(literals)) < n:
                literals[random.randint(0, n - 1)] *= -1
            clauses.add(tuple(sorted(literals)))
        return clauses
    
    def coxeter_group_action(clauses):
        action = {}
        for clause in clauses:
            key = tuple(sorted(abs(lit) for lit in clause))
            if key not in action:
                action[key] = len(action) + 1
        return action, max(action.values())
    
    def resolution_width(clauses):
        width = 0
        stack = list(clauses)
        while stack:
            clause = stack.pop()
            new_clauses = []
            for other_clause in clauses:
                if not set(clause).isdisjoint(other_clause):
                    new_clause = tuple(sorted(set(clause) ^ set(other_clause)))
                    if new_clause and len(new_clause) > 1:
                        new_clauses.append(new_clause)
            stack.extend(new_clauses)
            width = max(width, len(stack))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, n * (n - 1) // 2)
        clauses = generate_k_cnf(n, k)
        action, max_order = coxeter_group_action(clauses)
        width = resolution_width(clauses)
        results.append({
            "n": n,
            "k": k,
            "max_order": max_order,
            "width": width
        })
    
    if len(results) < 30:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation = 0
    n_sum = sum(result["n"] for result in results)
    width_sum = sum(result["width"] for result in results)
    max_order_sum = sum(result["max_order"] for result in results)
    n_width_product_sum = sum(result["n"] * result["width"] for result in results)
    n_max_order_product_sum = sum(result["n"] * result["max_order"] for result in results)
    
    n_mean = n_sum / len(results)
    width_mean = width_sum / len(results)
    max_order_mean = max_order_sum / len(results)
    
    numerator = n_width_product_sum - n_mean * width_sum
    denominator = math.sqrt((n_sum - n_mean**2) * (width_sum - width_mean**2))
    
    if denominator == 0:
        correlation = None
    else:
        correlation = numerator / denominator
    
    return {
        "metric_name": "resolution_width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation is not None and correlation >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8 and all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(result["counterexample"] for result in results):
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")