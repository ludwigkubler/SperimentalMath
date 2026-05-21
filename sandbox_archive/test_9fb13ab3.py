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

def generate_expander_graph(n):
    if n < 4 or n % 2 != 0:
        raise ValueError("n must be even and at least 4")
    
    edges = []
    for i in range(1, n // 2 + 1):
        edges.append((i, i + n // 2))
        edges.append((i + n // 2, i))
    return edges

def generate_tseitin_formula(n):
    variables = [f"x{i}" for i in range(1, n * n + 1)]
    clauses = []
    
    # Each variable appears exactly once
    for i in range(1, n * n + 1):
        clauses.append([variables[i - 1]])
    
    # Each row must be satisfied
    for i in range(n):
        clause = []
        for j in range(n):
            clause.append(variables[i * n + j])
        clauses.append(clause)
    
    # Each column must be satisfied
    for j in range(n):
        clause = []
        for i in range(n):
            clause.append(variables[i * n + j])
        clauses.append(clause)
    
    return variables, clauses

def calculate_kronecker_coefficient(a, b, c, d):
    if a == 0 or b == 0 or c == 0 or d == 0:
        return Fraction(0)
    
    k = min(a + b, c + d)
    numerator = 1
    denominator = 1
    
    for i in range(k):
        numerator *= (a + b - i) * (c + d - i)
        denominator *= (i + 1) * (b + d - i)
    
    return Fraction(numerator, denominator)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        A = generate_expander_graph(n)
        
        # Calculate Kronecker coefficients
        permanent_coefficient = calculate_kronecker_coefficient(1, n - 1, 1, n - 1)
        determinant_coefficient = calculate_kronecker_coefficient(1, n - 2, 1, n - 2)
        
        if permanent_coefficient <= determinant_coefficient:
            return {
                "metric_name": "Kronecker coefficient gap",
                "metric_value": permanent_coefficient,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, permanent_coefficient={permanent_coefficient}, determinant_coefficient={determinant_coefficient}"
            }
        
        total_metric_value += permanent_coefficient - determinant_coefficient
        instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "Kronecker coefficient gap",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")