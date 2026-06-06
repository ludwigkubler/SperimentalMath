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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def generate_random_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = random.sample(range(1, n+1), 3)
        sign = [random.choice([-1, 1]) for _ in range(3)]
        cnf.append([sign[i] * clause[i] for i in range(3)])
    return cnf

def incidence_polytope(cnf):
    n = len(cnf[0])
    polytope = []
    for assignment in product([-1, 1], repeat=n):
        if all(any(sign * var == assignment[var-1] for sign, var in clause) for clause in cnf):
            polytope.append(assignment)
    return polytope

def minimal_ehrhart_quotient(polytope):
    n = len(polytope[0])
    volume = 1
    for i in range(n):
        min_val = min(p[i] for p in polytope)
        max_val = max(p[i] for p in polytope)
        volume *= (max_val - min_val + 1) / (2**(n-i))
    return volume

def circuit_monotone_width(cnf):
    n = len(cnf[0])
    width = 0
    for i in range(n):
        stack = []
        for clause in cnf:
            if any(var == i+1 or var == -(i+1) for sign, var in clause):
                stack.append(clause)
            else:
                while stack and not any(sign * var == i+1 or sign * var == -(i+1) for sign, var in stack[-1]):
                    stack.pop()
        width = max(width, len(stack))
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_random_cnf(n, 10 * n)
        polytope = incidence_polytope(cnf)
        mu = minimal_ehrhart_quotient(polytope)
        w_m = circuit_monotone_width(cnf)
        results.append((mu, w_m))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mu_values, w_m_values = zip(*results)
    correlation_coefficient = sum((mu - mean_mu) * (w_m - mean_w_m) for mu, w_m in results) / len(results)
    mean_mu = sum(mu_values) / len(mu_values)
    mean_w_m = sum(w_m_values) / len(w_m_values)
    
    conjecture_holds = all(mu**2 <= w_m for mu, w_m in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")