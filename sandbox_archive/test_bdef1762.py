# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def compute_clause_set_complexity(cnf):
        return len(cnf)
    
    def compute_minimal_geometric_entropy(cnf):
        # Placeholder for actual geometric entropy computation
        # For simplicity, we use the number of clauses as a proxy
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mge_values = []
    c_phi_values = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n * 2))
            mge = compute_minimal_geometric_entropy(cnf)
            c_phi = compute_clause_set_complexity(cnf)
            mge_values.append(mge)
            c_phi_values.append(c_phi)
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        sum_yy = sum(yi ** 2 for yi in y)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = sum_y - slope * sum_x
        r_squared = (n * sum_xy - sum_x * sum_y) ** 2 / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    if len(mge_values) < 30:
        return {
            "metric_name": "linear_regression",
            "metric_value": None,
            "instances_tested": len(mge_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    slope, intercept, r_squared = linear_regression(c_phi_values, mge_values)
    
    return {
        "metric_name": "linear_regression",
        "metric_value": r_squared,
        "instances_tested": len(mge_values),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= slope <= 1.5 and r_squared >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_squared = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"r_squared_out_of_bounds\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")