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
    
    def generate_instance(n):
        return [random.choice([0, 1]) for _ in range(2**n - 1)]
    
    def tseitin_formula(instance):
        n = len(instance) + 1
        clauses = []
        for i in range(n):
            if instance[i]:
                clauses.append([i+1])
            else:
                clauses.append([-i-1])
        return clauses
    
    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment.append(literal)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(new_clauses, new_assignment):
                return True
            new_assignment.pop()
            new_clauses = [c for c in clauses if -literal not in c]
            if dpll(new_clauses, new_assignment):
                return True
        else:
            literal = next((i+1 for i in range(len(assignment)) if assignment[i] == 0), None)
            new_assignment.append(literal)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if dpll(new_clauses, new_assignment):
                return True
        return False
    
    def msl(clauses):
        n = len(clauses)
        max_symmetry_length = 0
        for i in range(n):
            symmetry_length = 1
            for j in range(i+1, n):
                if all(c[i] == c[j] for c in clauses):
                    symmetry_length += 1
            max_symmetry_length = max(max_symmetry_length, symmetry_length)
        return max_symmetry_length
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi**2 for xi in x)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
        intercept = (sum_y - slope * sum_x) / n
        return slope, intercept
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        msl_sum = 0
        l_sum = 0
        for _ in range(5):
            instance = generate_instance(n)
            clauses = tseitin_formula(instance)
            if not dpll(clauses):
                continue
            msl_value = msl(clauses)
            l_value = len(dpll(clauses, []))
            results.append((msl_value, l_value))
            instances_tested += 1
            msl_sum += msl_value
            l_sum += l_value
    
    if not results:
        return {
            "metric_name": "msl(l)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    msl_values, l_values = zip(*results)
    slope, intercept = linear_regression(msl_values, l_values)
    
    return {
        "metric_name": "msl(l)",
        "metric_value": slope,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": slope > 1.0 and all(msl_value >= 0.5 * l_value for msl_value, l_value in results),
        "counterexample": "" if slope > 1.0 else f"msl(l) = {slope}, which is not greater than 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_slope = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_slope} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"slope_not_greater_than_1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_results")