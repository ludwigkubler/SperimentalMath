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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def min_order_quasi_plurality(clauses):
        max_clauses = len(max(clauses, key=len))
        order = [0] * (max_clauses + 1)
        for clause in clauses:
            order[len(clause)] += 1
        return sum(order) / len(clauses)
    
    def resolution_width(clauses):
        n = len(clauses[0])
        max_width = 0
        queue = list(clauses)
        while queue:
            new_queue = []
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    clause_i = set(abs(x) for x in queue[i])
                    clause_j = set(abs(x) for x in queue[j])
                    if not (clause_i & clause_j):
                        continue
                    new_clause = list(clause_i ^ clause_j)
                    if len(new_clause) == 1:
                        return max_width + 1
                    new_queue.append(new_clause)
            queue = new_queue
            max_width += 1
        return max_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_order = min_order_quasi_plurality(cnf)
        width = resolution_width(cnf)
        results.append({"n": n, "min_order": min_order, "width": width})
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    min_orders = [result["min_order"] for result in results]
    widths = [result["width"] for result in results]
    
    n = len(min_orders)
    mean_min_order = sum(min_orders) / n
    mean_width = sum(widths) / n
    
    covariance = sum((min_orders[i] - mean_min_order) * (widths[i] - mean_width) for i in range(n)) / n
    variance_min_order = sum((min_orders[i] - mean_min_order) ** 2 for i in range(n)) / n
    variance_width = sum((widths[i] - mean_width) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_min_order) * math.sqrt(variance_width))
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if abs(result["metric_value"]) >= 0.9) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=no_data")