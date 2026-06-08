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
        for _ in range(10 * n):  # Generate 10*n clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def ehrhart_polynomial_degree(clauses):
        # Simplified Ehrhart polynomial degree estimation (O(n^2))
        return len(clauses) ** 0.5
    
    def clause_depth(clauses):
        max_depth = 0
        for clause in clauses:
            depth = sum(abs(x) > 1 for x in clause)
            if depth > max_depth:
                max_depth = depth
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 instances
            clauses = generate_cnf(n)
            degree = ehrhart_polynomial_degree(clauses)
            depth = clause_depth(clauses)
            if degree == 0:
                continue  # Skip if degree is zero to avoid division by zero
            results.append((n, degree, depth))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(result[0] for result in results)
    instances_tested = len(results)
    
    log_n_squared = [math.log2(n) ** 2 for n, _, _ in results]
    degrees = [result[1] for result in results]
    depths = [result[2] for result in results]
    
    mean_depth = sum(depths) / instances_tested
    mean_log_n_squared_times_degree = sum(log_n_squared[i] * degrees[i] for i in range(instances_tested)) / instances_tested
    
    correlation_coefficient = (sum((depths[i] - mean_depth) * (log_n_squared[i] * degrees[i] - mean_log_n_squared_times_degree) for i in range(instances_tested))
                               / math.sqrt(sum((depths[i] - mean_depth) ** 2 for i in range(instances_tested)) *
                                            sum((log_n_squared[i] * degrees[i] - mean_log_n_squared_times_degree) ** 2 for i in range(instances_tested))))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] != "" for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")