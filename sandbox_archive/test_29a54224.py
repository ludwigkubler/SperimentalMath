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
    
    def generate_3cnf(n, m):
        literals = [f'x{i}' for i in range(1, n+1)] + [f'~x{i}' for i in range(1, n+1)]
        clauses = set()
        while len(clauses) < m:
            clause = random.sample(literals, 3)
            if all(l not in clause and '~' + l not in clause for l in literals):
                clauses.add(tuple(sorted(clause)))
        return clauses
    
    def matroidal_cover(clauses):
        elements = set()
        for clause in clauses:
            elements.update(clause)
        cover = []
        for element in elements:
            cover.append([clause for clause in clauses if element in clause])
        return cover
    
    def euler_characteristic(cover):
        rank = len(cover)
        nullity = sum(len(c) - 1 for c in cover) // 2
        return rank - nullity
    
    def dpll_refutation_tree_width(clauses):
        n = max(int(l[1:]) for l in clauses if l.startswith('x'))
        m = len(clauses)
        tree_width = 0
        # Simplified DPLL-like algorithm to estimate width
        for _ in range(10):  # Run multiple times to average
            assignment = {f'x{i}': random.choice([True, False]) for i in range(1, n+1)}
            unsatisfied_clauses = [c for c in clauses if any(l not in assignment or (l.startswith('~') and assignment[l[1:]] != True) for l in c)]
            width = 0
            while unsatisfied_clauses:
                unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
                if unit_clause:
                    literal, = unit_clause
                    assignment[literal] = literal.startswith('x')
                    unsatisfied_clauses.remove(unit_clause)
                    for clause in unsatisfied_clauses[:]:
                        if any(l not in assignment or (l.startswith('~') and assignment[l[1:]] != True) for l in clause):
                            continue
                        unsatisfied_clauses.remove(clause)
                else:
                    width += 1
            tree_width = max(tree_width, width)
        return tree_width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 4 * n)
        clauses = generate_3cnf(n, m)
        cover = matroidal_cover(clauses)
        chi = euler_characteristic(cover)
        w = dpll_refutation_tree_width(clauses)
        results.append((chi, w))
    
    if len(results) < 30:
        return {
            "metric_name": "Euler Characteristic vs DPLL Refutation Tree Width",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    chi_values = [chi for chi, _ in results]
    w_squared_values = [w**2 for _, w in results]
    
    mean_chi = sum(chi_values) / len(chi_values)
    std_chi = math.sqrt(sum((x - mean_chi)**2 for x in chi_values) / len(chi_values))
    correlation_coefficient = sum((chi_values[i] - mean_chi) * (w_squared_values[i] - mean(w_squared_values)) for i in range(len(results))) / (len(results) * std_chi * math.sqrt(sum((x - mean(w_squared_values))**2 for x in w_squared_values)))
    
    return {
        "metric_name": "Euler Characteristic vs DPLL Refutation Tree Width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    mean_metric_value = sum(results) / len(results)
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r) >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r) < 0.8 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r) < 0.8))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")