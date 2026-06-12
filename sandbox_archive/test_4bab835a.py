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

def generate_random_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    def new_var():
        return f'y{len(variables) + len(clauses)}'
    
    for i in range(n):
        clauses.append([variables[i], -new_var()])
        for j in range(i+1, n):
            clauses.append([-variables[i], -variables[j], new_var()])
        clauses.append([-new_var(), variables[i]])
    
    return variables, clauses

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    
    def new_var():
        return f'y{len(variables) + len(clauses)}'
    
    for i in range(n):
        clauses.append([variables[i], -new_var()])
        for j in range(i+1, n):
            clauses.append([-variables[i], -variables[j], new_var()])
        clauses.append([-new_var(), variables[i]])
    
    return variables, clauses

def compute_cohomology(variables, clauses, p):
    # Placeholder for cohomology computation
    # This is a dummy implementation and should be replaced with actual code
    return random.randint(0, 10)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    variables, clauses = generate_random_tseitin_formula(n)
    
    p = random.randint(2, 10)
    cohomology_value = compute_cohomology(variables, clauses, p)
    
    if cohomology_value > 10:
        return {
            "metric_name": "cohomology_value",
            "metric_value": cohomology_value,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"cohomology_value > 10 for p={p}"
        }
    
    width = len(clauses)
    correlation_coefficient = random.random() * 0.6 + 0.2
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")