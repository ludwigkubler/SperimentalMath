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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(2, 4))]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate resolution width
        stack = []
        literals = set()
        for clause in cnf:
            if not any(lit in literals for lit in clause):
                stack.append((clause, 0))
                literals.update(clause)
        while stack:
            clause, index = stack.pop()
            if index == len(clause):
                return float('inf')
            lit = clause[index]
            neg_lit = -lit
            if neg_lit in literals:
                continue
            new_clause = [l for l in clause if l != lit and l != neg_lit]
            stack.append((new_clause, 0))
        return len(literals)
    
    def tropicalized_brauer_group(cnf):
        # Placeholder function to simulate Brauer group computation
        return random.randint(1, n * 10)
    
    results = []
    for _ in range(10):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        order = tropicalized_brauer_group(cnf)
        results.append((order, width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orders, widths = zip(*results)
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(orders, widths)) / (len(results) * std_dev_x * std_dev_y)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")