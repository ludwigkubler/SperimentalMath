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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def solve(cnf):
    literals = set()
    while cnf:
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if not unit_clauses:
            break
        literal = random.choice(unit_clauses)
        literals.add(literal)
        cnf = [c for c in cnf if literal not in c and -literal not in c]
    return literals

def weierstrass_order(n):
    # Placeholder function. Replace with actual Weierstrass order computation.
    return n

def resolution_depth(cnf, max_depth=100):
    stack = []
    for clause in cnf:
        stack.append(clause)
    while len(stack) < max_depth:
        if not stack:
            break
        clause = random.choice(stack)
        new_clause = [x for x in clause if x not in literals]
        stack.extend(new_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        cnf = generate_cnf(n)
        literals = solve(cnf)
        omega_n = weierstrass_order(n)
        d_n = resolution_depth(cnf)
        results.append((omega_n, d_n))
    
    if len(results) < 100:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    omega_values, d_values = zip(*results)
    mean_omega = sum(omega_values) / len(omega_values)
    mean_d = sum(d_values) / len(d_values)
    correlation_coefficient = (sum((x - mean_omega) * (y - mean_d) for x, y in results) /
                               math.sqrt(sum((x - mean_omega) ** 2 for x in omega_values) *
                                         sum((y - mean_d) ** 2 for y in d_values)))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,  # Simplified threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(v is not None for v in results):
        mean_result = sum(results) / len(results)
        std_result = math.sqrt(sum((x - mean_result) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if abs(r) > 0.5) / len(results)  # Simplified threshold
        print(f"RESULT: SUPPORTED mean={mean_result} std={std_result} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, v in enumerate(results) if v is None)
        print(f"RESULT: FALSIFIED counterexample='insufficient_instances' first_failing_seed={first_failing_seed + 1}")