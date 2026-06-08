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
    
    def generate_boolean_satisfiability_instance(n_vars, n_clauses):
        variables = [f'x{i}' for i in range(n_vars)]
        clauses = []
        for _ in range(n_clauses):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(clause)
        return variables, clauses

    def resolution_proof_width(phi):
        # Placeholder implementation of resolution proof width
        # This is a dummy function and should be replaced with actual computation
        return len(phi) * 2

    def minimal_order_braided_monoid(V, C):
        # Placeholder implementation of minimal order of braided monoid
        # This is a dummy function and should be replaced with actual computation
        return len(V) + len(C)

    n_vars = random.randint(5, 10)
    n_clauses = random.randint(n_vars, n_vars * 2)
    V, C = generate_boolean_satisfiability_instance(n_vars, n_clauses)
    
    n_braided_monoids = minimal_order_braided_monoid(V, C)
    w_phi_values = [resolution_proof_width(phi) for phi in [V + C]]
    
    if len(w_phi_values) == 0:
        return {
            "metric_name": "resolution_proof_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_vars,
            "conjecture_holds": False,
            "counterexample": "empty_instance"
        }
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        sum_yy = sum(yi ** 2 for yi in y)
        
        if n == 0:
            return None, None, None
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        r_squared = ((n * sum_xy - sum_x * sum_y) ** 2) / ((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, r_squared

    slope, intercept, r_squared = linear_regression([n_braided_monoids], w_phi_values)
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": r_squared,
        "instances_tested": len(w_phi_values),
        "n_max": n_vars,
        "conjecture_holds": r_squared >= 0.7 and r_squared <= 0.9,
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
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"r_squared_below_threshold\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)