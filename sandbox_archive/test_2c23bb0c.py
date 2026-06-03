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
    
    def generate_tseitin_formula(n):
        literals = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Generate conjunction of all literals
        conjunction = ' & '.join(literals)
        clauses.append(conjunction)
        
        # Generate disjunctions for each literal and its negation
        for lit in literals:
            clauses.append(f'~{lit} | {" & ".join([other_lit for other_lit in literals if other_lit != lit])}')
        
        return ' | '.join(clauses)
    
    def clause_indicator_polynomial(formula, n):
        # Simplify the formula to extract coefficients
        # This is a placeholder implementation; actual polynomial extraction is complex and not shown here.
        # For simplicity, we'll assume a linear polynomial for this example.
        return [1] * (n + 1)  # Placeholder coefficients
    
    def sum_of_absolute_values(poly):
        return sum(abs(coeff) for coeff in poly)
    
    def frege_proof_length(formula):
        # Simplified DPLL solver to estimate proof length
        # This is a placeholder implementation; actual DPLL is complex and not shown here.
        # For simplicity, we'll assume a linear proof length for this example.
        return len(formula.split(' | ')) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        poly = clause_indicator_polynomial(formula, n)
        abs_sum = sum_of_absolute_values(poly)
        proof_length = frege_proof_length(formula)
        
        results.append({
            "n": n,
            "abs_sum": abs_sum,
            "proof_length": proof_length
        })
    
    if len(results) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    abs_sums = [result["abs_sum"] for result in results]
    proof_lengths = [result["proof_length"] for result in results]
    
    def linear_regression(x, y):
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_xx = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        correlation_coefficient = (n * sum_xy - sum_x * sum_y) / math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
        
        return slope, intercept, correlation_coefficient
    
    slope, intercept, correlation_coefficient = linear_regression(abs_sums, proof_lengths)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "correlation_too_low"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_dev = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["metric_value"] is not None for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(result["counterexample"] == "correlation_too_low" for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] == "correlation_too_low")
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_or_other_reason")