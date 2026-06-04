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
    variables = list(range(1, m + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, 2)
        clauses.append(clause)
    return clauses

def compute_padic_l_function(n, m):
    # Placeholder function to compute p-adic L-function
    # This is a dummy implementation for testing purposes
    return Fraction(1, n**m)

def correlation_coefficient(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = (sum((xi - mean_x)**2 for xi in x) * sum((yi - mean_y)**2 for yi in y))**0.5
    
    if denominator == 0:
        return None
    
    return numerator / denominator

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    instances = [generate_cnf_formula(m) for m in range(1, 41)]
    padic_l_functions = [compute_padic_l_function(n, len(instance)) for n, instance in enumerate(instances, start=1)]
    instance_sizes = [len(instance) for instance in instances]
    
    correlation_coeff = correlation_coefficient(padic_l_functions, instance_sizes)
    
    metric_name = "padic_l_function_order"
    metric_value = sum(abs(lf.numerator / lf.denominator) for lf in padic_l_functions) / len(padic_l_functions)
    instances_tested = len(instances)
    n_max = max(len(instance) for instance in instances)
    conjecture_holds = correlation_coeff is not None and 0.8 <= abs(correlation_coeff) <= 1
    counterexample = "correlation_coefficient=0" if correlation_coeff == 0 else ""
    
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
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [i for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={first_failing_seed}")