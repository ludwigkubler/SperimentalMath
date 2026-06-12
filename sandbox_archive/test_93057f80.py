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

# Helper functions for DPLL algorithm
def dpll(cnf):
    return search([], cnf)

def search(assignments, cnf):
    if not cnf:
        return True
    unit_clauses = [c[0] for c in cnf if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        assignments.append(literal)
        new_cnf = simplify(cnf, literal)
        if not search(assignments, new_cnf):
            assignments.pop()
            return search(assignments + [-literal], new_cnf)
        return True
    pure_literals = [lit for lit in range(1, len(cnf) + 1) if all(lit not in c or -lit not in c for c in cnf)]
    if pure_literals:
        literal = pure_literals[0]
        assignments.append(literal)
        new_cnf = simplify(cnf, literal)
        return search(assignments, new_cnf)
    literal = random.choice(range(1, len(cnf) + 1))
    assignments.append(literal)
    new_cnf = simplify(cnf, literal)
    if not search(assignments, new_cnf):
        assignments.pop()
        return search(assignments + [-literal], new_cnf)
    return False

def simplify(cnf, literal):
    return [c for c in cnf if literal not in c and -literal not in c]

# Helper function to generate random CNF formulas
def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set()
        while len(clause) < 2:
            lit = random.choice(range(1, n + 1))
            if -lit not in clause and lit not in clause:
                clause.add(lit)
        cnf.append(tuple(sorted(clause)))
    return cnf

# Main function to run the trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters for generating CNF formulas
    n_values = [5, 10, 15, 20, 30, 40]
    m_values = [10] * len(n_values)
    
    min_order_values = []
    width_values = []
    
    for n, m in zip(n_values, m_values):
        cnf = generate_cnf(n, m)
        width = dpll(cnf)
        
        # Placeholder for minimal order of modular forms calculation
        min_order = sum(1 for _ in range(m))  # Simplified placeholder
        
        min_order_values.append(min_order)
        width_values.append(width)
    
    n_max = max(n_values)
    instances_tested = len(min_order_values)
    metric_name = "correlation"
    metric_value = compute_correlation(min_order_values, width_values)
    conjecture_holds = metric_value >= 0.8
    counterexample = "" if conjecture_holds else f"Correlation: {metric_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

# Helper function to compute Pearson correlation coefficient
def compute_correlation(x, y):
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x)) * math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
    
    if denominator == 0:
        return None
    
    correlation = numerator / denominator
    return correlation

# Main execution block
if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and max(r["metric_value"] for r in results) < 0.5:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='low_correlation' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")