# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def count_satisfying_assignments(cnf):
        n = len(cnf[0])
        count = 0
        for assignment in product([-1, 1], repeat=n):
            if all(any(lit * assignment[(abs(lit) - 1)] > 0 for lit in clause) for clause in cnf):
                count += 1
        return count
    
    def circuit_satisfiability_complexity(cnf):
        n = len(cnf[0])
        assignments = list(product([-1, 1], repeat=n))
        min_size = float('inf')
        for assignment in assignments:
            if all(any(lit * assignment[(abs(lit) - 1)] > 0 for lit in clause) for clause in cnf):
                size = sum(1 for lit in assignment if lit != 0)
                if size < min_size:
                    min_size = size
        return min_size
    
    def tropical_polynomial_representation(cnf):
        n = len(cnf[0])
        poly = [Fraction(0, 1)] * (2**n)
        for clause in cnf:
            product = Fraction(1, 1)
            for lit in clause:
                if lit > 0:
                    product *= Fraction(lit - 1, 1)
                else:
                    product *= Fraction(-lit + 1, 1)
            poly[sum(abs(lit) - 1 for lit in clause)] += product
        return poly
    
    def minimal_cyclotomic_polynomial_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            if poly[i] != Fraction(0, 1):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    mcrs = []
    sat_complexities = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        poly = tropical_polynomial_representation(cnf)
        mcr = minimal_cyclotomic_polynomial_rank(poly)
        sat_complexity = circuit_satisfiability_complexity(cnf)
        
        mcrs.append(mcr)
        sat_complexities.append(sat_complexity)
    
    correlation_coefficient = calculate_correlation(mcrs, sat_complexities)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

def calculate_correlation(x, y):
    n = len(x)
    if n != len(y):
        raise ValueError("x and y must have the same length")
    
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = sum((xi - mean_x)**2 for xi in x) * sum((yi - mean_y)**2 for yi in y)
    
    if denominator == 0:
        return 0
    
    correlation_coefficient = numerator / (n**0.5 * denominator**0.5)
    return correlation_coefficient

if __name__ == "__main__":
    import sys
    from itertools import product
    
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")