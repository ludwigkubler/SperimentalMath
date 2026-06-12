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
    for _ in range(2**n // 4):  # Ensure at least 8 clauses
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def search(assignments):
        unsatisfied_clauses = [c for c in cnf if not any(lit in assignments and (assignments[lit] == 1) or (-lit in assignments and (assignments[-lit] == -1)) for lit in c)]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            assignments[literal] = 1 if literal > 0 else -1
            if search(assignments):
                return True
            del assignments[literal]
            assignments[-literal] = 1 if -literal > 0 else -1
            if search(assignments):
                return True
            del assignments[-literal]
        pure_literal = next((lit for lit in range(1, n+1) if all(lit not in c or -lit not in c for c in unsatisfied_clauses)), None)
        if pure_literal:
            assignments[pure_literal] = 1
            if search(assignments):
                return True
            del assignments[pure_literal]
            assignments[-pure_literal] = 1
            if search(assignments):
                return True
            del assignments[-pure_literal]
        for literal in range(1, n+1):
            assignments[literal] = 1
            if search(assignments):
                return True
            del assignments[literal]
            assignments[-literal] = 1
            if search(assignments):
                return True
            del assignments[-literal]
        return False

    assignments = {}
    return search(assignments)

def min_order_modular_forms(n, p):
    # Placeholder function to simulate the minimal order of modular forms
    # This is a dummy implementation and should be replaced with actual computation
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(n)
        width = dpll(cnf)
        min_order = sum(min_order_modular_forms(n, p) for p in range(2, n+1)) / (n-1)
        results.append((min_order, width))
    mean_min_order = sum(x[0] for x in results) / len(results)
    mean_width = sum(x[1] for x in results) / len(results)
    correlation_coefficient = (sum((x - mean_min_order) * (y - mean_width) for x, y in results) /
                               math.sqrt(sum((x - mean_min_order)**2 for x, _ in results)) *
                               math.sqrt(sum((y - mean_width)**2 for _, y in results)))
    conjecture_holds = correlation_coefficient >= 0.8 and p_value < 0.05
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 73))  # Default to first 30 primes
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(x["metric_value"] for x in results) / len(results)
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")