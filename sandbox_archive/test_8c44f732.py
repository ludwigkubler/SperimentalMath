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

def generate_clause_set(n, k):
    clauses = []
    for _ in range(k):
        clause = set(random.sample(range(1, n+1), 2))
        if random.choice([True, False]):
            clause = {x: -1 for x in clause}
        clauses.append(clause)
    return clauses

def resolution_width(clauses):
    queue = [set(clause) for clause in clauses]
    while queue:
        new_queue = []
        while queue:
            clause1 = queue.pop()
            if len(clause1) == 1:
                literal = list(clause1)[0]
                for clause2 in queue:
                    if -literal in clause2:
                        new_clause = clause2 ^ {literal}
                        if new_clause:
                            new_queue.append(new_clause)
        queue = new_queue
    return len(queue)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 24 instances per seed
            clauses = generate_clause_set(n, random.randint(1, n))
            order = len(clauses)  # Simplified as a placeholder
            width = resolution_width(clauses)
            results.append((order, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders = [r[0] for r in results]
    widths = [r[1] for r in results]
    
    mean_order = sum(orders) / len(orders)
    mean_width = sum(widths) / len(widths)
    
    correlation_coefficient = 0
    if len(orders) > 1:
        numerator = sum((x - mean_order) * (y - mean_width) for x, y in zip(orders, widths))
        denominator = math.sqrt(sum((x - mean_order)**2 for x in orders)) * math.sqrt(sum((y - mean_width)**2 for y in widths))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient <= 1,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_out_of_range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unmet_acceptance_criteria")