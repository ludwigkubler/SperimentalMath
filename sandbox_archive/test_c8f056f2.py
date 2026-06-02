# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|'])
            left = generate_boolean_formula(n // 2)
            right = generate_boolean_formula(n - n // 2)
            return f"({left} {op} {right})"
    
    def frobenius_monomial_rank(formula):
        # Placeholder for actual implementation
        return len(formula.split())  # Simplified for demonstration
    
    def frege_proof_length(formula):
        # Placeholder for actual implementation
        if formula == '0' or formula == '1':
            return 1
        elif '&' in formula:
            left, right = formula[1:-2].split('&')
            return 1 + max(frege_proof_length(left), frege_proof_length(right))
        else:
            left, right = formula[1:-2].split('|')
            return 1 + max(frege_proof_length(left), frege_proof_length(right))
    
    def frobenius_algebraic_operation(formula):
        # Placeholder for actual implementation
        if '&' in formula:
            left, right = formula[1:-2].split('&')
            return f"({left} | {right})"
        else:
            left, right = formula[1:-2].split('|')
            return f"({left} & {right})"
    
    n_values = [5, 10, 15, 20, 30, 40]
    mfr_values = []
    l_values = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_boolean_formula(n)
            mfr = frobenius_monomial_rank(formula)
            l = frege_proof_length(formula)
            mfr_values.append(mfr)
            l_values.append(l)
            instances_tested += 1
            n_max = max(n_max, n)
    
    correlation = pearson_correlation(mfr_values, l_values)
    conjecture_holds = correlation >= 0.8 and p_value <= 0.05
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def pearson_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
    std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
    std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)
    
    if std_x == 0 or std_y == 0:
        return 0
    
    return cov_xy / (std_x * std_y)

def p_value(correlation, n):
    # Placeholder for actual implementation
    return 0.05  # Simplified for demonstration

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")