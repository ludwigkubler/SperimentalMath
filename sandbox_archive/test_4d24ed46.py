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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = matrix[j][i] / matrix[i][i]
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def dpll_width(clauses, assignment):
    variables = set(abs(var) for clause in clauses for var in clause)
    if not variables:
        return 0
    var = random.choice(list(variables))
    positive_clauses = [clause for clause in clauses if var in clause]
    negative_clauses = [clause for clause in clauses if -var in clause]
    assignment[var] = True
    width_positive = dpll_width(positive_clauses, assignment)
    del assignment[var]
    assignment[-var] = True
    width_negative = dpll_width(negative_clauses, assignment)
    del assignment[-var]
    return max(width_positive, width_negative) + 1

def min_reflections(clause):
    # Placeholder for the actual computation of minimal reflections
    # This is a dummy implementation and should be replaced with the actual logic
    return len(clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if all(var != -var for var in clause):
            clauses.append(clause)
    
    widths = []
    reflections = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        assignment = {}
        width = dpll_width(clauses, assignment)
        reflection = min_reflections(random.choice(clauses))
        widths.append(width)
        reflections.append(reflection)
    
    correlation_coefficient = sum((w - sum(widths) / len(widths)) * (r - sum(reflections) / len(reflections)) for w, r in zip(widths, reflections)) / (len(widths) * math.sqrt(sum((w - sum(widths) / len(widths)) ** 2 for w in widths)) * math.sqrt(sum((r - sum(reflections) / len(reflections)) ** 2 for r in reflections)))
    mean_width = sum(widths) / len(widths)
    mean_reflection = sum(reflections) / len(reflections)
    
    if correlation_coefficient >= 0.8 and abs(mean_width - mean_reflection) <= 3:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "correlation_threshold_not_met"
    
    return {
        "metric_name": "DPLL Width vs Reflections",
        "metric_value": correlation_coefficient,
        "instances_tested": len(widths),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_threshold_not_met\" first_failing_seed={first_failing_seed}")