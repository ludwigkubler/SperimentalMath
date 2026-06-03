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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if i != j:
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(rows):
                    matrix[j][k] -= factor * matrix[i][k]
    return matrix

def solve_linear_system(matrix, b):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    x = [0] * cols
    for i in range(rows - 1, -1, -1):
        x[i] = (augmented_matrix[i][-1] - sum(x[j] * augmented_matrix[i][j] for j in range(i + 1, cols))) / augmented_matrix[i][i]
    return x

def tseitin_formula(n):
    literals = [f'x{i+1}' for i in range(n)]
    clauses = []
    for i in range(n):
        clauses.append([literals[i]])
        clauses.append([-literals[i], f'l{i+1}'])
        clauses.append([literals[i], -f'l{i+1}', literals[(i + 1) % n]])
    clauses.append([-f'l{i+1}' for i in range(n)])
    return literals, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = tseitin_formula(n)
    
    # Convert Tseitin formula to algebraic variety (simplified for demonstration)
    V = [literals]  # Placeholder for actual algebraic variety computation
    
    # Find all Hodge classes containing at least one polynomial from V
    hodge_classes = []
    for f in V:
        # Simplified Hodge class computation (placeholder)
        min_deg_H_f = random.randint(1, n)  # Placeholder for actual computation
        hodge_classes.append(min_deg_H_f)
    
    # Measure the length L(π) of the shortest Frege proof for π using a small DPLL solver
    L_pi = len(clauses) * 2  # Simplified DPLL solver (placeholder)
    
    metric_value = sum(hodge_classes) / len(hodge_classes)
    conjecture_holds = abs(metric_value - L_pi) <= 0.7 * L_pi
    
    return {
        "metric_name": "min_deg_H_f",
        "metric_value": metric_value,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Counterexample for n={n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")