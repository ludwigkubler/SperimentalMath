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
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(random.randint(5, 20)):
            clause = random.sample(variables + [f'-{v}' for v in variables], random.randint(1, n))
            clauses.append(' OR '.join(clause))
        return ' AND '.join(clauses)
    
    def clause_tree_width(formula):
        if ' AND ' not in formula:
            return 0
        parts = formula.split(' AND ')
        max_width = 0
        for part in parts:
            width = 1 + max([clause_tree_width(p) for p in part.split(' OR ')])
            max_width = max(max_width, width)
        return max_width
    
    def twisted_tensor_product(formula):
        n = len([v for v in formula if v.startswith('x')])
        tensor = [[0] * (n+1) for _ in range(n+1)]
        for clause in formula.split(' AND '):
            literals = [l.strip('-') for l in clause.split(' OR ')]
            for lit in literals:
                i = int(lit[1:]) if lit.startswith('x') else -int(lit[1:])
                tensor[i][i] += 1
        return tensor
    
    def min_rank(tensor):
        n = len(tensor)
        rank = 0
        for _ in range(n):
            max_val = -math.inf
            max_idx = -1
            for i in range(n):
                if tensor[i][-1] > max_val:
                    max_val = tensor[i][-1]
                    max_idx = i
            rank += max_val
            for j in range(n):
                tensor[j][max_idx] -= max_val
        return rank
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + 20 > end_time:
            return {
                "metric_name": "ctw",
                "metric_value": sum(metric_values) / len(metric_values),
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        
        for _ in range(5):
            formula = generate_formula(n)
            ctw = clause_tree_width(formula)
            tensor = twisted_tensor_product(formula)
            mrt = min_rank(tensor)
            
            if n_max < n:
                n_max = n
            
            instances_tested += 1
            metric_values.append(ctw - mrt)
    
    correlation_coefficient, p_value = pearson_correlation(metric_values, range(5, 26))
    
    return {
        "metric_name": "ctw",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.5 and p_value <= 0.05,
        "counterexample": ""
    }

def pearson_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x)**2 for xi in x)) * math.sqrt(sum((yi - mean_y)**2 for yi in y))
    
    correlation_coefficient = numerator / denominator
    p_value = 2 * (1 - min(1, abs(correlation_coefficient)))
    
    return correlation_coefficient, p_value

if __name__ == "__main__":
    import sys
    import time
    
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    end_time = time.time() + 240
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")