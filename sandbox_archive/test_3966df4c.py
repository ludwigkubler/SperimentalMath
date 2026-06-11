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
    
    # Generate a CNF with known resolution proof length (simplified example)
    n = 10  # Number of variables
    m = 2 * n  # Number of clauses
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), random.randint(-n, -1)]
        cnf.append(clause)
    
    # Construct the algebraic curve associated with the CNF (simplified example)
    def construct_curve(cnf):
        curve_points = set()
        for clause in cnf:
            x, y = abs(clause[0]), abs(clause[1])
            if (x, y) not in curve_points:
                curve_points.add((x, y))
        return curve_points
    
    curve_points = construct_curve(cnf)
    
    # Compute the minimal number of integer points on the curve
    min_int_points = len(curve_points)
    
    # Calculate the length of the resolution proof (simplified example)
    def resolve_clause(clause, model):
        for lit in clause:
            if lit < 0 and -lit in model:
                return True
            elif lit > 0 and lit not in model:
                return False
        return False
    
    def resolve_cnf(cnf, model):
        while cnf:
            new_clause = []
            for clause in cnf:
                if not resolve_clause(clause, model):
                    new_clause.append(clause)
            if len(new_clause) == len(cnf):
                break
            cnf = new_clause
    
    def generate_model(n):
        return set(random.sample(range(1, n+1), random.randint(0, n)))
    
    model = generate_model(n)
    resolve_cnf(cnf, model)
    length_resolution_proof = len(cnf)  # Simplified example
    
    # Measure the correlation coefficient
    def correlation_coefficient(x, y):
        if len(x) != len(y):
            return None
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y) if std_x != 0 and std_y != 0 else None
    
    x_values = [min_int_points]
    y_values = [length_resolution_proof]
    
    corr_coeff = correlation_coefficient(x_values, y_values)
    
    # Check the acceptance criterion
    conjecture_holds = corr_coeff is not None and abs(corr_coeff - 1) <= 0.1
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": corr_coeff,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")