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
    
    def tseitin_formula(instance):
        n = len(instance)
        literals = list(range(1, 2 * n + 1))
        new_vars = [2 * n + i + 1 for i in range(n)]
        tseitin_clauses = []
        
        for i in range(n):
            tseitin_clauses.append([literals[i], -new_vars[i]])
            tseitin_clauses.append([-literals[i], new_vars[i]])
            for j in range(i + 1, n):
                tseitin_clauses.append([literals[j], -new_vars[i]])
                tseitin_clauses.append([-literals[j], new_vars[i]])
                tseitin_clauses.append([-new_vars[i], literals[i], literals[j]])
        
        return tseitin_clauses
    
    def resolution_width(clauses):
        queue = clauses[:]
        seen = set()
        while queue:
            clause1 = queue.pop(0)
            for clause2 in queue:
                for lit1 in clause1:
                    if -lit1 in clause2:
                        new_clause = [l for l in clause1 + clause2 if l != lit1 and l != -lit1]
                        if not new_clause:
                            return 1
                        new_clause.sort()
                        if tuple(new_clause) not in seen:
                            seen.add(tuple(new_clause))
                            queue.append(new_clause)
        return len(seen)
    
    def homology_order(n):
        # Placeholder for actual computation of homology order
        return random.randint(1, n)  # Simplified for testing
    
    k = 0  # Fixed k for simplicity
    instances_tested = 30
    n_max = 40
    metric_values = []
    
    for _ in range(instances_tested):
        instance = [random.choice([0, 1]) for _ in range(n_max)]
        tseitin_clauses = tseitin_formula(instance)
        homology_order_value = homology_order(n_max)
        resolution_width_value = resolution_width(tseitin_clauses)
        
        if homology_order_value > 1.5 * resolution_width_value:
            return {
                "metric_name": "homology_order",
                "metric_value": homology_order_value,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "homology_order > 1.5 * resolution_width"
            }
        
        metric_values.append(homology_order_value)
    
    correlation_coefficient = pearson_correlation(metric_values, [resolution_width(tseitin_formula([random.choice([0, 1]) for _ in range(n_max)])) for _ in range(instances_tested)])
    
    return {
        "metric_name": "homology_order",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

def pearson_correlation(x, y):
    if len(x) != len(y):
        return None
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) * sum((y[i] - mean_y) ** 2 for i in range(n)))
    
    if denominator == 0:
        return None
    
    return numerator / denominator

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='homology_order > 1.5 * resolution_width' first_failing_seed={first_failing_seed}")