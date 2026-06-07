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
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def hexp(instance):
        p = 2
        k = 0
        while True:
            found_solution = False
            for clause in instance:
                if all(abs(x) not in {abs(y) for y in clause} for x in range(-p, p+1)):
                    found_solution = True
                    break
            if found_solution:
                k += 1
                p *= 2
            else:
                return k
    
    def resolution_width(instance):
        clauses = instance[:]
        width = 0
        while clauses:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if abs(clauses[i][0]) == abs(clauses[j][0]):
                        new_clause = [c for c in clauses[i] if c != -clauses[j][0]] + [c for c in clauses[j] if c != -clauses[i][0]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return width
            clauses.append(new_clause)
            width = max(width, len(new_clause))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    hexp_values = []
    widths = []
    
    for n in n_values:
        instance = generate_sat_instance(n)
        hexp_val = hexp(instance)
        width = resolution_width(instance)
        hexp_values.append(hexp_val)
        widths.append(width)
    
    correlation_coefficient = sum((hexp_val - mean_hexp) * (width - mean_width) for hexp_val, width in zip(hexp_values, widths)) / len(hexp_values)
    mean_hexp = sum(hexp_values) / len(hexp_values)
    mean_width = sum(widths) / len(widths)
    mean_abs_diff = sum(abs(hexp_val - width) for hexp_val, width in zip(hexp_values, widths)) / len(hexp_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 and mean_abs_diff <= 3 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = [run_trial(seed) for seed in seeds]
    
    correlation_coefficients = [r["metric_value"] for r in results if "metric_value" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    mean_corr_coeff = sum(correlation_coefficients) / len(correlation_coefficients)
    std_dev_corr_coeff = math.sqrt(sum((x - mean_corr_coeff) ** 2 for x in correlation_coefficients) / len(correlation_coefficients))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_dev_corr_coeff} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")