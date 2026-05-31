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
    
    def generate_formula(n):
        if n == 1:
            return 'A'
        else:
            subformulas = [generate_formula(n-1) for _ in range(2)]
            return f'({subformulas[0]} & {subformulas[1]})'

    def dpll_search_tree(formula, assignment):
        if formula == 'A':
            return 1
        elif formula.startswith('('):
            left, right = formula[1:-1].split(' & ')
            return dpll_search_tree(left, assignment) + dpll_search_tree(right, assignment)
        else:
            var = formula
            if var in assignment:
                return 0
            else:
                true_assignment = assignment.copy()
                true_assignment[var] = True
                false_assignment = assignment.copy()
                false_assignment[var] = False
                return dpll_search_tree(formula, true_assignment) + dpll_search_tree(formula, false_assignment)

    def morse_function(n):
        formula = generate_formula(n)
        assignment = {}
        return dpll_search_tree(formula, assignment)

    n_values = [5, 10, 15, 20, 30, 40]
    critical_points = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cp = morse_function(n)
            if cp is not None:
                critical_points.append(cp)
    
    if len(critical_points) == 0:
        return {
            "metric_name": "Critical Points",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No critical points found"
        }
    
    mean_cp = sum(critical_points) / len(critical_points)
    n_cubed_root = [n ** (2/3) for n in n_values]
    correlation_sum = sum((cp - mean_cp) * (n_val ** (2/3) - mean(n_cubed_root)) for cp, n_val in zip(critical_points, n_values))
    variance_n_cubed_root = sum((n_val ** (2/3) - mean(n_cubed_root)) ** 2 for n_val in n_values)
    
    if variance_n_cubed_root == 0:
        return {
            "metric_name": "Critical Points",
            "metric_value": mean_cp,
            "instances_tested": len(critical_points),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance of n^(2/3) is zero"
        }
    
    correlation_coefficient = correlation_sum / (len(critical_points) * math.sqrt(variance_n_cubed_root))
    
    return {
        "metric_name": "Critical Points",
        "metric_value": mean_cp,
        "instances_tested": len(critical_points),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")