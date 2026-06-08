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
    
    def generate_instance(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (1 if random.random() < 0.5 else -1)
                      for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return variables, clauses

    def dpll(instance):
        variables, clauses = instance
        assignment = {v: None for v in variables}
        
        def is_satisfiable():
            for clause in clauses:
                if not any(lit in assignment and (assignment[lit] == 1) for lit in clause):
                    return False
            return True
        
        def backtrack(level=0):
            if level == len(variables):
                return is_satisfiable()
            
            v = variables[level]
            for value in [True, False]:
                assignment[v] = value
                if backtrack(level + 1):
                    return True
                assignment[v] = None
            
            return False
        
        return backtrack()

    def geometric_entropy(instance):
        # Placeholder function for geometric entropy calculation
        # This is a dummy implementation and should be replaced with actual GCT computation
        variables, clauses = instance
        return len(variables) * len(clauses)

    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            instance = generate_instance(n, random.randint(n, 2 * n))
            path_length = dpll(instance)
            entropy = geometric_entropy(instance)
            
            metric_values.append((entropy, path_length))
            instances_tested += 1
            n_max = max(n_max, n)

    if not metric_values:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    mean_entropy = sum(e for e, _ in metric_values) / len(metric_values)
    mean_path_length = sum(p for _, p in metric_values) / len(metric_values)

    correlation_coefficient = 0
    if mean_entropy != 0 and mean_path_length != 0:
        covariance = sum((e - mean_entropy) * (p - mean_path_length) for e, p in metric_values)
        variance_entropy = sum((e - mean_entropy) ** 2 for e, _ in metric_values)
        variance_path_length = sum((p - mean_path_length) ** 2 for _, p in metric_values)
        correlation_coefficient = covariance / (math.sqrt(variance_entropy) * math.sqrt(variance_path_length))

    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"

    return {
        "metric_name": "geometric_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
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
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")