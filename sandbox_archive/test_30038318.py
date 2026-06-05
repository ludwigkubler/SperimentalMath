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

def tseitin_formula(n):
    if n <= 0:
        return []
    
    variables = [f'x{i}' for i in range(2*n)]
    clauses = []

    # Base case: x1 ∨ ¬x2
    clauses.append([variables[0], -variables[1]])

    # Recursive case: (xi ∨ ¬xi+1) ∧ (¬xi ∨ xi+2)
    for i in range(n-1):
        clauses.append([variables[2*i], -variables[2*i+1]])
        clauses.append([-variables[2*i], variables[2*i+2]])

    return clauses

def dpll(clauses, assignment):
    if not clauses:
        return True
    unit_clauses = [c for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0][0]
        new_assignment = assignment[:]
        new_assignment[abs(literal)-1] = literal > 0
        return dpll([c for c in clauses if literal not in c], new_assignment)
    
    literal = random.choice(clauses[0])
    new_assignment = assignment[:]
    new_assignment[abs(literal)-1] = literal > 0
    if dpll(clauses, new_assignment):
        return True
    
    new_assignment[abs(literal)-1] = not (literal > 0)
    return dpll(clauses, new_assignment)

def circuit_monotone_width(clauses):
    assignment = [False] * len(clauses)
    if dpll(clauses, assignment):
        return 0
    for i in range(len(assignment)):
        assignment[i] = True
        if not dpll(clauses, assignment):
            assignment[i] = False
            break
    return sum(1 for a in assignment if a)

def minimal_representation_rank(n):
    clauses = tseitin_formula(n)
    # Simplify the circuit by removing redundant clauses and variables
    rank = len(set([tuple(sorted(c)) for c in clauses]))
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    r_values = []
    w_m_values = []
    
    for n in n_values:
        rank = minimal_representation_rank(n)
        width = circuit_monotone_width(clauses)
        r_values.append(rank)
        w_m_values.append(width)
    
    correlation_coefficient = pearson_correlation(r_values, w_m_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "Pearson correlation coefficient < 0.7"
    }

def pearson_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    std_dev_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)) / n)
    std_dev_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)) / n)
    return cov_xy / (std_dev_x * std_dev_y)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")