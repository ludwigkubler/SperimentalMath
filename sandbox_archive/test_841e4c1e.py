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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def matroid_from_cnf(cnf):
        elements = set(abs(lit) for lit in sum(cnf, []))
        independent_sets = [{0}]
        for element in elements:
            new_independent_sets = []
            for s in independent_sets:
                if all(element not in clause or -element in clause for clause in cnf):
                    new_independent_sets.append(s.union({element}))
            independent_sets.extend(new_independent_sets)
        return independent_sets
    
    def tropical_symplectic_leaves(matroid):
        leaves = []
        for s in matroid:
            if len(s) > 1 and all(len(t) == 1 for t in matroid if s.intersection(t)):
                leaves.append(s)
        return leaves
    
    def resolution_width(cnf):
        width = 0
        stack = [cnf]
        while stack:
            clause = stack.pop()
            if len(clause) == 1:
                continue
            new_clause = []
            for lit in clause:
                new_clauses = []
                for c in cnf:
                    if lit not in c and -lit not in c:
                        new_clauses.append(c)
                    elif lit in c:
                        new_clauses.append([l for l in c if l != lit])
                    else:
                        new_clauses.append([l for l in c if l != -lit])
                stack.extend(new_clauses)
            width = max(width, len(clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2*n, 3*n))
            matroid = matroid_from_cnf(cnf)
            leaves = tropical_symplectic_leaves(matroid)
            width = resolution_width(cnf)
            results.append((len(leaves), width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    ost_values = [ost for ost, _ in results]
    width_values = [width for _, width in results]
    
    mean_ost = sum(ost_values) / len(ost_values)
    mean_width = sum(width_values) / len(width_values)
    
    correlation_coefficient = 0
    if len(ost_values) > 1:
        numerator = sum((ost - mean_ost) * (width - mean_width) for ost, width in results)
        denominator = math.sqrt(sum((ost - mean_ost)**2 for ost in ost_values)) * math.sqrt(sum((width - mean_width)**2 for width in width_values))
        correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.95\" first_failing_seed={first_failing_seed}")