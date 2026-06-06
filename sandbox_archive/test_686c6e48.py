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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(lit == 0 for lit in clause):  # Ensure at least one literal is non-zero
            clause[random.randint(0, n - 1)] *= -1
        cnf.append(clause)
    return cnf

def frege_depth(cnf):
    depth = 0
    stack = [cnf]
    while stack:
        formula = stack.pop()
        if isinstance(formula[0], list):  # AND gate
            for subformula in formula:
                stack.append(subformula)
        else:  # OR gate
            depth += 1
    return depth

def monomial_representation(cnf):
    n = len(cnf[0])
    monomials = [Fraction(1, 2) ** (abs(lit) - 1) * lit for lit in range(-n, n + 1)]
    representation = 0
    for clause in cnf:
        term = 1
        for lit in clause:
            if abs(lit) > n:
                continue
            term *= monomials[abs(lit) - 1] * lit
        representation += term
    return abs(representation)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    trials = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in trials:
        cnf = generate_cnf(n, n * (n + 1) // 2)
        depth = frege_depth(cnf)
        
        if depth == 0:  # Skip trivial cases
            continue
        
        rep = monomial_representation(cnf)
        results.append((rep, math.log(depth + 1, 2)))
    
    if not results:
        return {
            "metric_name": "Monomial Representation Size vs. Log Depth",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    metric_values = [rep for rep, _ in results]
    log_depths = [depth for _, depth in results]
    
    mean_rep = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean_rep) ** 2 for x in metric_values) / len(metric_values))
    
    correlation_coefficient = (sum((metric_values[i] - mean_rep) * (log_depths[i] - mean(log_depths)) for i in range(len(results))) /
                               (len(results) * std_dev * math.sqrt(sum((x - mean(log_depths)) ** 2 for x in log_depths))))
    
    return {
        "metric_name": "Monomial Representation Size vs. Log Depth",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metric_values),
        "n_max": max(trials),
        "conjecture_holds": correlation_coefficient > 0.5 and all(x > 1 for x in metric_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'n_max': {result['n_max']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_metric = math.sqrt(sum((r['metric_value'] - mean_metric) ** 2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] > 0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(r['metric_value'] <= 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result['metric_value'] <= 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient did not meet threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=No valid instances found")