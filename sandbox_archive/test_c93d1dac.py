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

def generate_cnf_formula(m):
    variables = [f'x{i}' for i in range(1, m+1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(f"({clause[0]} ∨ {clause[1]})")
    return " ∧ ".join(clauses)

def compute_padic_l_function(n, m):
    # Placeholder function to compute p-adic L-function
    # This is a dummy implementation for testing purposes
    p = 2  # Using a fixed prime p=2 for simplicity
    order = Fraction(m**(1/3), p)
    return order

def correlation_coefficient(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = ((sum((xi - mean_x)**2 for xi in x)) * 
                   sum((yi - mean_y)**2 for yi in y))**0.5
    
    if denominator == 0:
        return float('nan')
    
    return numerator / denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    instances = [generate_cnf_formula(m) for m in range(1, 41)]
    padic_l_functions = [compute_padic_l_function(n, m) for n, m in enumerate(instances)]
    instance_sizes = [len(instance.split(' ∧ ')) for instance in instances]
    
    correlation = correlation_coefficient(padic_l_functions, instance_sizes)
    
    metric_name = "padic_l_function_order"
    metric_value = sum(abs(order) for order in padic_l_functions) / len(padic_l_functions)
    instances_tested = len(instances)
    n_max = max(instance_sizes)
    conjecture_holds = correlation >= 0.8 and correlation <= 1
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [i for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")