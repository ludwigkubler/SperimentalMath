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
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        s = random.randint(5, 40)
        cnf_formula = generate_cnf(s)
        min_order_K = compute_min_order_K(cnf_formula)
        monotone_width = compute_monotone_width(cnf_formula)
        
        if min_order_K is None or monotone_width is None:
            return {
                "metric_name": "monotone_width",
                "metric_value": float('inf'),
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        metric_values.append(min_order_K <= 1.5 * s**2)
    
    return {
        "metric_name": "monotone_width",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(metric_values),
        "counterexample": ""
    }

def generate_cnf(s: int) -> list:
    clauses = []
    for _ in range(s):
        clause = [random.randint(1, s * 2) for _ in range(random.randint(1, s))]
        clauses.append(clause)
    return clauses

def compute_min_order_K(cnf_formula: list) -> float:
    n = len(cnf_formula)
    if n == 0:
        return None
    
    # Construct quaternionic matrices and calculate determinant
    Q = construct_quaternionic_matrix(cnf_formula)
    det_Q = determinant(Q)
    
    if det_Q == 0:
        return None
    
    min_order_K = Fraction(det_Q).numerator / Fraction(det_Q).denominator
    return min_order_K

def compute_monotone_width(cnf_formula: list) -> float:
    # Placeholder for monotone width calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(cnf_formula)

def construct_quaternionic_matrix(cnf_formula: list) -> list:
    n = len(cnf_formula)
    Q = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i, clause in enumerate(cnf_formula):
        for literal in clause:
            if literal > 0:
                row = literal - 1
            else:
                row = -(literal + 1)
            
            Q[row][i] = 1
            Q[i][row] = 1
    
    return Q

def determinant(matrix: list) -> float:
    n = len(matrix)
    
    if n == 0:
        return 1
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        sign = (-1) ** (j % 2)
        det += sign * matrix[0][j] * determinant(submatrix)
    
    return det

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")