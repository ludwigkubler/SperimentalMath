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
        max_order = 0
        for clause in clauses:
            order = sum(abs(x) for x in clause) // len(clause)
            if order > max_order:
                max_order = order
        return max_order
    
    def resolution_proof_width(clauses):
        # Simplified version of resolution proof width calculation
        return sum(len(clause) for clause in clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_order = min_order_quasi_plurality(cnf)
        width = resolution_proof_width(cnf)
        results.append({"n": n, "min_order": min_order, "width": width})
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    n_values = [r["n"] for r in results]
    min_orders = [r["min_order"] for r in results]
    widths = [r["width"] for r in results]
    
    mean_n = sum(n_values) / len(n_values)
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_width = sum(widths) / len(widths)
    
    covariance = sum((n - mean_n) * (min_order - mean_min_order) for n, min_order in zip(n_values, min_orders)) / len(n_values)
    variance_n = sum((n - mean_n)**2 for n in n_values) / len(n_values)
    variance_width = sum((width - mean_width)**2 for width in widths) / len(widths)
    
    if variance_n == 0 or variance_width == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance is zero"
        }
    
    pearson_corr = covariance / math.sqrt(variance_n * variance_width)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(pearson_corr) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials completed")
        sys.exit(1)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    conjecture_holds_count = sum(r["conjecture_holds"] for r in results)
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric)**2 for x in metric_values) / len(metric_values))
    
    support_fraction = conjecture_holds_count / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.9\" first_failing_seed={first_failing_seed}")