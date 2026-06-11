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

def generate_tseitin_formula(n):
    if n <= 0:
        return []
    
    variables = [f'x{i}' for i in range(1, n + 1)]
    clauses = []
    
    def add_clause(lit1, lit2):
        if isinstance(lit1, str) and lit1.startswith('-'):
            lit1 = -int(lit1[1:])
        if isinstance(lit2, str) and lit2.startswith('-'):
            lit2 = -int(lit2[1:])
        clauses.append([lit1, lit2])
    
    for i in range(1, n + 1):
        add_clause(variables[i-1], variables[i])
    
    return clauses

def dpll_search_tree_width(clauses):
    def dfs(model, literals):
        if not literals:
            return 0
        literal = literals[0]
        pos_clauses = [c for c in clauses if literal in c or -literal in c]
        neg_clauses = [c for c in clauses if literal not in c and -literal not in c]
        
        if not pos_clauses:
            return dfs(model, literals[1:])
        
        max_width = 0
        for clause in pos_clauses:
            new_model = model.copy()
            new_model[literal] = True
            width = dfs(new_model, [l for l in literals if l != literal and -l not in literals])
            max_width = max(max_width, width)
        
        return max_width + 1
    
    initial_model = {}
    initial_literals = list(range(1, len(variables) + 1))
    return dfs(initial_model, initial_literals)

def minimal_order_brauer_group(n):
    # Placeholder for Brauer group computation
    # This is a mock implementation and does not reflect actual Brauer group calculation
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_tseitin_formula(n)
        if not clauses:
            continue
        
        width = dpll_search_tree_width(clauses)
        order_brauer_group = minimal_order_brauer_group(n)
        
        if width == 0 or order_brauer_group == 0:
            continue
        
        results.append((order_brauer_group, math.log(width) ** 2))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n = len(results)
    sum_x = sum(x for x, _ in results)
    sum_y = sum(y for _, y in results)
    sum_xy = sum(x * y for x, y in results)
    sum_xx = sum(x ** 2 for x, _ in results)
    sum_yy = sum(y ** 2 for _, y in results)
    
    mean_x = sum_x / n
    mean_y = sum_y / n
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_xx - sum_x ** 2) * (n * sum_yy - sum_y ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 10 and correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    if all(result["metric_value"] is not None for result in results):
        values = [result["metric_value"] for result in results]
        mean = sum(values) / len(values)
        std = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        elif any(result["metric_value"] < 0.5 or result["metric_value"] > 10 for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if result["metric_value"] < 0.5 or result["metric_value"] > 10)
            print(f"RESULT: FALSIFIED counterexample=\"metric out of bounds\" first_failing_seed={first_failing_seed}")
        else:
            print(f"RESULT: INCONCLUSIVE reason=unknown")
    else:
        print("RESULT: INCONCLUSIVE reason=missing data")