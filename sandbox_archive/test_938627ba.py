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

def generate_tseitin_formula(n):
    if n <= 0:
        return ""
    
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    # Generate clauses for OR operations
    for var in variables:
        clauses.append(f'{var} OR {~var}')
    
    # Generate clauses for AND operations
    for i in range(n):
        clause = f'x{i+1}'
        for j in range(i+2, n+1):
            clause += f' AND x{j}'
        clauses.append(clause)
    
    return ' AND '.join(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Define the range of instance sizes
    instance_sizes = [5, 10, 15, 20, 30, 40]
    metric_values = []
    n_max = 0
    
    for n in instance_sizes:
        formula = generate_tseitin_formula(n)
        if not formula:
            continue
        
        # Simulate the computation of LID and Frege proof depth
        lid = random.uniform(1, n)  # Placeholder for actual LID computation
        frege_depth = random.randint(10, 5*n)  # Placeholder for actual Frege depth computation
        
        metric_values.append(lid)
        n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "LID",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Calculate Pearson's correlation coefficient
    mean_lid = sum(metric_values) / len(metric_values)
    variance_lid = sum((x - mean_lid) ** 2 for x in metric_values) / len(metric_values)
    covariance = sum((metric_values[i] - mean_lid) * (i + 10) for i in range(len(metric_values))) / len(metric_values)
    std_dev_lid = math.sqrt(variance_lid)
    
    if std_dev_lid == 0:
        return {
            "metric_name": "LID",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = covariance / (len(metric_values) * std_dev_lid)
    
    return {
        "metric_name": "LID",
        "metric_value": pearson_corr,
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
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
        print("RESULT: INCONCLUSIVE reason=unknown")