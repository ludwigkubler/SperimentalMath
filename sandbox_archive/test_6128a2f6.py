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
    
    def generate_instance(n_vars, n_clauses):
        variables = [f"x{i}" for i in range(n_vars)]
        clauses = []
        for _ in range(n_clauses):
            clause = random.sample(variables + [f"~{v}" for v in variables], 2)
            clauses.append(clause)
        return variables, clauses
    
    def resolution_width(clauses):
        n_vars = len(set(v[0] if v[0][0] != '~' else v[1] for v in clauses))
        width = [n_vars]
        while True:
            new_clauses = []
            for i in range(len(width)):
                for j in range(i + 1, len(width)):
                    common_var = set(clauses[i]).intersection(set(clauses[j]))
                    if common_var:
                        new_clause = [v for v in clauses[i] if v not in common_var] + \
                                      [v for v in clauses[j] if v not in common_var]
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            width.extend(sorted(set(len(c) for c in new_clauses)))
        return max(width)
    
    def minimal_braided_monoid_order(variables, clauses):
        n_vars = len(variables)
        n_clauses = len(clauses)
        order = n_vars + n_clauses
        return order
    
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            variables, clauses = generate_instance(n, n)
            instances_tested += 1
            w_phi = resolution_width(clauses)
            n_braided_monoid = minimal_braided_monoid_order(variables, clauses)
            metric_values.append((n_braided_monoid, w_phi))
    
    if not metric_values:
        return {
            "metric_name": "resolution_width",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": max([n for n, _ in metric_values]),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_braided_monoids = [v[0] for v in metric_values]
    w_phi_values = [v[1] for v in metric_values]
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = ((n * sum_xy - sum_x * sum_y) ** 2) / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared
    
    _, _, r_squared = linear_regression(n_braided_monoids, w_phi_values)
    
    if r_squared < 0.7:
        conjecture_holds = False
        counterexample = f"r_squared={r_squared:.4f} < 0.7"
    
    return {
        "metric_name": "resolution_width",
        "metric_value": r_squared,
        "instances_tested": instances_tested,
        "n_max": max([n for n, _ in metric_values]),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_squared = sum(r["metric_value"] for r in results) / len(results)
    std_r_squared = math.sqrt(sum((r["metric_value"] - mean_r_squared) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_squared:.4f} std={std_r_squared:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.7 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.7)
        print(f"RESULT: FALSIFIED counterexample=\"r_squared<{0.7:.2f}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")