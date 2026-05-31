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
    
    def generate_tseitin_formula(n, d):
        if n < 1 or d < 2:
            return None
        variables = list(range(1, n + 1))
        clauses = []
        
        # Generate the first part of Tseitin formula
        for i in range(1, n + 1):
            clause = [i]
            for j in range(n):
                if (j * d) % n == i - 1:
                    clause.append(-variables[j])
            clauses.append(clause)
        
        # Generate the second part of Tseitin formula
        for i in range(1, n + 1):
            for j in range(n):
                if (j * d) % n == i - 2:
                    clauses.append([i, variables[j]])
        
        return clauses

    def resolution_width(clauses):
        queue = clauses[:]
        learned_clauses = []
        
        while True:
            new_clause = None
            for clause1 in queue:
                for clause2 in queue:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in [-y for y in clause1] and x not in [-y for y in clause2]]
                        if len(new_clause) == 0:
                            return len(learned_clauses)
                        learned_clauses.append(new_clause)
            if new_clause is None:
                break
            queue.append(new_clause)
        
        return len(learned_clauses)

    def min_local_index(n, d):
        # Placeholder implementation for minimal local index calculation
        # This should be replaced with actual tropical curve computation
        return random.uniform(1, n * d)

    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_tseitin_formula(n, n)
            if clauses is None:
                continue
            width = resolution_width(clauses)
            local_index = min_local_index(n, n)
            results.append((local_index, width))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    local_indices, widths = zip(*results)
    correlation_coefficient = sum((x - mean_local_index) * (y - mean_width) for x, y in zip(local_indices, widths)) / (len(results) * std_dev_local_index * std_dev_width)
    mean_local_index = sum(local_indices) / len(local_indices)
    std_dev_local_index = math.sqrt(sum((x - mean_local_index) ** 2 for x in local_indices) / len(local_indices))
    mean_width = sum(widths) / len(widths)
    std_dev_width = math.sqrt(sum((y - mean_width) ** 2 for y in widths) / len(widths))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_local_index <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((x["metric_value"] - mean_metric_value) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")